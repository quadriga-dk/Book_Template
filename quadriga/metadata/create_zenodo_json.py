"""
Creates a .zenodo.json file from CITATION.cff and metadata.yml.

This script reads citation data from the 'preferred-citation' section of
CITATION.cff and additional metadata from metadata.yml to generate a Zenodo
deposit metadata file following the Zenodo JSON schema.

The upload_type is set to "lesson" as specified for QUADRIGA OERs.
"""

import json
import logging
import sys
from pathlib import Path

from .utils import extract_keywords, get_file_path, get_repo_root, load_yaml_file


def clean_doi(doi_string: str) -> str | None:
    """
    Extract DOI identifier from a DOI string or URL.

    Args:
        doi_string (str): DOI string which may include URL prefix

    Returns
    -------
        str: Clean DOI identifier (e.g., "10.5281/zenodo.14970672")
    """
    if not doi_string:
        return None

    # Remove common DOI URL prefixes
    doi = str(doi_string)
    prefixes = ["https://doi.org/", "http://doi.org/", "doi:"]
    for prefix in prefixes:
        if doi.startswith(prefix):
            doi = doi[len(prefix) :]
            break

    return doi.strip()


def clean_orcid(orcid_string: str) -> str | None:
    """
    Extract ORCID identifier from an ORCID string or URL.

    Args:
        orcid_string (str): ORCID string which may include URL prefix

    Returns
    -------
        str: Clean ORCID identifier (e.g., "0000-0002-1602-6032")
    """
    if not orcid_string:
        return None

    # Remove common ORCID URL prefixes
    orcid = str(orcid_string)
    prefixes = ["https://orcid.org/", "http://orcid.org/", "orcid:"]
    for prefix in prefixes:
        if orcid.startswith(prefix):
            orcid = orcid[len(prefix) :]
            break

    return orcid.strip()


def format_creators_for_zenodo(authors: list) -> list:
    """
    Format authors list for Zenodo creators field.

    Args:
        authors (list): List of author dictionaries with 'given-names' and 'family-names'

    Returns
    -------
        list: List of creator dictionaries in Zenodo format
    """
    if not authors:
        logging.warning("No authors provided to format_creators_for_zenodo")
        return []

    creators = []
    for i, author in enumerate(authors):
        if not isinstance(author, dict):
            logging.warning(f"Author at index {i} is not a dictionary: {author}")
            continue

        family = author.get("family-names", "")
        given = author.get("given-names", "")

        if not family and not given:
            logging.warning(f"Author at index {i} is missing both family-names and given-names")
            continue

        creator = {"name": f"{family}, {given}" if family and given else (family or given)}

        # Add affiliation if present
        if author.get("affiliation"):
            creator["affiliation"] = author["affiliation"]

        # Add ORCID if present (cleaned)
        if author.get("orcid"):
            clean_orcid_id = clean_orcid(author["orcid"])
            if clean_orcid_id:
                creator["orcid"] = clean_orcid_id

        creators.append(creator)

    return creators


def format_contributors_for_zenodo(contributors):
    """
    Format contributors list for Zenodo contributors field.

    Args:
        contributors (list): List of contributor strings or dictionaries

    Returns
    -------
        list: List of contributor dictionaries in Zenodo format
    """
    if not contributors:
        return []

    formatted_contributors = []
    for contributor in contributors:
        if isinstance(contributor, str):
            # Simple string format: "Family, Given" or just a name
            formatted_contributors.append(
                {
                    "name": contributor,
                    "type": "Other",  # Default type
                }
            )
        elif isinstance(contributor, dict):
            # Dictionary format with potential additional fields
            contrib = {}

            # Try to construct name from given-names and family-names
            if "family-names" in contributor or "given-names" in contributor:
                family = contributor.get("family-names", "")
                given = contributor.get("given-names", "")
                contrib["name"] = f"{family}, {given}" if family and given else (family or given)
            elif "name" in contributor:
                contrib["name"] = contributor["name"]
            else:
                continue  # Skip if no name available

            # Add type if specified, otherwise default to "Other"
            contrib["type"] = contributor.get("type", "Other")

            # Add affiliation if present
            if "affiliation" in contributor:
                contrib["affiliation"] = contributor["affiliation"]

            # Add ORCID if present
            if "orcid" in contributor:
                clean_orcid_id = clean_orcid(contributor["orcid"])
                if clean_orcid_id:
                    contrib["orcid"] = clean_orcid_id

            formatted_contributors.append(contrib)

    return formatted_contributors


