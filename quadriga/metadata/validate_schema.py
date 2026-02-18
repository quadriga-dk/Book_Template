"""Validate metadata.yml against the QUADRIGA JSON Schema.

This module fetches the QUADRIGA schema (and referenced sub-schemas) from the
remote URL and validates a metadata dictionary against it.
"""

from __future__ import annotations

import json
import logging
import urllib.request

from quadriga.metadata.utils import get_file_path, load_yaml_file

logger = logging.getLogger(__name__)

QUADRIGA_SCHEMA_URL = (
    "https://quadriga-dk.github.io/quadriga-schema/latest/schema.json"
)


def _fetch_json(url: str) -> dict:
    """Fetch a JSON document from a URL.

    Args:
        url: URL to fetch

    Returns
    -------
        dict: Parsed JSON content

    Raises
    ------
        urllib.error.URLError: If the URL cannot be reached
        json.JSONDecodeError: If the response is not valid JSON
    """
    with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310
        return json.loads(resp.read())


def _validate_metadata(
    metadata: dict, schema_url: str = QUADRIGA_SCHEMA_URL
) -> tuple[bool, list[str]]:
    """Validate a metadata dictionary against the QUADRIGA JSON Schema.

    Fetches the schema (and any ``$ref`` sub-schemas) fresh from the given URL.

    Args:
        metadata: Metadata dictionary (e.g. parsed from metadata.yml)
        schema_url: URL of the main QUADRIGA schema

    Returns
    -------
        tuple[bool, list[str]]: ``(True, [])`` when valid, or
        ``(False, [error_message, ...])`` when validation fails or the schema
        cannot be fetched.
    """
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError:
        logger.warning(
            "jsonschema package not installed – skipping schema validation. "
            "Install it via: pip install jsonschema"
        )
        return True, []

    try:
        logger.info("Fetching QUADRIGA schema from %s ...", schema_url)
        main_schema = _fetch_json(schema_url)
    except Exception:
        logger.exception("Failed to fetch schema from %s", schema_url)
        return False, [f"Could not fetch schema from {schema_url}"]

    def retrieve(uri: str) -> Resource:
        data = _fetch_json(uri)
        return Resource.from_contents(data, default_specification=DRAFT202012)

    try:
        registry: Registry = Registry(retrieve=retrieve)
        validator = Draft202012Validator(main_schema, registry=registry)
        errors = list(validator.iter_errors(metadata))
    except Exception:
        logger.exception("Error during schema validation")
        return False, ["Unexpected error during schema validation"]

    if errors:
        messages = []
        for err in errors:
            path = err.json_path if err.json_path != "$" else "(root)"
            messages.append(f"{path}: {err.message}")
        return False, messages

    return True, []


def validate_schema() -> bool:
    """Load metadata.yml and validate it against the QUADRIGA schema.

    Returns
    -------
        bool: True if validation passed, False otherwise.
    """
    metadata_path = get_file_path("metadata.yml")
    metadata = load_yaml_file(metadata_path)
    if metadata is None:
        logger.error("Could not load metadata.yml for validation.")
        return False

    valid, errors = _validate_metadata(metadata)
    if valid:
        logger.info("Schema validation passed.")
        return True

    logger.error("Schema validation failed with %d error(s):", len(errors))
    for i, error in enumerate(errors, 1):
        logger.error("  %d. %s", i, error)
    return False
