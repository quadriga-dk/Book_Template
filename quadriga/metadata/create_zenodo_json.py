"""
Creates a .zenodo.json file from metadata.yml.

metadata.yml is the single source of truth for all metadata. This script
generates a Zenodo deposit metadata file from it following the Zenodo JSON
schema.

The upload_type is set to "lesson" as specified for QUADRIGA OERs.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

from .utils import (
    clean_orcid,
    extract_keywords,
    get_content_license,
    get_file_path,
    get_languages,
    get_publication_date,
    get_repo_root,
    load_yaml_file,
)

logger = logging.getLogger(__name__)


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
        logger.warning("No authors provided to format_creators_for_zenodo")
        return []

    creators = []
    for i, author in enumerate(authors):
        if not isinstance(author, dict):
            logger.warning("Author at index %d is not a dictionary: %s", i, author)
            continue

        family = author.get("family-names", "")
        given = author.get("given-names", "")

        if not family and not given:
            logger.warning("Author at index %d is missing both family-names and given-names", i)
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


def format_contributors_for_zenodo(contributors: list | None) -> list:
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


def create_zenodo_json() -> bool | None:
    """
    Create a .zenodo.json file from metadata.yml.

    The upload_type is always set to "lesson" for QUADRIGA OERs.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Define file paths
        try:
            repo_root = get_repo_root()  # Get repo root
            metadata_path = get_file_path("metadata.yml", repo_root)
            zenodo_json_path = get_file_path(".zenodo.json", repo_root)
        except Exception:
            logger.exception("Failed to resolve file paths")
            return False

        if not metadata_path.exists():
            logger.error("metadata.yml file not found at %s", metadata_path)
            return False

        # Load metadata.yml
        metadata = load_yaml_file(metadata_path)
        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load metadata.yml or invalid format. Exiting.")
            return False

        zenodo_metadata: dict[str, Any] = {"upload_type": "lesson"}

        # title
        if "title" in metadata:
            zenodo_metadata["title"] = metadata["title"]
            logger.info("Added title: %s", metadata["title"])
        else:
            logger.error("No title found in metadata.yml")
            return False

        # creators
        if metadata.get("authors"):
            creators = format_creators_for_zenodo(metadata["authors"])
            if creators:
                zenodo_metadata["creators"] = creators
                logger.info("Added %d creators", len(creators))
            else:
                logger.error("Could not format any creators from authors")
                return False
        else:
            logger.error("No authors found in metadata.yml")
            return False

        # description
        description = "<p>" + metadata.get("description") + "</p>"

        description_base = f"""
<p>Dieses interaktive Lehrbuch kann als <a href="{metadata.get("url")}" target="_blank">Web-Version</a> verwendet, zur individuellen Anpassung heruntergeladen werden und steht darüber hinaus auch auf <a href="{metadata.get("git")}" target="_blank">GitHub</a> zur Verfügung.</p>
<p>Die QUADRIGA-OER sind nach einem einheitlichen <a href="https://quadriga-dk.github.io/Book_Template" target="_blank">Template</a> gestaltet, werden nach einem standardisierten Verfahren <a href="{metadata.get("quality-assurance").get("description", "TODO")}" target="_blank">qualitätsgeprüft</a> und mit Metadaten nach dem <a href="https://doi.org/10.5281/zenodo.18184772" target="_blank">QUADRIGA-Metadatenschema</a> ausgezeichnet.</p>
<h5>QUADRIGA Datenkompetenzzentrum</h5>
<p>QUADRIGA ist das Datenkompetenzzentrum der Wissenschaftsregion Berlin-Brandenburg. Für die beiden Anwendungsdomänen Digital Humanities und Verwaltungswissenschaft entstehen unter der Einbindung der Expertise der beiden Disziplinen Informatik und Informationswissenschaft Selbstlernangebote, die als OER in Form von Jupyter Books zur freien Nachnutzung zur Verfügung gestellt werden. Um den Forschungsprozess möglichst realistisch abzubilden, basieren die OER auf Fallstudien, denen wiederum ein eigens für das Projekt entwickeltes <a href="https://doi.org/10.5281/zenodo.14747822" target="_blank">Datenkompetenzframework</a> zugrunde liegt. Die Fallstudien nehmen drei für die Anwendungsdomänen repräsentativen Datentypen in den Blick: Bewegtes Bild, Tabelle und Text.</p>
<p>Zu den Zielgruppen von QUADRIGA zählen insbesondere promovierende und promovierte Wissenschaftler*innen der genannten Disziplinen, die den Umgang mit digitalen Daten, Methoden und Werkzeugen erlernen und weiterentwickeln wollen.</p>
<p>QUADRIGA ist eins von 11 Datenkompetenzzentren in Deutschland und wird vom <a href="https://www.bmftr.bund.de/DE/Forschung/Wissenschaftssystem/Forschungsdaten/DatenkompetenzenInDerWissenschaft/datenkompetenzeninderwissenschaft.html" target="_blank">Bundesministerium für Forschung, Technologie und Raumfahrt (BMFTR)</a> und von der Europäischen Union im Rahmen von <a href="https://next-generation-eu.europa.eu/index_de" target="_blank">NextGenerationEU</a> finanziert. Zu den Verbundpartnern zählen:
  <ul>
    <li>Universität Potsdam (Verbundkoordination) <i>(Förderkennzeichen: 16DKZ2034A)</i></li>
    <li>Filmuniversität Babelsberg KONRAD WOLF <i>(Förderkennzeichen: 16DKZ2034B)</i></li>
    <li>Fachhochschule Potsdam <i>(Förderkennzeichen: 16DKZ2034C)</i></li>
    <li>Fraunhofer FOKUS <i>(Förderkennzeichen: 16DKZ2034D)</i></li>
    <li>Freie Universität Berlin <i>(Förderkennzeichen: 16DKZ2034E)</i></li>
    <li>Technische Universität Berlin <i>(Förderkennzeichen: 16DKZ2034F)</i></li>
    <li>Gesellschaft für Informatik <i>(Förderkennzeichen: 16DKZ2034G)</i></li>
    <li>Humboldt-Universität zu Berlin <i>(Förderkennzeichen: 16DKZ2034H)</i></li>
  </ul>
</p>

<p>Mehr zum Aufbau und zur Umsetzung des Projekts können Sie im <a href="https://doi.org/10.5281/zenodo.10805015" target="_blank">Umsetzungskonzept</a> erfahren.</p>

<p>Weitere Informationen sowie Publikationen finden Sie auf der <a href="https://www.quadriga-dk.de" target="_blank">Webseite</a>, in der <a href="https://zenodo.org/communities/quadriga" target="_blank">Zenodo-Community</a> und der <a href="https://github.com/quadriga-dk" target="_blank">GitHub-Organisation</a> des Projekts.</p>
"""
        zenodo_metadata["description"] = description + description_base
        logger.info("Added description")

        # publication date
        publication_date = get_publication_date(metadata)
        if publication_date:
            zenodo_metadata["publication_date"] = publication_date
            logger.info("Added publication_date: %s", publication_date)
        else:
            logger.warning("No publication date found")

        # Note: DOI field is intentionally NOT included in .zenodo.json
        # Zenodo assigns DOIs automatically upon upload/release.
        # Including a self-referencing DOI would be circular and incorrect.

        # keywords
        if metadata.get("keywords"):
            keywords_list = extract_keywords(metadata["keywords"])
            if keywords_list:
                zenodo_metadata["keywords"] = keywords_list
                logger.info("Added %d keywords", len(keywords_list))

        # license
        license_id = get_content_license(metadata)
        if license_id:
            # Zenodo expects license IDs like "CC-BY-4.0"
            # Clean up common variations
            license_clean = str(license_id).upper().replace("_", "-").replace(" ", "-")
            zenodo_metadata["license"] = license_clean
            logger.info("Added license: %s", license_clean)

        # language (Zenodo expects ISO 639-2/3 codes, e.g. "deu")
        languages = get_languages(metadata)
        if languages:
            zenodo_metadata["language"] = languages[0]
            logger.info("Added language: %s", languages[0])

        # contributors
        if metadata.get("contributors"):
            contributors = format_contributors_for_zenodo(metadata["contributors"])
            if contributors:
                zenodo_metadata["contributors"] = contributors
                logger.info("Added %d contributors", len(contributors))

        # related_identifiers
        related_identifiers = []
        repo_url = metadata.get("git")
        if repo_url:
            related_identifiers.append({"identifier": repo_url, "relation": "isSupplementedBy", "scheme": "url"})
            logger.info("Added repository URL as related identifier")
        url = metadata.get("url")
        if url and url != repo_url:
            related_identifiers.append({"identifier": url, "relation": "isAlternateIdentifier", "scheme": "url"})
            logger.info("Added URL as related identifier")

        if related_identifiers:
            zenodo_metadata["related_identifiers"] = related_identifiers

        # community
        zenodo_metadata["communities"] = [{"identifier": "quadriga"}]
        logger.info("Added QUADRIGA community")

        # version
        if "version" in metadata:
            zenodo_metadata["version"] = str(metadata["version"])
            logger.info("Added version: %s", metadata["version"])

        # write .zenodo.json
        try:
            with zenodo_json_path.open("w", encoding="utf-8") as f:
                json.dump(zenodo_metadata, f, ensure_ascii=False, indent=2)
        except OSError:
            logger.exception("Error writing to %s", zenodo_json_path)
            return False
        else:
            logger.info("Zenodo metadata successfully created at %s", zenodo_json_path)
            return True

    except Exception:
        logger.exception("Unexpected error in create_zenodo_json")
        return False


if __name__ == "__main__":
    success = create_zenodo_json()
    sys.exit(0 if success else 1)
