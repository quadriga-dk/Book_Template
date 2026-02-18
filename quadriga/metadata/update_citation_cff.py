"""
Update or create the CITATION.cff file with metadata from metadata.yml.

This script reads metadata from 'metadata.yml' and updates the corresponding
fields in 'CITATION.cff'. It handles fields like title, authors, URL,
repository URL, and publication date. It also ensures that the
'preferred-citation' section, if present, is updated consistently.

If CITATION.cff does not exist, a new one is created from metadata.yml with
the required CFF boilerplate fields.
"""

import logging
import sys
from pathlib import Path

from .utils import extract_keywords, get_file_path, load_yaml_file, save_yaml_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def _create_initial_citation_cff(metadata: dict) -> dict:
    """
    Create an initial CITATION.cff data structure from metadata.yml.

    Builds a minimal valid CFF 1.2.0 file with the required fields
    (cff-version, message, title, authors) plus optional fields
    that can be derived from metadata.yml.

    Args:
        metadata: Parsed metadata.yml data

    Returns
    -------
        dict: A valid CFF data structure
    """
    citation_data: dict = {
        "cff-version": "1.2.0",
        "message": "If you use this work, please cite it using the metadata from this file.",
        "type": "dataset",
    }

    # Title (required by CFF)
    citation_data["title"] = metadata.get("title", "Untitled")

    # Authors (required by CFF)
    if metadata.get("authors"):
        citation_authors = []
        for author in metadata["authors"]:
            cff_author: dict = {}
            if "given-names" in author:
                cff_author["given-names"] = author["given-names"]
            if "family-names" in author:
                cff_author["family-names"] = author["family-names"]
            if "orcid" in author:
                cff_author["orcid"] = author["orcid"]
            if "affiliation" in author:
                cff_author["affiliation"] = author["affiliation"]
            if cff_author:
                citation_authors.append(cff_author)
        citation_data["authors"] = citation_authors if citation_authors else [{"name": "Unknown"}]
    else:
        citation_data["authors"] = [{"name": "Unknown"}]

    # Optional fields from metadata
    if "version" in metadata:
        citation_data["version"] = metadata["version"]

    if "url" in metadata:
        citation_data["url"] = metadata["url"]

    if "git" in metadata:
        citation_data["repository-code"] = metadata["git"]

    if "identifier" in metadata:
        doi_url = metadata["identifier"]
        if "doi.org" in str(doi_url):
            # Extract DOI value from URL
            doi_value = str(doi_url).split("doi.org/")[-1] if "doi.org/" in str(doi_url) else None
            if doi_value:
                citation_data["identifiers"] = [
                    {"type": "doi", "value": doi_value, "description": "Zenodo"}
                ]

    if "description" in metadata:
        citation_data["abstract"] = metadata["description"]

    if metadata.get("keywords"):
        flattened = extract_keywords(metadata["keywords"])
        if flattened:
            citation_data["keywords"] = flattened

    if "license" in metadata:
        license_data = metadata["license"]
        if isinstance(license_data, str):
            citation_data["license"] = license_data
        elif isinstance(license_data, dict) and "content" in license_data:
            # Use content license as primary (most relevant for citation)
            content_license = license_data["content"]
            if isinstance(content_license, str):
                citation_data["license"] = content_license
            elif isinstance(content_license, list) and content_license:
                citation_data["license"] = content_license[0]

    logger.info("Created initial CITATION.cff from metadata.yml")
    return citation_data


