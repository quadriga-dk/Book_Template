"""
Creates an RDF/XML file from quadriga-metadata.yml using QUADRIGA schema x-mappings.

This script reads metadata from 'quadriga-metadata.yml' and transforms it into
RDF/XML format using the x-mappings defined in the QUADRIGA v2.0.0 schema. The
output follows Schema.org, Dublin Core, LRMI, and other standard vocabularies.

The RDF/XML file provides machine-readable linked data that can be consumed by
semantic web applications, triple stores, and other RDF-aware systems.
"""

from __future__ import annotations

import logging
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from rdflib import (  # type: ignore[import-not-found]
    RDF,
    Graph,
    Literal,
    Namespace,
    URIRef,
)
from rdflib.namespace import DCTERMS, SKOS, XSD  # type: ignore[import-not-found]

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

# Define namespaces
SCHEMA = Namespace("http://schema.org/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
LRMI = Namespace("http://purl.org/dcx/lrmi-terms/")


def _sort_xml_element(element: ET.Element) -> None:
    """
    Recursively sort child elements for deterministic XML output.

    Sorts by tag name, then by attributes (as sorted key-value pairs),
    then by text content. This ensures identical output regardless of
    Python's hash randomization (PYTHONHASHSEED).

    Args:
        element: XML element whose children will be sorted in-place
    """
    children = list(element)
    for child in children:
        _sort_xml_element(child)
    children.sort(key=lambda e: (e.tag, sorted(e.attrib.items()), e.text or ""))
    element[:] = children


def add_person(graph: Graph, person_data: Any, base_uri: str, person_type: str, index: int) -> URIRef | None:
    """
    Add a person (author or contributor) to the RDF graph.

    Uses x-mappings:
    - authorLIST/contributorLIST -> schema:Person
    - givenName -> schema:givenName
    - familyName -> schema:familyName
    - orcid -> schema:identifier
    - affiliation -> schema:affiliation

    Args:
        graph: RDF graph to add triples to
        person_data: Author or contributor dictionary
        base_uri: Base URI for the resource
        person_type: Type of person ('author' or 'contributor')
        index: Index of the person in the list

    Returns
    -------
        URIRef: URI of the person node, or None if invalid
    """
    if not isinstance(person_data, dict):
        logger.warning("Invalid person data: %s", person_data)
        return None

    # Create person URI
    person_uri = URIRef(f"{base_uri}#{person_type}_{index}")
    graph.add((person_uri, RDF.type, SCHEMA.Person))

    # givenName -> schema:givenName (exactMatch)
    if "givenName" in person_data:
        graph.add((person_uri, SCHEMA.givenName, Literal(person_data["givenName"])))

    # familyName -> schema:familyName (exactMatch)
    if "familyName" in person_data:
        graph.add((person_uri, SCHEMA.familyName, Literal(person_data["familyName"])))

    # Construct full name
    if "givenName" in person_data or "familyName" in person_data:
        given = person_data.get("givenName", "")
        family = person_data.get("familyName", "")
        full_name = f"{given} {family}".strip()
        graph.add((person_uri, SCHEMA.name, Literal(full_name)))

    # orcid -> schema:identifier (exactMatch)
    if "orcid" in person_data:
        clean_orcid_id = clean_orcid(person_data["orcid"])
        if clean_orcid_id:
            # Create PropertyValue node for ORCID
            orcid_node = URIRef(f"{base_uri}#{person_type}_{index}_orcid")
            graph.add((orcid_node, RDF.type, SCHEMA.PropertyValue))
            graph.add((orcid_node, SCHEMA.propertyID, Literal("ORCID")))
            graph.add((orcid_node, SCHEMA.value, Literal(clean_orcid_id)))
            graph.add((orcid_node, SCHEMA.url, URIRef(f"https://orcid.org/{clean_orcid_id}")))
            graph.add((person_uri, SCHEMA.identifier, orcid_node))

    # affiliation -> schema:affiliation (mapped in both author and contributor)
    if "affiliation" in person_data:
        # Create Organization node
        org_node = URIRef(f"{base_uri}#{person_type}_{index}_org")
        graph.add((org_node, RDF.type, SCHEMA.Organization))
        graph.add((org_node, SCHEMA.name, Literal(person_data["affiliation"])))
        graph.add((person_uri, SCHEMA.affiliation, org_node))

    # Note: CRediT roles (creditLIST field) are not included in RDF
    # because schema.org does not have a standard property for contributor roles

    return person_uri


def add_learning_objective(
    graph: Graph, objective_data: Any, base_uri: str, chapter_index: int, obj_index: int
) -> URIRef | None:
    """
    Add a learning objective to the RDF graph as an AlignmentObject.

    Uses x-mappings:
    - description -> schema:teaches / lrmi:teaches (closeMatch)
    - competency -> maps to modalia:Skill
    - bloomsCategory -> part of educational alignment
    - assessment -> lrmi:assesses / schema:assesses (closeMatch)

    Args:
        graph: RDF graph to add triples to
        objective_data: Learning objective dictionary
        base_uri: Base URI for the resource
        chapter_index: Index of the chapter
        obj_index: Index of the objective

    Returns
    -------
        URIRef: URI of the alignment object node, or None if invalid
    """
    if not isinstance(objective_data, dict):
        return None

    obj_uri = URIRef(f"{base_uri}#chapter_{chapter_index}_objective_{obj_index}")
    graph.add((obj_uri, RDF.type, SCHEMA.AlignmentObject))

    # description -> learning objective text
    if "description" in objective_data:
        graph.add((obj_uri, SCHEMA.targetName, Literal(objective_data["description"])))

    # Add competency framework information
    descriptions = []
    if "competency" in objective_data:
        graph.add(
            (
                obj_uri,
                SCHEMA.educationalFramework,
                Literal("QUADRIGA Competency Framework"),
            )
        )
        descriptions.append(f"Competency: {objective_data['competency']}")

    # Add Bloom's taxonomy level
    if "bloomsCategory" in objective_data:
        descriptions.append(f"Bloom's: {objective_data['bloomsCategory']}")

    # Add data flow
    if "dataFlow" in objective_data:
        descriptions.append(f"Data Flow: {objective_data['dataFlow']}")

    # Combine descriptions
    if descriptions:
        graph.add((obj_uri, SCHEMA.targetDescription, Literal(" | ".join(descriptions))))

    # assessment -> lrmi:assesses (closeMatch)
    if "assessment" in objective_data:
        graph.add((obj_uri, LRMI.assesses, Literal(objective_data["assessment"])))

    return obj_uri


def add_chapter(graph: Graph, chapter_data: Any, base_uri: str, chapter_index: int) -> URIRef | None:
    """
    Add a chapter to the RDF graph as a LearningResource.

    Uses x-mappings:
    - chapter -> schema:LearningResource / lrmi:LearningResource (exactMatch)
    - title -> schema:name (exactMatch)
    - description -> schema:description (exactMatch)
    - url -> schema:url (exactMatch)
    - timeRequired -> schema:timeRequired (exactMatch)
    - learningGoal -> schema:teaches / lrmi:teaches (closeMatch)
    - learningObjectiveLIST -> schema:teaches / lrmi:teaches (closeMatch)

    Args:
        graph: RDF graph to add triples to
        chapter_data: Chapter dictionary
        base_uri: Base URI for the resource
        chapter_index: Index of the chapter

    Returns
    -------
        URIRef: URI of the chapter node, or None if invalid
    """
    if not isinstance(chapter_data, dict):
        return None

    chapter_uri = URIRef(f"{base_uri}#chapter_{chapter_index}")
    graph.add((chapter_uri, RDF.type, SCHEMA.LearningResource))

    # title -> schema:name (exactMatch)
    if "title" in chapter_data:
        graph.add((chapter_uri, SCHEMA.name, Literal(chapter_data["title"])))

    # description -> schema:description (exactMatch)
    if "description" in chapter_data:
        graph.add((chapter_uri, SCHEMA.description, Literal(chapter_data["description"])))

    # url -> schema:url (exactMatch)
    if "url" in chapter_data:
        graph.add((chapter_uri, SCHEMA.url, URIRef(chapter_data["url"])))

    # timeRequired -> schema:timeRequired (exactMatch)
    if "timeRequired" in chapter_data:
        graph.add((chapter_uri, SCHEMA.timeRequired, Literal(chapter_data["timeRequired"])))

    # learningGoal -> schema:teaches / lrmi:teaches (closeMatch)
    if "learningGoal" in chapter_data:
        graph.add((chapter_uri, SCHEMA.teaches, Literal(chapter_data["learningGoal"])))

    # learningObjectiveLIST -> educationalAlignment with AlignmentObject
    if chapter_data.get("learningObjectiveLIST"):
        for obj_index, obj_data in enumerate(chapter_data["learningObjectiveLIST"]):
            obj_uri = add_learning_objective(graph, obj_data, base_uri, chapter_index, obj_index)
            if obj_uri:
                graph.add((chapter_uri, SCHEMA.educationalAlignment, obj_uri))

    # language -> schema:inLanguage (exactMatch)
    if "language" in chapter_data:
        language_value = chapter_data["language"]
        if isinstance(language_value, list):
            for lang in language_value:
                graph.add((chapter_uri, SCHEMA.inLanguage, Literal(lang)))
        else:
            graph.add((chapter_uri, SCHEMA.inLanguage, Literal(language_value)))

    return chapter_uri


def create_rdfxml() -> bool | None:
    """
    Create a quadriga-metadata.rdf file from quadriga-metadata.yml using QUADRIGA
    schema x-mappings.

    The function reads metadata from quadriga-metadata.yml and transforms it into
    RDF/XML format using the x-mappings defined in the QUADRIGA v2.0.0 schema.
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
            rdf_path = get_file_path("quadriga-metadata.rdf", repo_root)
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

        # Create RDF graph
        graph = Graph()
        graph.bind("schema", SCHEMA)
        graph.bind("dc", DC)
        graph.bind("dcterms", DCTERMS)
        graph.bind("lrmi", LRMI)
        graph.bind("skos", SKOS)

        # Create base URI for the resource
        base_uri = metadata.get("identifierOER", metadata.get("identifier", "http://example.org/book"))
        if isinstance(base_uri, str) and not base_uri.startswith("http"):
            base_uri = f"http://example.org/{base_uri}"

        resource_uri = URIRef(base_uri)

        # Add types: Book and LearningResource
        graph.add((resource_uri, RDF.type, SCHEMA.Book))
        graph.add((resource_uri, RDF.type, SCHEMA.LearningResource))

        # ===== BASIC METADATA =====

        # title -> schema:name (exactMatch)
        if "title" in metadata:
            graph.add((resource_uri, SCHEMA.name, Literal(metadata["title"])))
            logger.info("Added title: %s", metadata["title"])
        else:
            logger.warning("No title found in %s", METADATA_FILENAME)

        # description -> schema:description (exactMatch)
        if "description" in metadata:
            graph.add((resource_uri, SCHEMA.description, Literal(metadata["description"])))
            logger.info("Added description")

        # identifier (DOI) -> schema:identifier (exactMatch)
        doi = get_doi(metadata)
        if doi:
            # Create PropertyValue node for DOI
            doi_node = URIRef(f"{base_uri}#doi")
            graph.add((doi_node, RDF.type, SCHEMA.PropertyValue))
            graph.add((doi_node, SCHEMA.propertyID, Literal("DOI")))
            graph.add((doi_node, SCHEMA.value, Literal(doi)))
            graph.add((doi_node, SCHEMA.url, URIRef(f"https://doi.org/{doi}")))
            graph.add((resource_uri, SCHEMA.identifier, doi_node))
            logger.info("Added DOI identifier: %s", doi)
        else:
            logger.warning("No DOI found in %s 'identifier' field", METADATA_FILENAME)

        # version -> schema:version (exactMatch)
        if "version" in metadata:
            graph.add((resource_uri, SCHEMA.version, Literal(str(metadata["version"]))))
            logger.info("Added version: %s", metadata["version"])

        # schemaVersion -> schema:schemaVersion
        if "schemaVersion" in metadata:
            graph.add((resource_uri, SCHEMA.schemaVersion, Literal(str(metadata["schemaVersion"]))))
            logger.info("Added schema version: %s", metadata["schemaVersion"])

        # identifierOER -> schema:url (exactMatch)
        if "identifierOER" in metadata:
            graph.add((resource_uri, SCHEMA.url, URIRef(metadata["identifierOER"])))
            logger.info("Added URL: %s", metadata["identifierOER"])

        # identifierGit -> schema:codeRepository as SoftwareSourceCode
        if "identifierGit" in metadata:
            repo_node = URIRef(f"{base_uri}#repository")
            graph.add((repo_node, RDF.type, SCHEMA.SoftwareSourceCode))
            graph.add((repo_node, SCHEMA.name, Literal("Source Code Repository")))
            graph.add((repo_node, SCHEMA.codeRepository, URIRef(metadata["identifierGit"])))
            graph.add((resource_uri, SCHEMA.workExample, repo_node))
            logger.info("Added code repository as workExample: %s", metadata["identifierGit"])

        # ===== DATES =====

        # dateIssued -> schema:datePublished (exactMatch)
        if "dateIssued" in metadata:
            date_value = metadata["dateIssued"]
            if hasattr(date_value, "isoformat"):
                date_str = date_value.isoformat()
            else:
                date_str = str(date_value)
            graph.add((resource_uri, SCHEMA.datePublished, Literal(date_str, datatype=XSD.date)))
            logger.info("Added datePublished: %s", date_str)

        # dateModified -> schema:dateModified (exactMatch)
        if "dateModified" in metadata:
            date_value = metadata["dateModified"]
            if hasattr(date_value, "isoformat"):
                date_str = date_value.isoformat()
            else:
                date_str = str(date_value)
            graph.add((resource_uri, SCHEMA.dateModified, Literal(date_str, datatype=XSD.date)))
            logger.info("Added dateModified: %s", date_str)

        # ===== PEOPLE =====

        # authorLIST -> schema:author (exactMatch)
        if metadata.get("authorLIST"):
            for i, author in enumerate(metadata["authorLIST"]):
                person_uri = add_person(graph, author, base_uri, "author", i)
                if person_uri:
                    graph.add((resource_uri, SCHEMA.author, person_uri))
            logger.info("Added %d authors", len(metadata["authorLIST"]))
        else:
            logger.warning("No authors found in %s", METADATA_FILENAME)

        # contributorLIST -> schema:contributor (exactMatch)
        if metadata.get("contributorLIST"):
            for i, contributor in enumerate(metadata["contributorLIST"]):
                person_uri = add_person(graph, contributor, base_uri, "contributor", i)
                if person_uri:
                    graph.add((resource_uri, SCHEMA.contributor, person_uri))
            logger.info("Added %d contributors", len(metadata["contributorLIST"]))

        # ===== LANGUAGE & KEYWORDS =====

        # language -> schema:inLanguage (exactMatch)
        if "language" in metadata:
            language_value = metadata["language"]
            if isinstance(language_value, list):
                for lang in language_value:
                    graph.add((resource_uri, SCHEMA.inLanguage, Literal(lang)))
                logger.info("Added languages: %s", ", ".join(language_value))
            else:
                graph.add((resource_uri, SCHEMA.inLanguage, Literal(language_value)))
                logger.info("Added language: %s", language_value)

        # keywordLIST -> schema:keywords (exactMatch) and schema:about (closeMatch)
        if metadata.get("keywordLIST"):
            keywords_list = extract_keywords(metadata["keywordLIST"])
            if keywords_list:
                for keyword in keywords_list:
                    graph.add((resource_uri, SCHEMA.keywords, Literal(keyword)))
                    # Also add as 'about' for closeMatch mapping
                    keyword_node = URIRef(f"{base_uri}#keyword_{keywords_list.index(keyword)}")
                    graph.add((keyword_node, RDF.type, SCHEMA.Thing))
                    graph.add((keyword_node, SCHEMA.name, Literal(keyword)))
                    graph.add((resource_uri, SCHEMA.about, keyword_node))
                logger.info("Added %d keywords", len(keywords_list))

        # ===== EDUCATIONAL METADATA =====

        # disciplineLIST -> schema:about (closeMatch)
        if metadata.get("disciplineLIST"):
            for i, disc in enumerate(metadata["disciplineLIST"]):
                disc_node = URIRef(f"{base_uri}#discipline_{i}")
                graph.add((disc_node, RDF.type, SCHEMA.Thing))
                graph.add((disc_node, SCHEMA.name, Literal(disc)))
                graph.add((resource_uri, SCHEMA.about, disc_node))
            logger.info("Added %d disciplines", len(metadata["disciplineLIST"]))

        # researchObjectTypeLIST -> schema:about (broadMatch)
        if metadata.get("researchObjectTypeLIST"):
            for i, obj_type in enumerate(metadata["researchObjectTypeLIST"]):
                obj_node = URIRef(f"{base_uri}#research_object_{i}")
                graph.add((obj_node, RDF.type, SCHEMA.Thing))
                graph.add((obj_node, SCHEMA.name, Literal(obj_type)))
                graph.add((resource_uri, SCHEMA.about, obj_node))
            logger.info("Added %d research object types", len(metadata["researchObjectTypeLIST"]))

        # targetGroupLIST -> schema:audience (closeMatch)
        if metadata.get("targetGroupLIST"):
            for i, group in enumerate(metadata["targetGroupLIST"]):
                audience_node = URIRef(f"{base_uri}#audience_{i}")
                graph.add((audience_node, RDF.type, SCHEMA.Audience))
                graph.add((audience_node, SCHEMA.audienceType, Literal(group)))
                graph.add((resource_uri, SCHEMA.audience, audience_node))
            logger.info("Added %d target groups", len(metadata["targetGroupLIST"]))

        # timeRequired -> schema:timeRequired (exactMatch)
        if "timeRequired" in metadata:
            graph.add((resource_uri, SCHEMA.timeRequired, Literal(metadata["timeRequired"])))
            logger.info("Added time required: %s", metadata["timeRequired"])

        # ===== LICENSE =====

        # license -> schema:license; licenseCode -> schema:license (code)
        licenses = []
        if metadata.get("license"):
            licenses.append(("Content", metadata["license"]))
        if metadata.get("licenseCode"):
            licenses.append(("Source Code", metadata["licenseCode"]))

        for i, (name, license_url) in enumerate(licenses):
            license_node = URIRef(f"{base_uri}#license_{i}")
            graph.add((license_node, RDF.type, SCHEMA.CreativeWork))
            graph.add((license_node, SCHEMA.name, Literal(name)))
            graph.add((license_node, SCHEMA.license, URIRef(license_url)))
            graph.add((resource_uri, SCHEMA.license, license_node))
        if licenses:
            logger.info("Added license information")

        # ===== CHAPTERS (hasPart) =====

        # chapterLIST -> schema:hasPart (closeMatch)
        if metadata.get("chapterLIST"):
            for i, chapter in enumerate(metadata["chapterLIST"]):
                chapter_uri = add_chapter(graph, chapter, base_uri, i)
                if chapter_uri:
                    graph.add((resource_uri, SCHEMA.hasPart, chapter_uri))
            logger.info("Added %d chapters", len(metadata["chapterLIST"]))

        # tableOfContents -> dcterms:tableOfContents (exactMatch)
        if "tableOfContents" in metadata:
            graph.add((resource_uri, DCTERMS.tableOfContents, Literal(metadata["tableOfContents"])))
            logger.info("Added table of contents")

        # ===== ADDITIONAL METADATA =====

        # contextOfCreation -> schema:funding (adapted mapping)
        if "contextOfCreation" in metadata:
            graph.add((resource_uri, SCHEMA.funding, Literal(metadata["contextOfCreation"])))
            logger.info("Added context of creation")

        # learningResourceType -> schema:learningResourceType (closeMatch)
        #                       -> lrmi:learningResourceType (closeMatch)
        #                       -> dcterms:type (broadMatch)
        #                       -> dc:type (broadMatch)
        if "learningResourceType" in metadata:
            lrt = Literal(metadata["learningResourceType"])
            graph.add((resource_uri, SCHEMA.learningResourceType, lrt))
            graph.add((resource_uri, LRMI.learningResourceType, lrt))
            graph.add((resource_uri, DCTERMS.type, lrt))
            graph.add((resource_uri, DC.type, lrt))
            logger.info("Added learning resource type: %s", metadata["learningResourceType"])

        # qualityAssurance: not mapped to RDF
        # All schema x-mappings are relatedMatch only — too loose for RDF/JSON-LD output

        # Serialize to RDF/XML and post-process for deterministic output.
        # rdflib's pretty-xml serializer uses Python dicts internally, so element
        # and namespace ordering varies across process invocations due to hash
        # randomization. We sort the XML elements after serialization to guarantee
        # reproducible output regardless of PYTHONHASHSEED.
        logger.info("Serializing %d triples to RDF/XML...", len(graph))

        try:
            xml_bytes = graph.serialize(format="pretty-xml", encoding="utf-8")
            xml_str = xml_bytes.decode("utf-8") if isinstance(xml_bytes, bytes) else xml_bytes

            # Register namespace prefixes so ElementTree preserves them
            for prefix, uri in [
                ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
                ("schema", str(SCHEMA)),
                ("dc", str(DC)),
                ("dcterms", str(DCTERMS)),
                ("lrmi", str(LRMI)),
                ("skos", str(SKOS)),
            ]:
                ET.register_namespace(prefix, uri)

            # Parse, sort elements recursively, and re-serialize
            root = ET.fromstring(xml_str)
            _sort_xml_element(root)
            ET.indent(root, space="  ")

            sorted_xml = ET.tostring(root, encoding="unicode", xml_declaration=True)

            with rdf_path.open("w", encoding="utf-8") as f:
                f.write(sorted_xml)
                f.write("\n")
        except OSError:
            logger.exception("Error writing to %s", rdf_path)
            return False
        else:
            logger.info("RDF/XML metadata successfully created at %s", rdf_path)
            return True

    except Exception:
        logger.exception("Unexpected error in create_rdfxml")
        return False


if __name__ == "__main__":
    success = create_rdfxml()
    sys.exit(0 if success else 1)