def create_zenodo_json():
    """
    Creates a .zenodo.json file from CITATION.cff and metadata.yml.

    The function reads the 'preferred-citation' section from CITATION.cff
    and combines it with data from metadata.yml to create a Zenodo-compliant
    metadata file. The upload_type is always set to "lesson" for QUADRIGA OERs.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Define file paths
        try:
            repo_root = get_repo_root()  # Get repo root
            citation_cff_path = get_file_path("CITATION.cff", repo_root)
            metadata_path = get_file_path("metadata.yml", repo_root)
            zenodo_json_path = get_file_path(".zenodo.json", repo_root)
        except Exception as e:
            logging.exception(f"Failed to resolve file paths: {e!s}")
            return False

        # Check if required files exist
        if not Path(citation_cff_path).exists():
            logging.error(f"CITATION.cff file not found at {citation_cff_path}")
            return False

        if not Path(metadata_path).exists():
            logging.error(f"metadata.yml file not found at {metadata_path}")
            return False

        # Load CITATION.cff
        citation_data = load_yaml_file(citation_cff_path)
        if not citation_data:
            logging.error("Could not load CITATION.cff. Exiting.")
            return False

        # Load metadata.yml
        metadata = load_yaml_file(metadata_path)
        if not metadata:
            logging.error("Could not load metadata.yml. Exiting.")
            return False

        # Extract data from preferred-citation or root
        if "preferred-citation" in citation_data:
            logging.info("Using 'preferred-citation' section from CITATION.cff")
            pref = citation_data.get("preferred-citation")
        else:
            logging.info("No 'preferred-citation' section found, using root data")
            pref = citation_data

        zenodo_metadata = {"upload_type": "lesson"}

        # title
        if "title" in pref:
            zenodo_metadata["title"] = pref["title"]
            logging.info(f"Added title: {pref['title']}")
        else:
            logging.error("No title found in CITATION.cff")
            return False

        # creators
        if pref.get("authors"):
            creators = format_creators_for_zenodo(pref["authors"])
            if creators:
                zenodo_metadata["creators"] = creators
                logging.info(f"Added {len(creators)} creators")
            else:
                logging.error("Could not format any creators from authors")
                return False
        else:
            logging.error("No authors found in preferred-citation")
            return False

        # description
        description = citation_data.get("abstract")
        if not description:
            description = metadata.get("description")

        if description:
            zenodo_metadata["description"] = description
            logging.info("Added description")
        else:
            logging.warning("No description/abstract found")

        # publication date
        publication_date = None
        if "date-modified" in metadata:
            # Use date-modified from metadata.yml and convert to string if needed
            date_value = metadata["date-modified"]
            # Handle both date objects and strings
            if hasattr(date_value, "isoformat"):
                # It's a date/datetime object, convert to ISO format string
                publication_date = date_value.isoformat()
            else:
                # It's already a string
                publication_date = str(date_value)
            logging.info(f"Added publication_date from metadata.yml: {publication_date}")
        elif "year" in pref:
            # Fall back to year from CITATION.cff
            year = str(pref["year"])
            # Zenodo expects ISO 8601 date format (YYYY-MM-DD)
            # We use January 1st as default when only year is provided
            publication_date = f"{year}-01-01"
            logging.info(f"Added publication_date from year (fallback): {publication_date}")
        else:
            logging.warning("No publication date or year found")
        if publication_date:
            zenodo_metadata["publication_date"] = publication_date

        # Note: DOI field is intentionally NOT included in .zenodo.json
        # Zenodo assigns DOIs automatically upon upload/release.
        # Including a self-referencing DOI would be circular and incorrect.

        # keywords
        if pref.get("keywords"):
            keywords_list = extract_keywords(pref["keywords"])
            if keywords_list:
                zenodo_metadata["keywords"] = keywords_list
                logging.info(f"Added {len(keywords_list)} keywords")

        # license
        license_id = None
        if "license" in pref:
            license_id = pref["license"]
        elif "copyright" in pref:
            license_id = pref["copyright"]
        if license_id:
            # Zenodo expects license IDs like "CC-BY-SA-4.0"
            # Clean up common variations
            license_clean = str(license_id).upper().replace("_", "-")
            zenodo_metadata["license"] = license_clean
            logging.info(f"Added license: {license_clean}")

        # language
        if pref.get("languages"):
            lang = (
                pref["languages"][0] if isinstance(pref["languages"], list) else pref["languages"]
            )
            zenodo_metadata["language"] = lang
            logging.info(f"Added language: {lang}")

        # contributors
        if metadata.get("contributors"):
            contributors = format_contributors_for_zenodo(metadata["contributors"])
            if contributors:
                zenodo_metadata["contributors"] = contributors
                logging.info(f"Added {len(contributors)} contributors")

        # related_identifiers
        related_identifiers = []
        repo_url = pref.get("repository-code")
        if repo_url:
            related_identifiers.append(
                {"identifier": repo_url, "relation": "isSupplementedBy", "scheme": "url"}
            )
            logging.info("Added repository URL as related identifier")
        url = pref.get("url")
        if url and url != repo_url:
            related_identifiers.append(
                {"identifier": url, "relation": "isAlternateIdentifier", "scheme": "url"}
            )
            logging.info("Added URL as related identifier")

        if related_identifiers:
            zenodo_metadata["related_identifiers"] = related_identifiers

        # community
        zenodo_metadata["communities"] = [{"identifier": "quadriga"}]
        logging.info("Added QUADRIGA community")

        # version
        if "version" in pref:
            zenodo_metadata["version"] = str(pref["version"])
            logging.info(f"Added version: {pref['version']}")

        # write .zenodo.json
        try:
            with zenodo_json_path.open("w", encoding="utf-8") as f:
                json.dump(zenodo_metadata, f, ensure_ascii=False, indent=2)
            logging.info(f"Zenodo metadata successfully created at {zenodo_json_path}")
            return True
        except OSError as e:
            logging.exception(f"Error writing to {zenodo_json_path}: {e}")
            return False

    except Exception as e:
        logging.exception(f"Unexpected error in create_zenodo_json: {e!s}")
        return False


if __name__ == "__main__":
    success = create_zenodo_json()
    sys.exit(0 if success else 1)
