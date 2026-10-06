"""
Creates a JSON-LD file from quadriga-metadata.yml using QUADRIGA schema x-mappings.

This script reads metadata from 'quadriga-metadata.yml' and transforms it into
JSON-LD format using the x-mappings defined in the QUADRIGA v2.0.0 schema. The
output follows Schema.org, Dublin Core, LRMI, and other standard vocabularies.

The JSON-LD file provides machine-readable linked data that can be consumed by
search engines, digital repositories, and other semantic web applications.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

from .utils import (
    METADATA_FILENAME,
    clean_orcid,
    extract_keywords,
    get_doi,
    get_file_path,
    get_repo_root,
    load_yaml_file,
)

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


def transform_person(person_data: Any) -> dict[str, Any]:
    """
    Transform author or contributor to Schema.org Person.

    Uses x-mappings:
    - authorLIST/contributorLIST -> schema:Person
    - givenName -> schema:givenName
    - familyName -> schema:familyName
    - orcid -> schema:identifier
    - affiliation -> schema:affiliation
    - creditLIST -> not included (no standard schema.org mapping for CRediT roles)

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

    # givenName -> schema:givenName (exactMatch)
    if "givenName" in person_data:
        person["givenName"] = person_data["givenName"]

    # familyName -> schema:familyName (exactMatch)
    if "familyName" in person_data:
        person["familyName"] = person_data["familyName"]

    # Construct full name
    if "givenName" in person_data or "familyName" in person_data:
        given = person_data.get("givenName", "")
        family = person_data.get("familyName", "")
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

    # Note: CRediT roles (creditLIST field) are not included in JSON-LD
    # because schema.org does not have a standard property for contributor roles
    # on Person objects within author/contributor arrays

    return person


