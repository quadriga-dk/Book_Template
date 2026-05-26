"""
Create the CITATION.bib file from metadata.yml.

metadata.yml is the single source of truth for all metadata. This script
rebuilds CITATION.bib from it completely on every run.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone

from .utils import (
    extract_keywords,
    format_authors_for_bibtex,
    generate_citation_key,
    get_content_license,
    get_doi,
    get_file_path,
    get_languages,
    get_publication_year,
    load_yaml_file,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def _bibtex_field(name: str, value: str) -> str:
    """Format a single BibTeX field line, sanitizing braces in the value."""
    clean_value = str(value).replace("{", "").replace("}", "")
    return f"  {name:<9} = {{{clean_value}}},"


def create_bibtex_from_metadata() -> bool:
    """
    Create a CITATION.bib file from metadata.yml.

    QUADRIGA OERs are published as books (Jupyter Books), so the entry type
    is '@book'.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Define file paths using utility functions
        try:
            repo_root = get_file_path("")  # Get repo root
            metadata_path = get_file_path("metadata.yml", repo_root)
            citation_bib_path = get_file_path("CITATION.bib", repo_root)
        except Exception:
            logger.exception("Failed to resolve file paths")
            return False

        if not metadata_path.exists():
            logger.error("metadata.yml file not found at %s", metadata_path)
            return False

        metadata = load_yaml_file(metadata_path)

        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load metadata.yml or invalid format. Exiting.")
            return False

        title = metadata.get("title", "")
        if not title:
            logger.warning("No title found in metadata.yml")

        authors = metadata.get("authors", [])
        if not authors:
            logger.warning("No authors found in metadata.yml")

        year = get_publication_year(metadata)
        if not year:
            year = str(datetime.now(tz=timezone.utc).year)
            logger.info("No date-modified or date-issued found, using current year: %s", year)

        try:
            author_str = format_authors_for_bibtex(authors)
        except Exception:
            logger.exception("Error formatting authors")
            author_str = ""

        try:
            citation_key = generate_citation_key(authors, title, year)
        except Exception:
            logger.exception("Error generating citation key")
            citation_key = "Unknown_Citation_Key"

        # Compile BibTeX entry
        bibtex_lines = [f"@book{{{citation_key},"]

        if title:
            bibtex_lines.append(_bibtex_field("title", title))
        if author_str:
            bibtex_lines.append(_bibtex_field("author", author_str))
        if year:
            bibtex_lines.append(_bibtex_field("year", year))
        if "version" in metadata:
            bibtex_lines.append(_bibtex_field("version", metadata["version"]))

        doi = get_doi(metadata)
        if doi:
            bibtex_lines.append(_bibtex_field("doi", doi))
        else:
            logger.warning("No DOI found in metadata.yml 'identifier' field")

        if "url" in metadata:
            bibtex_lines.append(_bibtex_field("url", metadata["url"]))

        license_id = get_content_license(metadata)
        if license_id:
            bibtex_lines.append(_bibtex_field("copyright", license_id))

        languages = get_languages(metadata)
        if languages:
            bibtex_lines.append(_bibtex_field("language", ", ".join(languages)))

        keywords = extract_keywords(metadata.get("keywords"))
        if keywords:
            bibtex_lines.append(_bibtex_field("keywords", ", ".join(keywords)))

        # Close the entry
        bibtex_lines.append("}")
        bibtex = "\n".join(bibtex_lines)

        # Write to CITATION.bib
        try:
            with citation_bib_path.open("w", encoding="utf-8") as f:
                f.write(bibtex)
        except OSError:
            logger.exception("Error writing to %s", citation_bib_path)
            return False
        else:
            logger.info("BibTeX citation successfully created at %s", citation_bib_path)
            return True

    except Exception:
        logger.exception("Unexpected error in create_bibtex_from_metadata")
        return False


if __name__ == "__main__":
    success = create_bibtex_from_metadata()
    sys.exit(0 if success else 1)
