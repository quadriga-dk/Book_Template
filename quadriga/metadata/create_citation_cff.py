"""
Generate the CITATION.cff file from metadata.yml.

metadata.yml is the single source of truth for all metadata. This script
rebuilds CITATION.cff from it completely on every run — manual edits to
CITATION.cff will be overwritten.

The generated file contains a root citation (CFF type 'software', as required
by the CFF 1.2.0 schema for repository citations) and a 'preferred-citation'
of type 'book' that carries the full citation for the OER itself, including
DOI, year, language and license.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from .utils import (
    extract_keywords,
    get_content_license,
    get_doi,
    get_file_path,
    get_languages,
    get_publication_year,
    load_yaml_file,
    save_yaml_file,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def _cff_person(person: dict) -> dict:
    """
    Convert a metadata.yml author/contributor entry to a CFF person.

    Copies only the fields CFF understands (drops e.g. 'credit').

    Args:
        person: Author or contributor dictionary from metadata.yml

    Returns
    -------
        dict: CFF person entry
    """
    cff_person = {}
    for key in ("given-names", "family-names", "orcid", "affiliation"):
        if key in person:
            cff_person[key] = person[key]
    return cff_person


def build_citation_data(metadata: dict) -> dict:
    """
    Build the complete CITATION.cff data structure from metadata.yml.

    Args:
        metadata: Parsed metadata.yml data

    Returns
    -------
        dict: A valid CFF 1.2.0 data structure
    """
    title = metadata.get("title", "Untitled")
    if title == "Untitled":
        logger.warning("No title found in metadata.yml, using 'Untitled'")

    authors = [person for person in (_cff_person(a) for a in metadata.get("authors", [])) if person]
    if not authors:
        logger.warning("No authors found in metadata.yml")
        authors = [{"name": "Unknown"}]

    keywords = extract_keywords(metadata.get("keywords"))
    doi = get_doi(metadata)
    if not doi:
        logger.warning("No DOI found in metadata.yml 'identifier' field")
    license_id = get_content_license(metadata)
    year = get_publication_year(metadata)
    languages = get_languages(metadata)

    citation_data: dict = {
        "cff-version": "1.2.0",
        "title": title,
    }

    if "description" in metadata:
        citation_data["abstract"] = metadata["description"]

    citation_data["type"] = "software"
    citation_data["message"] = "Please cite this software using the metadata from `preferred-citation` in `CITATION.cff`."
    citation_data["authors"] = authors

    if doi:
        citation_data["identifiers"] = [{"type": "doi", "value": doi, "description": "Zenodo"}]

    if "git" in metadata:
        citation_data["repository-code"] = metadata["git"]

    if "url" in metadata:
        citation_data["url"] = metadata["url"]

    if keywords:
        citation_data["keywords"] = keywords

    if license_id:
        citation_data["license"] = license_id

    # QUADRIGA OERs are built with Jupyter Book — cite it as a reference
    if metadata.get("learning-resource-type") == "Jupyter Book":
        citation_data["references"] = [
            {
                "title": "Jupyter Book",
                "type": "software",
                "authors": [
                    {
                        "name": "The Jupyter Book Community",
                        "website": "https://github.com/jupyter-book/jupyter-book/graphs/contributors",
                    }
                ],
            }
        ]

    # The preferred citation for the OER itself (a book, not the repository).
    # Authors and keywords reuse the same objects as the root citation, which
    # PyYAML serializes as anchors/aliases.
    preferred_citation: dict = {}
    if year:
        preferred_citation["year"] = year
    preferred_citation["authors"] = authors
    preferred_citation["title"] = title
    preferred_citation["type"] = "book"
    if doi:
        preferred_citation["doi"] = doi
    if "url" in metadata:
        preferred_citation["url"] = metadata["url"]
    if "git" in metadata:
        preferred_citation["repository-code"] = metadata["git"]
    if license_id:
        preferred_citation["license"] = license_id
    if languages:
        preferred_citation["languages"] = languages
    if license_id:
        preferred_citation["copyright"] = license_id
    if keywords:
        preferred_citation["keywords"] = keywords
    if "version" in metadata:
        preferred_citation["version"] = metadata["version"]

    citation_data["preferred-citation"] = preferred_citation

    if "version" in metadata:
        citation_data["version"] = metadata["version"]

    return citation_data


def create_citation_cff() -> bool:
    """
    Generate the CITATION.cff file from metadata.yml.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Define file paths
        try:
            repo_root = get_file_path("")  # Get repo root by providing empty relative path
            metadata_path = get_file_path("metadata.yml", repo_root)
            citation_cff_path = get_file_path("CITATION.cff", repo_root)
        except Exception:
            logger.exception("Failed to resolve file paths")
            return False

        # metadata.yml must exist
        if not Path(metadata_path).exists():
            logger.error("Required file metadata.yml not found at %s", metadata_path)
            return False

        # Load metadata.yml
        metadata = load_yaml_file(metadata_path)

        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load metadata.yml or invalid format. Exiting.")
            return False

        citation_data = build_citation_data(metadata)

        return save_yaml_file(
            citation_cff_path,
            citation_data,
            schema_comment="# yaml-language-server: $schema=https://citation-file-format.github.io/1.2.0/schema.json",
        )

    except Exception:
        logger.exception("Unexpected error in create_citation_cff")
        return False


if __name__ == "__main__":
    success = create_citation_cff()
    sys.exit(0 if success else 1)
