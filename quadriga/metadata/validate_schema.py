"""Validate metadata.yml against the QUADRIGA JSON Schema.

This module fetches the QUADRIGA schema (and referenced sub-schemas) from the
remote URL and validates a metadata dictionary against it.  Schemas are cached
locally to avoid repeated downloads.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import urllib.request
from pathlib import Path

from quadriga.metadata.utils import get_file_path, load_yaml_file

logger = logging.getLogger(__name__)

QUADRIGA_SCHEMA_URL = (
    "https://quadriga-dk.github.io/quadriga-schema/v1.0.0/schema.json"
)

# Cache directory and max age (24 hours)
SCHEMA_CACHE_DIR = Path.cwd() / ".schema_cache"
SCHEMA_CACHE_MAX_AGE = 86400  # seconds


def _cache_path_for_url(url: str) -> Path:
    """Return a cache file path for a given URL.

    Args:
        url: URL to derive cache path from

    Returns
    -------
        Path: Path to the cached file
    """
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
    return SCHEMA_CACHE_DIR / f"{url_hash}.json"


def _fetch_json(url: str) -> dict:
    """Fetch a JSON document from a URL, using a local cache.

    Cached files are reused if they are younger than SCHEMA_CACHE_MAX_AGE.

    Args:
        url: URL to fetch

    Returns
    -------
        dict: Parsed JSON content

    Raises
    ------
        urllib.error.URLError: If the URL cannot be reached and no cache exists
        json.JSONDecodeError: If the response is not valid JSON
    """
    cache_file = _cache_path_for_url(url)

    # Use cache if fresh enough
    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < SCHEMA_CACHE_MAX_AGE:
            logger.debug("Using cached schema for %s (age: %ds)", url, int(age))
            return json.loads(cache_file.read_text(encoding="utf-8"))

    # Fetch from remote
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310
            data = json.loads(resp.read())

        # Try to write to cache (skip silently if not writable, e.g. in Docker)
        try:
            SCHEMA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.debug("Cached schema for %s", url)
        except OSError:
            logger.debug("Could not write schema cache (read-only filesystem), continuing without cache")

        return data
    except Exception:
        # Fall back to stale cache if available
        if cache_file.exists():
            logger.warning("Failed to fetch %s, using stale cache", url)
            return json.loads(cache_file.read_text(encoding="utf-8"))
        raise


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