def transform_learning_objective(objective_data: Any) -> dict[str, Any]:
    """
    Transform learning objective entry to AlignmentObject.

    Uses x-mappings:
    - description -> schema:teaches / lrmi:teaches (closeMatch)
    - competency -> maps to modalia:Skill
    - bloomsCategory -> part of educational alignment
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

    # description -> learning objective text
    if "description" in objective_data:
        objective["targetName"] = objective_data["description"]

    # Add competency framework information if available
    if "competency" in objective_data:
        objective["educationalFramework"] = "QUADRIGA Competency Framework"
        objective["targetDescription"] = f"Competency: {objective_data['competency']}"

    # Add Bloom's taxonomy level if available
    if "bloomsCategory" in objective_data:
        if "targetDescription" in objective:
            objective["targetDescription"] += f" | Bloom's: {objective_data['bloomsCategory']}"
        else:
            objective["targetDescription"] = f"Bloom's: {objective_data['bloomsCategory']}"

    # Add data flow if available
    if "dataFlow" in objective_data:
        if "targetDescription" in objective:
            objective["targetDescription"] += f" | Data Flow: {objective_data['dataFlow']}"
        else:
            objective["targetDescription"] = f"Data Flow: {objective_data['dataFlow']}"

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
    - timeRequired -> schema:timeRequired (exactMatch)
    - learningGoal -> schema:teaches / lrmi:teaches (closeMatch)
    - learningObjectiveLIST -> schema:teaches / lrmi:teaches (closeMatch)

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

    # timeRequired -> schema:timeRequired (exactMatch)
    if "timeRequired" in chapter_data:
        chapter["timeRequired"] = chapter_data["timeRequired"]

    # learningGoal -> schema:teaches / lrmi:teaches (closeMatch)
    if "learningGoal" in chapter_data:
        chapter["teaches"] = chapter_data["learningGoal"]

    # learningObjectiveLIST -> schema:teaches / lrmi:teaches (closeMatch)
    # Map to AlignmentObject for structured representation
    if chapter_data.get("learningObjectiveLIST"):
        objectives = []
        for obj in chapter_data["learningObjectiveLIST"]:
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


def transform_license(metadata: dict) -> dict | list | str | None:
    """
    Transform license information to Schema.org license.

    In schema v2.0.0 both the content license ('license') and the code
    license ('licenseCode') are plain license URLs. Uses x-mappings:
    - license -> schema:license (broadMatch)
    - licenseCode -> schema:license (broadMatch)

    Args:
        metadata: Parsed quadriga-metadata.yml data

    Returns
    -------
        str or list: Schema.org license representation or None
    """
    licenses = []

    if metadata.get("license"):
        licenses.append(
            {"@type": "CreativeWork", "name": "Content", "license": metadata["license"]}
        )

    if metadata.get("licenseCode"):
        licenses.append(
            {"@type": "CreativeWork", "name": "Source Code", "license": metadata["licenseCode"]}
        )

    if not licenses:
        return None
    return licenses[0] if len(licenses) == 1 else licenses


def create_jsonld() -> bool | None:
    """
    Create a quadriga-metadata.jsonld file from quadriga-metadata.yml using
    QUADRIGA schema x-mappings.

    The function reads metadata from quadriga-metadata.yml and transforms it into
    JSON-LD format using the x-mappings defined in the QUADRIGA v2.0.0 schema.
    The output uses Schema.org as the primary vocabulary, with additional terms
    from Dublin Core, LRMI (Learning Resource Metadata Initiative), and other
    standards.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Define file paths
        try:
            repo_root = get_repo_root()
            metadata_path = get_file_path(METADATA_FILENAME, repo_root)
            jsonld_path = get_file_path("quadriga-metadata.jsonld", repo_root)
        except Exception:
            logger.exception("Failed to resolve file paths")
            return False

        # Check if quadriga-metadata.yml exists
        if not Path(metadata_path).exists():
            logger.error("%s file not found at %s", METADATA_FILENAME, metadata_path)
            return False

        # Load quadriga-metadata.yml
        metadata = load_yaml_file(metadata_path)
        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load %s or invalid format. Exiting.", METADATA_FILENAME)
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
            logger.warning("No title found in %s", METADATA_FILENAME)

        # description -> schema:description (exactMatch)
        if "description" in metadata:
            jsonld["description"] = metadata["description"]
            logger.info("Added description")

        # identifier (DOI) -> schema:identifier (exactMatch)
        doi = get_doi(metadata)
        if doi:
            jsonld["identifier"] = {
                "@type": "PropertyValue",
                "propertyID": "DOI",
                "value": doi,
                "url": f"https://doi.org/{doi}",
            }
            logger.info("Added DOI identifier: %s", doi)
        else:
            logger.warning("No DOI found in %s 'identifier' field", METADATA_FILENAME)

        # version -> schema:version (exactMatch)
        if "version" in metadata:
            jsonld["version"] = str(metadata["version"])
            logger.info("Added version: %s", metadata["version"])

        # schemaVersion -> schema:schemaVersion
        if "schemaVersion" in metadata:
            jsonld["schemaVersion"] = str(metadata["schemaVersion"])
            logger.info("Added schema version: %s", metadata["schemaVersion"])

        # identifierOER -> schema:url (exactMatch)
        if "identifierOER" in metadata:
            jsonld["url"] = metadata["identifierOER"]
            logger.info("Added URL: %s", metadata["identifierOER"])

        # identifierGit -> schema:codeRepository as SoftwareSourceCode
        # codeRepository is not valid for Book type, so we link to source code as a workExample
        if "identifierGit" in metadata:
            jsonld["workExample"] = {
                "@type": "SoftwareSourceCode",
                "name": "Source Code Repository",
                "codeRepository": metadata["identifierGit"],
            }
            logger.info("Added code repository as workExample: %s", metadata["identifierGit"])

        # ===== DATES =====

        # dateIssued -> schema:datePublished (exactMatch)
        if "dateIssued" in metadata:
            # Handle both date objects and strings
            date_value = metadata["dateIssued"]
            if hasattr(date_value, "isoformat"):
                jsonld["datePublished"] = date_value.isoformat()
            else:
                jsonld["datePublished"] = str(date_value)
            logger.info("Added datePublished: %s", jsonld["datePublished"])

        # dateModified -> schema:dateModified (exactMatch)
        if "dateModified" in metadata:
            date_value = metadata["dateModified"]
            if hasattr(date_value, "isoformat"):
                jsonld["dateModified"] = date_value.isoformat()
            else:
                jsonld["dateModified"] = str(date_value)
            logger.info("Added dateModified: %s", jsonld["dateModified"])

        # ===== PEOPLE =====

        # authorLIST -> schema:author (exactMatch)
        if metadata.get("authorLIST"):
            authors = []
            for author in metadata["authorLIST"]:
                person = transform_person(author)
                if person and len(person) > 1:  # More than just @type
                    authors.append(person)
            if authors:
                jsonld["author"] = authors
                logger.info("Added %d authors", len(authors))
        else:
            logger.warning("No authors found in %s", METADATA_FILENAME)

        # contributorLIST -> schema:contributor (exactMatch)
        if metadata.get("contributorLIST"):
            contributors = []
            for contributor in metadata["contributorLIST"]:
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

        # keywordLIST -> schema:keywords (exactMatch) and schema:about (closeMatch)
        if metadata.get("keywordLIST"):
            keywords_list = extract_keywords(metadata["keywordLIST"])
            if keywords_list:
                jsonld["keywords"] = keywords_list
                # Also add as 'about' for closeMatch mapping
                jsonld["about"] = [{"@type": "Thing", "name": kw} for kw in keywords_list]
                logger.info("Added %d keywords", len(keywords_list))

        # ===== EDUCATIONAL METADATA =====

        # disciplineLIST -> schema:about (closeMatch) and modalia:Discipline (exactMatch)
        if metadata.get("disciplineLIST"):
            if "about" not in jsonld:
                jsonld["about"] = []
            for disc in metadata["disciplineLIST"]:
                jsonld["about"].append({"@type": "Thing", "name": disc})
            logger.info("Added %d disciplines", len(metadata["disciplineLIST"]))

        # researchObjectTypeLIST -> schema:about (broadMatch)
        if metadata.get("researchObjectTypeLIST"):
            if "about" not in jsonld:
                jsonld["about"] = []
            for obj_type in metadata["researchObjectTypeLIST"]:
                jsonld["about"].append({"@type": "Thing", "name": obj_type})
            logger.info("Added %d research object types", len(metadata["researchObjectTypeLIST"]))

        # targetGroupLIST -> schema:audience (closeMatch) and lrmi:educationalAudience (closeMatch)
        if metadata.get("targetGroupLIST"):
            jsonld["audience"] = [
                {"@type": "Audience", "audienceType": group}
                for group in metadata["targetGroupLIST"]
            ]
            logger.info("Added %d target groups", len(jsonld["audience"]))

        # timeRequired -> schema:timeRequired (exactMatch)
        if "timeRequired" in metadata:
            jsonld["timeRequired"] = metadata["timeRequired"]
            logger.info("Added time required: %s", metadata["timeRequired"])

        # ===== LICENSE =====

        # license/licenseCode -> schema:license
        license_data = transform_license(metadata)
        if license_data:
            jsonld["license"] = license_data
            logger.info("Added license information")

        # ===== CHAPTERS (hasPart) =====

        # chapterLIST -> schema:hasPart (closeMatch)
        if metadata.get("chapterLIST"):
            parts = []
            for chapter in metadata["chapterLIST"]:
                chapter_obj = transform_chapter(chapter)
                if chapter_obj and len(chapter_obj) > 1:  # More than just @type
                    parts.append(chapter_obj)
            if parts:
                jsonld["hasPart"] = parts
                logger.info("Added %d chapters", len(parts))

        # tableOfContents -> dcterms:tableOfContents (exactMatch)
        if "tableOfContents" in metadata:
            jsonld["dcterms:tableOfContents"] = metadata["tableOfContents"]
            logger.info("Added table of contents")

        # ===== ADDITIONAL METADATA =====

        # contextOfCreation -> modalia:Community (closeMatch)
        if "contextOfCreation" in metadata:
            jsonld["funding"] = metadata["contextOfCreation"]
            logger.info("Added context of creation")

        # learningResourceType -> schema:learningResourceType (closeMatch)
        #                       -> lrmi:learningResourceType (closeMatch)
        #                       -> dcterms:type (broadMatch)
        #                       -> dc:type (broadMatch)
        if "learningResourceType" in metadata:
            jsonld["learningResourceType"] = metadata["learningResourceType"]
            jsonld["lrmi:learningResourceType"] = metadata["learningResourceType"]
            jsonld["dcterms:type"] = metadata["learningResourceType"]
            jsonld["dc:type"] = metadata["learningResourceType"]
            logger.info("Added learning resource type: %s", metadata["learningResourceType"])

        # qualityAssurance: not mapped to JSON-LD
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
