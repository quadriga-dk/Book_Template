"""
Update the CITATION.cff file with metadata from metadata.yml.

This script reads metadata from 'metadata.yml' and updates the corresponding
fields in 'CITATION.cff'. It handles fields like title, authors, URL,
repository URL, and publication date. It also ensures that the
'preferred-citation' section, if present, is updated consistently.
"""

import logging
import sys
from pathlib import Path

from .utils import extract_keywords, get_file_path, load_yaml_file, save_yaml_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def update_citation() -> bool:
    """
    Update the CITATION.cff file using data from the metadata.yml file.

    The function performs the following steps:
    1.  Constructs absolute paths to 'metadata.yml' and 'CITATION.cff'.
    2.  Loads data from both YAML files.
    3.  Updates 'CITATION.cff' fields (title, authors, URL, repository-code,
        and publication year in preferred-citation) based on 'metadata.yml'.
    4.  For authors, it attempts to preserve existing author details in
        'CITATION.cff' if a matching author (by given and family names) is found.
    5.  Saves the updated data back to 'CITATION.cff', including a schema comment.

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

        # Check if files exist
        for path, name in [
            (metadata_path, "metadata.yml"),
            (citation_cff_path, "CITATION.cff"),
        ]:
            if not Path(path).exists():
                logger.error("Required file %s not found at %s", name, path)
                return False

        # Load metadata.yml
        metadata = load_yaml_file(metadata_path)

        # Load existing CITATION.cff
        citation_data = load_yaml_file(citation_cff_path)

        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load metadata.yml or invalid format. Exiting.")
            return False

        if not citation_data or not isinstance(citation_data, dict):
            logger.error("Could not load CITATION.cff or invalid format. Exiting.")
            return False

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

        # Update publication year based on date-modified or date-published
        # Prefer newer date-modified, if available
        year_source = None
        year_value = None

        year_digits = 4
        if "date-modified" in metadata:
            date_str = metadata["date-modified"]
            if isinstance(date_str, str) and len(date_str) >= year_digits:
                year_value = date_str[:4]
                year_source = "date-modified"
        elif "date-published" in metadata:
            date_str = metadata["date-published"]
            if isinstance(date_str, str) and len(date_str) >= year_digits:
                year_value = date_str[:4]  # Extract year from YYYY-MM-DD
                year_source = "date-published"
        if year_value and "preferred-citation" in citation_data:
            citation_data["preferred-citation"]["year"] = year_value
            updates_made = True
            logger.info("Updated publication year to: %s (from %s)", year_value, year_source)

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
