"""
Generate an OERSI-compatible ``metadata.yml`` from quadriga-metadata.yml.

OERSI (Open Educational Resources Search Index, https://oersi.org) discovers
repository-hosted OER through a ``metadata.yml`` file in the repository root.
That file uses schema.org / LRMI properties as produced by the OERSI metadata
generator (https://oersi.gitlab.io/metadata-form/metadata-generator.html).

quadriga-metadata.yml remains the single source of truth. This script maps the
QUADRIGA application profile onto the OERSI properties and resolves the
controlled vocabularies:

* ``disciplineLIST``        -> ``about`` (KIM Hochschulfächersystematik)
* ``targetGroupLIST``       -> ``educationalLevel`` (KIM Bildungsstufe)
* ``learningResourceType``  -> ``learningResourceType`` (HCRT)
* ``authorLIST``            -> ``creator``
* ``contributorLIST``       -> ``contributor``
* ``identifierOER``         -> ``id`` (GitHub Pages URLs are normalised to
  the book root so the id stays stable when files or folders are renamed)

Values that are not in the mapping tables below are logged as warnings and
omitted from the generated file. Extend the mappings when a new QUADRIGA value
is introduced.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from .utils import (
    ISO_639_1_TO_3,
    METADATA_FILENAME,
    clean_orcid,
    extract_keywords,
    get_doi,
    get_file_path,
    get_repo_root,
    load_yaml_file,
    save_yaml_file,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

#: Name of the generated OERSI file (must be ``metadata.yml`` in the repo root).
OERSI_FILENAME = "metadata.yml"

#: Header written to the generated file.
GENERATED_COMMENT = (
    "# Generated from quadriga-metadata.yml by "
    "quadriga/metadata/create_oersi_metadata.py. Do not edit manually."
)

#: OERSI expects a schema.org context in every record.
SCHEMA_CONTEXT = "https://schema.org/"

#: Allowed values for ``creativeWorkStatus`` in the OERSI form.
CREATIVE_WORK_STATUSES = ("Draft", "Incomplete", "Published")

#: Languages supported by the OERSI metadata form vocabulary.
OERSI_LANGUAGES = {"de", "en", "fi", "fr", "es", "uk"}

#: ISO 639-3 -> ISO 639-1, so three-letter codes can be normalised as well.
ISO_639_3_TO_1 = {value: key for key, value in ISO_639_1_TO_3.items()}

#: QUADRIGA discipline -> KIM Hochschulfächersystematik URI.
#:
#: The Hochschulfächersystematik does not have a dedicated "Digital Humanities"
#: entry; ``n01`` (Geisteswissenschaften allgemein) is the closest match.
SUBJECT_MAPPING = {
    "verwaltungswissenschaften": "https://w3id.org/kim/hochschulfaechersystematik/n29",
    "informationswissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n06",
    "bibliothekswissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n06",
    "dokumentationswissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n037",
    "digital humanities": "https://w3id.org/kim/hochschulfaechersystematik/n01",
    "geisteswissenschaften": "https://w3id.org/kim/hochschulfaechersystematik/n1",
    "geschichtswissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n068",
    "literaturwissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n188",
    "medienwissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n302",
    "politikwissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n25",
    "rechtswissenschaft": "https://w3id.org/kim/hochschulfaechersystematik/n28",
    "sozialwissenschaften": "https://w3id.org/kim/hochschulfaechersystematik/n26",
    "wirtschaftswissenschaften": "https://w3id.org/kim/hochschulfaechersystematik/n184",
    "informatik": "https://w3id.org/kim/hochschulfaechersystematik/n079",
    "übergreifend": "https://w3id.org/kim/hochschulfaechersystematik/n0",
}

#: QUADRIGA target group -> KIM Bildungsstufe URI(s).
#:
#: KIM has no postdoc level; ``level_8`` (Promotion oder äquivalent) is the
#: highest available level and therefore used for researchers.
EDUCATIONAL_LEVEL_MAPPING = {
    "forschende (postdoc)": ["https://w3id.org/kim/educationalLevel/level_8"],
    "forschende (projektleitung)": ["https://w3id.org/kim/educationalLevel/level_8"],
    "forschende": ["https://w3id.org/kim/educationalLevel/level_8"],
    "promovierende": ["https://w3id.org/kim/educationalLevel/level_8"],
    "doktorand:innen": ["https://w3id.org/kim/educationalLevel/level_8"],
    "hochschullehrende": ["https://w3id.org/kim/educationalLevel/level_A"],
    "lehrende": ["https://w3id.org/kim/educationalLevel/level_A"],
    "studierende": ["https://w3id.org/kim/educationalLevel/level_A"],
    "bachelorstudierende": ["https://w3id.org/kim/educationalLevel/level_6"],
    "masterstudierende": ["https://w3id.org/kim/educationalLevel/level_7"],
}

#: QUADRIGA learning resource type -> HCRT URI(s).
LEARNING_RESOURCE_TYPE_MAPPING = {
    "jupyter book": ["https://w3id.org/kim/hcrt/textbook"],
    "lehrbuch": ["https://w3id.org/kim/hcrt/textbook"],
    "kurs": ["https://w3id.org/kim/hcrt/course"],
    "fallstudie": ["https://w3id.org/kim/hcrt/case_study"],
    "skript": ["https://w3id.org/kim/hcrt/script"],
    "folien": ["https://w3id.org/kim/hcrt/slide"],
    "präsentation": ["https://w3id.org/kim/hcrt/slide"],
    "video": ["https://w3id.org/kim/hcrt/video"],
    "arbeitsblatt": ["https://w3id.org/kim/hcrt/worksheet"],
    "datensatz": ["https://w3id.org/kim/hcrt/data"],
}

#: QUADRIGA affiliation -> canonical organisation name and ROR ID.
#:
#: Affiliations that are not listed here are emitted with their source name
#: only, without an ID, and a warning is logged so the mapping can be added.
AFFILIATION_MAPPING = {
    "fraunhofer-institut für offene kommunikationssysteme fokus": {
        "name": "Fraunhofer-Institut für Offene Kommunikationssysteme FOKUS",
        "id": "https://ror.org/00px80p03",
    },
    "fraunhofer fokus": {
        "name": "Fraunhofer-Institut für Offene Kommunikationssysteme FOKUS",
        "id": "https://ror.org/00px80p03",
    },
    "fachhochschule potsdam": {
        "name": "Fachhochschule Potsdam",
        "id": "https://ror.org/012m9bp23",
    },
    "humboldt-universität zu berlin": {
        "name": "Humboldt-Universität zu Berlin",
        "id": "https://ror.org/01hcx6992",
    },
    "humboldt-universität zu berlin, institut für bibliotheks- und informationswissenschaft": {
        "name": "Humboldt-Universität zu Berlin",
        "id": "https://ror.org/01hcx6992",
    },
    "universität potsdam": {
        "name": "Universität Potsdam",
        "id": "https://ror.org/03bnmw459",
    },
    "technische universität berlin": {
        "name": "Technische Universität Berlin",
        "id": "https://ror.org/03v4gjf40",
    },
    "tu berlin": {
        "name": "Technische Universität Berlin",
        "id": "https://ror.org/03v4gjf40",
    },
}

#: Common compact license identifiers -> license URLs.
LICENSE_URL_MAPPING = {
    "cc0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "cc-by-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "cc-by-sa-4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "cc-by-nd-4.0": "https://creativecommons.org/licenses/by-nd/4.0/",
    "cc-by-nc-4.0": "https://creativecommons.org/licenses/by-nc/4.0/",
    "cc-by-nc-sa-4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "cc-by-nc-nd-4.0": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
}


def _normalise(value: object) -> str:
    """Normalise a mapping key (case, surrounding and repeated whitespace)."""
    return " ".join(str(value).strip().lower().split())


def _unique(values: list[Any]) -> list[Any]:
    """Return values without duplicates while preserving their order."""
    seen: set[Any] = set()
    result: list[Any] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _normalize_oer_url(url: object) -> str:
    """
    Normalise an OER URL to the stable book root for GitHub Pages hosts.

    OERSI uses ``id`` as the identity of a resource: a changed ``id``
    surfaces the same OER as a new record in the index. Deep links into
    individual chapters change whenever files or folders are renamed, so
    GitHub Pages URLs (``*.github.io``) are reduced to scheme, host and the
    first path segment (the repository name). This matches the fallback id
    that the OERSI importer itself derives for GitHub repositories. URLs on
    other hosts are returned unchanged, because their book root cannot be
    derived reliably.

    Args:
        url: Value of ``identifierOER`` from quadriga-metadata.yml

    Returns
    -------
        str: The normalised URL, or an empty string for empty input
    """
    text = str(url or "").strip()
    if not text:
        return ""

    parsed = urlparse(text)
    host = parsed.hostname or ""
    if host != "github.io" and not host.endswith(".github.io"):
        return text

    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        # Already the site root (e.g. a user/organisation pages site).
        return text

    root = f"{parsed.scheme}://{host}/{segments[0]}/"
    if root != text:
        logger.info("Normalised OER URL '%s' to book root '%s'", text, root)
    return root


def _get_content_license_url(metadata: dict) -> str | None:
    """
    Get the content license as a URL from quadriga-metadata.yml.

    Supports the v2.0.0 shape (a plain license URL) as well as v1-shaped
    dictionaries with a ``content`` entry. Compact identifiers such as
    ``CC-BY-4.0`` are resolved through ``LICENSE_URL_MAPPING``.

    Args:
        metadata: Parsed quadriga-metadata.yml data

    Returns
    -------
        str: License URL or None if no usable license was found
    """
    license_data = metadata.get("license")

    # v2.0.0: license is a plain URL
    if isinstance(license_data, str):
        value = license_data.strip()
    elif isinstance(license_data, dict):
        content = license_data.get("content")
        if isinstance(content, str):
            value = content.strip()
        elif isinstance(content, dict):
            value = str(content.get("url") or content.get("name") or "").strip()
        elif isinstance(content, list) and content:
            value = str(content[0]).strip()
        else:
            value = ""
    else:
        value = ""

    if not value:
        return None
    if value.lower().startswith(("http://", "https://")):
        return value

    mapped = LICENSE_URL_MAPPING.get(_normalise(value))
    if mapped:
        return mapped

    logger.warning("Could not resolve license '%s' to a URL; omitting it", value)
    return None


def _get_oersi_languages(metadata: dict) -> list[str]:
    """
    Get the languages from quadriga-metadata.yml as OERSI language codes.

    Args:
        metadata: Parsed quadriga-metadata.yml data

    Returns
    -------
        list: Supported ISO 639-1 language codes (e.g. ``["de"]``)
    """
    value = metadata.get("language")
    if not value:
        return []

    codes = value if isinstance(value, list) else [value]
    languages: list[str] = []
    for code in codes:
        normalised = _normalise(code)
        normalised = ISO_639_3_TO_1.get(normalised, normalised)
        if normalised in OERSI_LANGUAGES:
            languages.append(normalised)
        else:
            logger.warning(
                "Language '%s' is not in the OERSI vocabulary (%s); omitting it",
                code,
                ", ".join(sorted(OERSI_LANGUAGES)),
            )
    return _unique(languages)


def _build_affiliation(affiliation: object) -> dict[str, Any] | None:
    """
    Convert an affiliation string to a schema.org Organization.

    Known institutions get their canonical name and ROR ID from
    ``AFFILIATION_MAPPING``. Unknown institutions keep their source name and
    are emitted without an ID.

    Args:
        affiliation: Affiliation string from quadriga-metadata.yml

    Returns
    -------
        dict: schema.org Organization or None if the affiliation is empty
    """
    name = str(affiliation or "").strip()
    if not name:
        return None

    mapped = AFFILIATION_MAPPING.get(_normalise(name))
    if mapped:
        return {
            "name": mapped["name"],
            "id": mapped["id"],
            "type": "Organization",
        }

    logger.warning("No ROR mapping for affiliation '%s'; using name only", name)
    return {"name": name, "type": "Organization"}


def _build_person(person: object) -> dict[str, Any] | None:
    """
    Convert an author or contributor to an OERSI/schema.org Person.

    Args:
        person: Author or contributor dictionary from quadriga-metadata.yml

    Returns
    -------
        dict: schema.org Person or None if no name is available
    """
    if not isinstance(person, dict):
        logger.warning("Invalid person entry: %s", person)
        return None

    given_name = str(person.get("givenName") or "").strip()
    family_name = str(person.get("familyName") or "").strip()
    if not given_name and not family_name:
        logger.warning("Person entry without givenName and familyName: %s", person)
        return None

    result: dict[str, Any] = {}
    if given_name:
        result["givenName"] = given_name
    if family_name:
        result["familyName"] = family_name
    result["name"] = f"{given_name} {family_name}".strip()

    orcid = clean_orcid(person.get("orcid"))
    if orcid:
        result["id"] = f"https://orcid.org/{orcid}"

    result["type"] = "Person"

    affiliation = _build_affiliation(person.get("affiliation"))
    if affiliation:
        result["affiliation"] = affiliation

    return result


def _build_creator_list(people: list | None, role: str) -> list[dict[str, Any]]:
    """
    Build a schema.org Person list for creators or contributors.

    Args:
        people: List of author/contributor dictionaries
        role: Role name used in log messages (e.g. "author")

    Returns
    -------
        list: schema.org Person entries
    """
    result: list[dict[str, Any]] = []
    for person in people or []:
        converted = _build_person(person)
        if converted:
            result.append(converted)
        else:
            logger.warning("Skipping invalid %s entry", role)
    return result


def _map_vocabulary(
    values: list | None,
    mapping: Mapping[str, list[str] | str],
    field_name: str,
) -> list[str]:
    """
    Map QUADRIGA labels onto OERSI vocabulary URIs.

    Args:
        values: List of values from quadriga-metadata.yml
        mapping: Mapping from normalised label to URI or list of URIs
        field_name: Field name used in log messages

    Returns
    -------
        list: Unique vocabulary URIs in input order
    """
    result: list[str] = []
    for value in values or []:
        key = _normalise(value)
        mapped = mapping.get(key)
        if not mapped:
            logger.warning("No %s mapping for '%s'; omitting it", field_name, value)
            continue
        if isinstance(mapped, str):
            result.append(mapped)
        else:
            result.extend(mapped)
    return _unique(result)


def _build_basic_fields(metadata: dict, status: str) -> dict[str, Any]:
    """Build the required OERSI fields: context, status, type, name and license."""
    title = str(metadata.get("title") or "").strip()
    if not title:
        logger.error("No title found in %s", METADATA_FILENAME)
        return {}

    oersi: dict[str, Any] = {
        "@context": SCHEMA_CONTEXT,
        "creativeWorkStatus": status,
        "type": "LearningResource",
        "name": title,
    }

    description = metadata.get("description")
    if description:
        oersi["description"] = str(description).strip()

    license_url = _get_content_license_url(metadata)
    if license_url:
        oersi["license"] = license_url
    else:
        logger.warning("No license found in %s; OERSI expects one", METADATA_FILENAME)

    # identifierOER -> id (canonical URL of the published OER); GitHub Pages
    # URLs are normalised to the book root so the id stays stable
    if metadata.get("identifierOER"):
        oersi["id"] = _normalize_oer_url(metadata["identifierOER"])
    else:
        logger.warning("No 'identifierOER' found; OERSI expects a resource URL")

    return oersi


def _add_people_and_keywords(oersi: dict[str, Any], metadata: dict) -> None:
    """Add creators, contributors, keywords and languages to the OERSI record."""
    creators = _build_creator_list(metadata.get("authorLIST"), "author")
    if creators:
        oersi["creator"] = creators
    else:
        logger.warning("No authors found in %s", METADATA_FILENAME)

    # contributorLIST -> contributor (not required by OERSI, but valid schema.org)
    contributors = _build_creator_list(metadata.get("contributorLIST"), "contributor")
    if contributors:
        oersi["contributor"] = contributors

    keywords = _unique(extract_keywords(metadata.get("keywordLIST")))
    if keywords:
        oersi["keywords"] = keywords

    languages = _get_oersi_languages(metadata)
    if languages:
        oersi["inLanguage"] = languages


def _add_vocabulary_fields(oersi: dict[str, Any], metadata: dict) -> None:
    """Add subjects, target groups, educational levels and material types."""
    # disciplineLIST -> about
    subjects = _map_vocabulary(
        metadata.get("disciplineLIST"),
        SUBJECT_MAPPING,
        "subject (discipline)",
    )
    if subjects:
        oersi["about"] = subjects

    # targetGroupLIST -> educationalLevel (KIM URIs)
    target_groups = metadata.get("targetGroupLIST") or []
    educational_levels = _map_vocabulary(
        target_groups,
        EDUCATIONAL_LEVEL_MAPPING,
        "educational level (target group)",
    )
    if educational_levels:
        oersi["educationalLevel"] = educational_levels

    # learningResourceType -> HCRT
    resource_types = _map_vocabulary(
        [metadata["learningResourceType"]] if metadata.get("learningResourceType") else None,
        LEARNING_RESOURCE_TYPE_MAPPING,
        "learning resource type",
    )
    if resource_types:
        oersi["learningResourceType"] = resource_types


def _add_optional_fields(oersi: dict[str, Any], metadata: dict) -> None:
    """Add optional schema.org properties that carry useful QUADRIGA information."""
    # OERSI's metadata profile indexes the learning resource duration as
    # schema.org 'duration'; QUADRIGA stores the same value as 'timeRequired'.
    if metadata.get("timeRequired"):
        oersi["duration"] = metadata["timeRequired"]
    if metadata.get("version"):
        oersi["version"] = str(metadata["version"])

    for source, target in (("dateIssued", "datePublished"), ("dateModified", "dateModified")):
        value = metadata.get(source)
        if value:
            oersi[target] = value.isoformat() if hasattr(value, "isoformat") else str(value)

    # Keep the DOI for consumers that read schema.org identifiers.
    doi = get_doi(metadata)
    if doi:
        oersi["identifier"] = f"https://doi.org/{doi}"


def build_oersi_metadata(metadata: dict, status: str = "Published") -> dict[str, Any]:
    """
    Build the OERSI ``metadata.yml`` data structure.

    Args:
        metadata: Parsed quadriga-metadata.yml data
        status: Value for ``creativeWorkStatus`` (Draft, Incomplete, Published)

    Returns
    -------
        dict: OERSI/schema.org metadata, or an empty dict if no title is available
    """
    oersi = _build_basic_fields(metadata, status)
    if not oersi:
        return {}

    _add_people_and_keywords(oersi, metadata)
    _add_vocabulary_fields(oersi, metadata)
    _add_optional_fields(oersi, metadata)
    return oersi


def create_oersi_metadata(
    output_path: str | Path | None = None,
    status: str = "Published",
) -> bool:
    """
    Generate the OERSI ``metadata.yml`` from quadriga-metadata.yml.

    Args:
        output_path: Optional output path. Relative paths are resolved against
                     the repository root; defaults to ``metadata.yml`` there.
        status: Value for ``creativeWorkStatus`` (Draft, Incomplete, Published)

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    if status not in CREATIVE_WORK_STATUSES:
        logger.error("Invalid creativeWorkStatus '%s'", status)
        return False

    try:
        repo_root = get_repo_root()
        metadata_path = get_file_path(METADATA_FILENAME, repo_root)
        if not metadata_path.exists():
            logger.error("%s file not found at %s", METADATA_FILENAME, metadata_path)
            return False

        metadata = load_yaml_file(metadata_path)
        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load %s or invalid format", METADATA_FILENAME)
            return False

        oersi_data = build_oersi_metadata(metadata, status=status)
        if not oersi_data:
            return False

        if output_path is None:
            oersi_path = get_file_path(OERSI_FILENAME, repo_root)
        else:
            oersi_path = Path(output_path)
            if not oersi_path.is_absolute():
                oersi_path = repo_root / oersi_path

        return save_yaml_file(oersi_path, oersi_data, schema_comment=GENERATED_COMMENT)

    except Exception:
        logger.exception("Unexpected error in create_oersi_metadata")
        return False


def main(argv: list[str] | None = None) -> int:
    """
    Command-line entry point.

    Args:
        argv: Optional argument list (defaults to ``sys.argv[1:]``)

    Returns
    -------
        int: Process exit code (0 on success, 1 on failure)
    """
    parser = argparse.ArgumentParser(
        description="Generate an OERSI-compatible metadata.yml from quadriga-metadata.yml."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output path (default: metadata.yml in the repository root).",
    )
    parser.add_argument(
        "--status",
        choices=CREATIVE_WORK_STATUSES,
        default="Published",
        help="Value for creativeWorkStatus (default: Published).",
    )
    args = parser.parse_args(argv)

    success = create_oersi_metadata(output_path=args.output, status=args.status)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