def update_citation() -> bool:
    """
    Update or create the CITATION.cff file using data from the metadata.yml file.

    If CITATION.cff exists, the function updates its fields based on metadata.yml,
    preserving existing author details and preferred-citation sections.

    If CITATION.cff does not exist, a new one is created from metadata.yml with
    the required CFF boilerplate.

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

        # Load existing CITATION.cff or create initial structure
        if Path(citation_cff_path).exists():
            citation_data = load_yaml_file(citation_cff_path)
            if not citation_data or not isinstance(citation_data, dict):
                logger.error("Could not load CITATION.cff or invalid format. Exiting.")
                return False
        else:
            logger.info("CITATION.cff not found — creating from metadata.yml")
            citation_data = _create_initial_citation_cff(metadata)

        # Track if updates were made
        updates_made = False

        # Update citation fields based on metadata
        if "title" in metadata:
            citation_data["title"] = metadata["title"]
            # Also update preferred-citation if it exists
            if "preferred-citation" in citation_data:
                citation_data["preferred-citation"]["title"] = metadata["title"]
            updates_made = True
            logger.info("Updated title to: %s", metadata["title"])
        else:
            logger.warning("No title found in metadata.yml")

        if "version" in metadata:
            citation_data["version"] = metadata["version"]
            if "preferred-citation" in citation_data:
                citation_data["preferred-citation"]["version"] = metadata["version"]
            updates_made = True
            logger.info("Updated version to: %s", metadata["version"])
        else:
            logger.warning("No version found in metadata.yml, skipping version update")

        if metadata.get("authors"):
            try:
                # Convert metadata authors format to citation authors format
                citation_authors = []
                for author in metadata["authors"]:
                    new_author_entry = {}
                    # Copy existing citation data for authors entry if exists
                    for cit_author in citation_data.get("authors", []):
                        if (
                            "given-names" in cit_author
                            and "family-names" in cit_author
                            and "given-names" in author
                            and "family-names" in author
                        ) and (
                            cit_author["given-names"] == author["given-names"]
                            and cit_author["family-names"] == author["family-names"]
                        ):
                            new_author_entry = cit_author
                            break

                    # Update author entry with metadata
                    if "given-names" in author:
                        new_author_entry["given-names"] = author["given-names"]
                    if "family-names" in author:
                        new_author_entry["family-names"] = author["family-names"]
                    if "orcid" in author:
                        new_author_entry["orcid"] = author["orcid"]
                    if "affiliation" in author:
                        new_author_entry["affiliation"] = author["affiliation"]
                    citation_authors.append(new_author_entry)

                if citation_authors:
                    citation_data["authors"] = citation_authors

                    # Also update preferred-citation if it exists
                    if "preferred-citation" in citation_data:
                        citation_data["preferred-citation"]["authors"] = citation_authors

                    updates_made = True
                    logger.info("Updated %d authors", len(citation_authors))
                else:
                    logger.warning("Failed to process authors from metadata.yml")
            except Exception:
                logger.exception("Error processing authors")
        else:
            logger.warning("No authors found in metadata.yml")

        # Update URL if present in metadata
        if "url" in metadata:
            citation_data["url"] = metadata["url"]
            if "preferred-citation" in citation_data:
                citation_data["preferred-citation"]["url"] = metadata["url"]
            updates_made = True
            logger.info("Updated URL to: %s", metadata["url"])

        # Update repository URL if present in metadata
        if "git" in metadata:
            citation_data["repository-code"] = metadata["git"]
            if "preferred-citation" in citation_data:
                citation_data["preferred-citation"]["repository-code"] = metadata["git"]
            updates_made = True
            logger.info("Updated repository-code to: %s", metadata["git"])

        # Update publication year based on date-modified or date-issued
        # Prefer newer date-modified, if available
        year_source = None
        year_value = None

        year_digits = 4
        if "date-modified" in metadata:
            date_str = metadata["date-modified"]
            if isinstance(date_str, str) and len(date_str) >= year_digits:
                year_value = date_str[:4]
                year_source = "date-modified"
        elif "date-issued" in metadata:
            date_str = metadata["date-issued"]
            if isinstance(date_str, str) and len(date_str) >= year_digits:
                year_value = date_str[:4]  # Extract year from YYYY-MM-DD
                year_source = "date-issued"
        if year_value and "preferred-citation" in citation_data:
            citation_data["preferred-citation"]["year"] = year_value
            updates_made = True
            logger.info("Updated publication year to: %s (from %s)", year_value, year_source)

        if "description" in metadata:
            citation_data["abstract"] = metadata["description"]
            updates_made = True
            logger.info("Updated abstract from description")

        # Update keywords if present in metadata
        # Extract keywords to flatten any language-keyed formats
        if metadata.get("keywords"):
            flattened_keywords = extract_keywords(metadata["keywords"])
            if flattened_keywords:
                citation_data["keywords"] = flattened_keywords
                if "preferred-citation" in citation_data:
                    citation_data["preferred-citation"]["keywords"] = flattened_keywords
                updates_made = True
                logger.info("Updated keywords with %d items", len(flattened_keywords))
            else:
                logger.warning("Keywords found in metadata.yml but could not be extracted")
        else:
            logger.warning("No keywords found in metadata.yml")

        # No changes
        if not updates_made:
            logger.warning("No updates were made to CITATION.cff")
            return True  # Not an error, just no changes needed

        # Save updated CITATION.cff
        return save_yaml_file(
            citation_cff_path,
            citation_data,
            schema_comment="# yaml-language-server: $schema=https://citation-file-format.github.io/1.2.0/schema.json",
        )

    except Exception:
        logger.exception("Unexpected error in update_citation")
        return False


if __name__ == "__main__":
    success = update_citation()
    sys.exit(0 if success else 1)
