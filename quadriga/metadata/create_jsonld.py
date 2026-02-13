"""
Creates a JSON-LD file from metadata.yml using QUADRIGA schema x-mappings.

This script reads metadata from 'metadata.yml' and transforms it into JSON-LD
format using the x-mappings defined in the QUADRIGA schema. The output follows
Schema.org, Dublin Core, LRMI, and other standard vocabularies.

The JSON-LD file provides machine-readable linked data that can be consumed by
search engines, digital repositories, and other semantic web applications.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

from .utils import extract_keywords, get_file_path, get_repo_root, load_yaml_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def build_jsonld_context() -> dict[str, str]:
    """
    Build the JSON-LD @context with vocabulary namespaces.

    Returns
    -------
        dict: Context dictionary with vocabulary prefixes
    """
    return {
        "schema": "http://schema.org/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "lrmi": "http://purl.org/dcx/lrmi-terms/",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "@vocab": "http://schema.org/",
    }


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

    orcid = str(orcid_string)
    prefixes = ["https://orcid.org/", "http://orcid.org/", "orcid:"]
    for prefix in prefixes:
        if orcid.startswith(prefix):
            orcid = orcid[len(prefix) :]
            break

    return orcid.strip()


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

    doi = str(doi_string)
    prefixes = ["https://doi.org/", "http://doi.org/", "doi:"]
    for prefix in prefixes:
        if doi.startswith(prefix):
            doi = doi[len(prefix) :]
            break

    return doi.strip()


def transform_person(person_data: Any) -> dict[str, Any]:
    """
    Transform author or contributor to Schema.org Person.

    Uses x-mappings:
    - author/contributor -> schema:Person
    - given-names -> schema:givenName
    - family-names -> schema:familyName
    - orcid -> schema:identifier
    - affiliation -> schema:affiliation
    - credit -> not included (no standard schema.org mapping for CRediT roles)

    Args:
        person_data (dict): Author or contributor dictionary

    Returns
    -------
        dict: Schema.org Person object
    """
    if not isinstance(person_data, dict):
        logger.warning("Invalid person data: %s", person_data)
        return {}

    person: dict[str, Any] = {"@type": "Person"}

    # given-names -> schema:givenName (exactMatch)
    if "given-names" in person_data:
        person["givenName"] = person_data["given-names"]

    # family-names -> schema:familyName (exactMatch)
    if "family-names" in person_data:
        person["familyName"] = person_data["family-names"]

    # Construct full name
    if "given-names" in person_data or "family-names" in person_data:
        given = person_data.get("given-names", "")
        family = person_data.get("family-names", "")
        person["name"] = f"{given} {family}".strip()

    # orcid -> schema:identifier (exactMatch)
    if "orcid" in person_data:
        clean_orcid_id = clean_orcid(person_data["orcid"])
        if clean_orcid_id:
            person["identifier"] = {
                "@type": "PropertyValue",
                "propertyID": "ORCID",
                "value": clean_orcid_id,
                "url": f"https://orcid.org/{clean_orcid_id}",
            }

    # affiliation -> schema:affiliation (mapped in both author and contributor)
    if "affiliation" in person_data:
        person["affiliation"] = {
            "@type": "Organization",
            "name": person_data["affiliation"],
        }

    # Note: CRediT roles (credit field) are not included in JSON-LD
    # because schema.org does not have a standard property for contributor roles
    # on Person objects within author/contributor arrays

    return person


def transform_learning_objective(objective_data: Any) -> dict[str, Any]:
    """
    Transform learning objective entry to AlignmentObject.

    Uses x-mappings:
    - learning-objective -> schema:teaches / lrmi:teaches (closeMatch)
    - competency -> maps to modalia:Skill
    - blooms-category -> part of educational alignment
    - assessment -> lrmi:assesses / schema:assesses (closeMatch)

    Args:
        objective_data (dict): Learning objective dictionary

    Returns
    -------
        dict: Schema.org AlignmentObject
    """
    if not isinstance(objective_data, dict):
        return {}

    objective = {
        "@type": "AlignmentObject",
    }

    # learning-objective text
    if "learning-objective" in objective_data:
        objective["targetName"] = objective_data["learning-objective"]

    # Add competency framework information if available
    if "competency" in objective_data:
        objective["educationalFramework"] = "QUADRIGA Competency Framework"
        objective["targetDescription"] = f"Competency: {objective_data['competency']}"

    # Add Bloom's taxonomy level if available
    if "blooms-category" in objective_data:
        if "targetDescription" in objective:
            objective["targetDescription"] += f" | Bloom's: {objective_data['blooms-category']}"
        else:
            objective["targetDescription"] = f"Bloom's: {objective_data['blooms-category']}"

    # Add data flow if available
    if "data-flow" in objective_data:
        if "targetDescription" in objective:
            objective["targetDescription"] += f" | Data Flow: {objective_data['data-flow']}"
        else:
            objective["targetDescription"] = f"Data Flow: {objective_data['data-flow']}"

    # assessment -> lrmi:assesses / schema:assesses (closeMatch)
    if "assessment" in objective_data:
        objective["lrmi:assesses"] = objective_data["assessment"]

    return objective


def transform_chapter(chapter_data: Any) -> dict[str, Any]:
    """
    Transform chapter to Schema.org/LRMI LearningResource.

    Uses x-mappings:
    - chapter -> schema:LearningResource / lrmi:LearningResource (exactMatch)
    - title -> schema:name (exactMatch)
    - description -> schema:description (exactMatch)
    - url -> schema:url (exactMatch)
    - time-required -> schema:timeRequired (exactMatch)
    - learning-goal -> schema:teaches / lrmi:teaches (closeMatch)
    - learning-objectives -> schema:teaches / lrmi:teaches (closeMatch)

    Args:
        chapter_data (dict): Chapter dictionary

    Returns
    -------
        dict: Schema.org LearningResource object
    """
    if not isinstance(chapter_data, dict):
        return {}

    chapter: dict[str, Any] = {
        "@type": "LearningResource",
    }

    # title -> schema:name (exactMatch)
    if "title" in chapter_data:
        chapter["name"] = chapter_data["title"]

    # description -> schema:description (exactMatch)
    if "description" in chapter_data:
        chapter["description"] = chapter_data["description"]

    # url -> schema:url (exactMatch)
    if "url" in chapter_data:
        chapter["url"] = chapter_data["url"]

    # time-required -> schema:timeRequired (exactMatch)
    if "time-required" in chapter_data:
        chapter["timeRequired"] = chapter_data["time-required"]

    # learning-goal -> schema:teaches / lrmi:teaches (closeMatch)
    if "learning-goal" in chapter_data:
        chapter["teaches"] = chapter_data["learning-goal"]

    # learning-objectives -> schema:teaches / lrmi:teaches (closeMatch)
    # Map to AlignmentObject for structured representation
    if chapter_data.get("learning-objectives"):
        objectives = []
        for obj in chapter_data["learning-objectives"]:
            transformed = transform_learning_objective(obj)
            if transformed and len(transformed) > 1:  # More than just @type
                objectives.append(transformed)

        if objectives:
            chapter["educationalAlignment"] = objectives

    # language -> schema:inLanguage (exactMatch)
    # Chapter-level language override (supports single language or array)
    if "language" in chapter_data:
        chapter["inLanguage"] = chapter_data["language"]

    return chapter


def transform_license(license_data: Any) -> dict | list | str | None:
    """
    Transform license information to Schema.org license.

    The QUADRIGA schema has separate licenses for code and content.
    Uses x-mappings:
    - license -> schema:license (exactMatch)

    Args:
        license_data: License dictionary or string

    Returns
    -------
        dict or list: Schema.org license representation
    """
    if not license_data:
        return None

    # Handle string license (simple case)
    if isinstance(license_data, str):
        return license_data

    # Handle complex license structure (code vs content)
    if isinstance(license_data, dict):
        licenses = []

        # Code license
        if "code" in license_data:
            code_license = {
                "@type": "CreativeWork",
                "name": "Source Code",
                "license": license_data["code"],
            }
            licenses.append(code_license)

        # Content license
        if "content" in license_data:
            content_license_data = license_data["content"]
            if isinstance(content_license_data, dict):
                content_license = {
                    "@type": "CreativeWork",
                    "name": "Content",
                }
                if "url" in content_license_data:
                    content_license["license"] = content_license_data["url"]
                # Note: licenseName is not a valid schema.org property
                # The license URL should be sufficient for identification
                licenses.append(content_license)
            elif isinstance(content_license_data, str):
                content_license = {
                    "@type": "CreativeWork",
                    "name": "Content",
                    "license": content_license_data,
                }
                licenses.append(content_license)

        return licenses if len(licenses) > 1 else licenses[0] if licenses else None

    return None


def create_jsonld() -> bool | None:
    """
    Create a metadata.jsonld file from metadata.yml using QUADRIGA schema x-mappings.

    The function reads metadata from metadata.yml and transforms it into JSON-LD
    format using the x-mappings defined in the QUADRIGA schema. The output uses
    Schema.org as the primary vocabulary, with additional terms from Dublin Core,
    LRMI (Learning Resource Metadata Initiative), and other standards.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Define file paths
        try:
            repo_root = get_repo_root()
            metadata_path = get_file_path("metadata.yml", repo_root)
            jsonld_path = get_file_path("metadata.jsonld", repo_root)
        except Exception:
            logger.exception("Failed to resolve file paths")
            return False

        # Check if metadata.yml exists
        if not Path(metadata_path).exists():
            logger.error("metadata.yml file not found at %s", metadata_path)
            return False

        # Load metadata.yml
        metadata = load_yaml_file(metadata_path)
        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load metadata.yml or invalid format. Exiting.")
            return False

        # Build JSON-LD structure
        jsonld: dict[str, Any] = {
            "@context": build_jsonld_context(),
            "@type": ["Book", "LearningResource"],
        }

        # ===== BASIC METADATA =====

        # title -> schema:name (exactMatch)
        if "title" in metadata:
            jsonld["name"] = metadata["title"]
            logger.info("Added title: %s", metadata["title"])
        else:
            logger.warning("No title found in metadata.yml")

        # description -> schema:description (exactMatch)
        if "description" in metadata:
            jsonld["description"] = metadata["description"]
            logger.info("Added description")

        # identifier (DOI) -> schema:identifier (exactMatch)
        if "identifier" in metadata:
            clean_doi_id = clean_doi(metadata["identifier"])
            if clean_doi_id:
                jsonld["identifier"] = {
                    "@type": "PropertyValue",
                    "propertyID": "DOI",
                    "value": clean_doi_id,
                    "url": metadata["identifier"],
                }
                logger.info("Added DOI identifier: %s", clean_doi_id)

        # version -> schema:version (exactMatch)
        if "version" in metadata:
            jsonld["version"] = str(metadata["version"])
            logger.info("Added version: %s", metadata["version"])

        # schema-version -> schema:schemaVersion
        if "schema-version" in metadata:
            jsonld["schemaVersion"] = str(metadata["schema-version"])
            logger.info("Added schema version: %s", metadata["schema-version"])

        # url -> schema:url (exactMatch)
        if "url" in metadata:
            jsonld["url"] = metadata["url"]
            logger.info("Added URL: %s", metadata["url"])

        # git -> schema:workExample as SoftwareSourceCode
        # codeRepository is not valid for Book type, so we link to source code as a workExample
        if "git" in metadata:
            jsonld["workExample"] = {
                "@type": "SoftwareSourceCode",
                "name": "Source Code Repository",
                "codeRepository": metadata["git"],
            }
            logger.info("Added code repository as workExample: %s", metadata["git"])

        # ===== DATES =====

        # date-issued -> schema:datePublished (exactMatch)
        if "date-issued" in metadata:
            # Handle both date objects and strings
            date_value = metadata["date-issued"]
            if hasattr(date_value, "isoformat"):
                jsonld["datePublished"] = date_value.isoformat()
            else:
                jsonld["datePublished"] = str(date_value)
            logger.info("Added datePublished: %s", jsonld["datePublished"])

        # date-modified -> schema:dateModified (exactMatch)
        if "date-modified" in metadata:
            date_value = metadata["date-modified"]
            if hasattr(date_value, "isoformat"):
                jsonld["dateModified"] = date_value.isoformat()
            else:
                jsonld["dateModified"] = str(date_value)
            logger.info("Added dateModified: %s", jsonld["dateModified"])

        # ===== PEOPLE =====

        # authors -> schema:author (exactMatch)
        if metadata.get("authors"):
            authors = []
            for author in metadata["authors"]:
                person = transform_person(author)
                if person and len(person) > 1:  # More than just @type
                    authors.append(person)
            if authors:
                jsonld["author"] = authors
                logger.info("Added %d authors", len(authors))
        else:
            logger.warning("No authors found in metadata.yml")

        # contributors -> schema:contributor (exactMatch)
        if metadata.get("contributors"):
            contributors = []
            for contributor in metadata["contributors"]:
                person = transform_person(contributor)
                if person and len(person) > 1:  # More than just @type
                    contributors.append(person)
            if contributors:
                jsonld["contributor"] = contributors
                logger.info("Added %d contributors", len(contributors))

        # ===== LANGUAGE & KEYWORDS =====

        # language -> schema:inLanguage (exactMatch)
        # Supports both single language (string) and multiple languages (array)
        if "language" in metadata:
            language_value = metadata["language"]
            # If it's already a list, use it as-is
            # If it's a single string, use it as-is (Schema.org supports both)
            jsonld["inLanguage"] = language_value
            if isinstance(language_value, list):
                logger.info("Added languages: %s", ", ".join(language_value))
            else:
                logger.info("Added language: %s", language_value)

        # keywords -> schema:keywords (exactMatch) and schema:about (closeMatch)
        if metadata.get("keywords"):
            keywords_list = extract_keywords(metadata["keywords"])
            if keywords_list:
                jsonld["keywords"] = keywords_list
                # Also add as 'about' for closeMatch mapping
                jsonld["about"] = [{"@type": "Thing", "name": kw} for kw in keywords_list]
                logger.info("Added %d keywords", len(keywords_list))

        # ===== EDUCATIONAL METADATA =====

        # discipline -> schema:about (closeMatch) and modalia:Discipline (exactMatch)
        if metadata.get("discipline"):
            if "about" not in jsonld:
                jsonld["about"] = []
            for disc in metadata["discipline"]:
                jsonld["about"].append({"@type": "Thing", "name": disc})
            logger.info("Added %d disciplines", len(metadata["discipline"]))

        # research-object-type -> schema:about (broadMatch)
        if metadata.get("research-object-type"):
            if "about" not in jsonld:
                jsonld["about"] = []
            for obj_type in metadata["research-object-type"]:
                jsonld["about"].append({"@type": "Thing", "name": obj_type})
            logger.info("Added %d research object types", len(metadata["research-object-type"]))

        # target-group -> schema:audience (closeMatch) and lrmi:educationalAudience (closeMatch)
        if metadata.get("target-group"):
            jsonld["audience"] = [
                {"@type": "Audience", "audienceType": group} for group in metadata["target-group"]
            ]
            logger.info("Added %d target groups", len(jsonld["audience"]))

        # time-required -> schema:timeRequired (exactMatch)
        if "time-required" in metadata:
            jsonld["timeRequired"] = metadata["time-required"]
            logger.info("Added time required: %s", metadata["time-required"])

        # ===== LICENSE =====

        # license -> schema:license (exactMatch)
        if "license" in metadata:
            license_data = transform_license(metadata["license"])
            if license_data:
                jsonld["license"] = license_data
                logger.info("Added license information")

        # ===== CHAPTERS (hasPart) =====

        # chapters -> schema:hasPart (closeMatch)
        if metadata.get("chapters"):
            parts = []
            for chapter in metadata["chapters"]:
                chapter_obj = transform_chapter(chapter)
                if chapter_obj and len(chapter_obj) > 1:  # More than just @type
                    parts.append(chapter_obj)
            if parts:
                jsonld["hasPart"] = parts
                logger.info("Added %d chapters", len(parts))

        # table-of-contents -> dcterms:tableOfContents (exactMatch)
        if "table-of-contents" in metadata:
            jsonld["dcterms:tableOfContents"] = metadata["table-of-contents"]
            logger.info("Added table of contents")

        # ===== ADDITIONAL METADATA =====

        # context-of-creation -> modalia:Community (closeMatch)
        if "context-of-creation" in metadata:
            jsonld["funding"] = metadata["context-of-creation"]
            logger.info("Added context of creation")

        # learning-resource-type -> schema:learningResourceType (closeMatch)
        #                        -> lrmi:learningResourceType (closeMatch)
        #                        -> dcterms:type (broadMatch)
        #                        -> dc:type (broadMatch)
        if "learning-resource-type" in metadata:
            jsonld["learningResourceType"] = metadata["learning-resource-type"]
            jsonld["lrmi:learningResourceType"] = metadata["learning-resource-type"]
            jsonld["dcterms:type"] = metadata["learning-resource-type"]
            jsonld["dc:type"] = metadata["learning-resource-type"]
            logger.info("Added learning resource type: %s", metadata["learning-resource-type"])

        # quality-assurance: not mapped to JSON-LD
        # All schema x-mappings are relatedMatch only — too loose for RDF/JSON-LD output

        # Write JSON-LD file
        try:
            with jsonld_path.open("w", encoding="utf-8") as f:
                json.dump(jsonld, f, ensure_ascii=False, indent=2)
        except OSError:
            logger.exception("Error writing to %s", jsonld_path)
            return False
        else:
            logger.info("JSON-LD metadata successfully created at %s", jsonld_path)
            return True

    except Exception:
        logger.exception("Unexpected error in create_jsonld")
        return False


if __name__ == "__main__":
    success = create_jsonld()
    sys.exit(0 if success else 1)
