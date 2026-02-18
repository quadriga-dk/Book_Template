"""Update version and date-modified in metadata.yml based on git tag."""

import logging
import os
import sys
from datetime import UTC, datetime

from .utils import get_file_path, load_yaml_file, save_yaml_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def update_version_from_tag() -> bool:
    """
    Update book and date-modified in metadata.yml from git tag.

    Expects the version to be passed via environment variable TAG_VERSION.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Get version from environment variable (set by GitHub Actions)
        version = os.environ.get("TAG_VERSION")
        if not version:
            logger.info("No TAG_VERSION environment variable found - skipping version update")
            return True

        logger.info("Updating metadata for version: %s", version)

        # Get file path
        try:
            repo_root = get_file_path("")
            metadata_path = get_file_path("metadata.yml", repo_root)
        except Exception:
            logger.exception("Failed to resolve file paths")
            return False

        # Load metadata.yml
        metadata = load_yaml_file(metadata_path)
        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load metadata.yml or invalid format")
            return False

        # Track if updates were made
        updates_made = False

        # Update version
        current_version = metadata.get("version")
        if current_version != version:
            metadata["version"] = version
            updates_made = True
            logger.info("Updated version from '%s' to '%s'", current_version, version)
        else:
            logger.info("version already matches tag version: %s", version)

        # Update date-modified
        current_date = datetime.now(UTC).strftime("%Y-%m-%d")
        old_date = metadata.get("date-modified")
        if old_date != current_date:
            metadata["date-modified"] = current_date
            updates_made = True
            logger.info("Updated date-modified from '%s' to '%s'", old_date, current_date)
        else:
            logger.info("date-modified already current: %s", current_date)

        # Save if updates were made
        if updates_made:
            success = save_yaml_file(
                metadata_path,
                metadata,
                schema_comment="# yaml-language-server: $schema=https://quadriga-dk.github.io/quadriga-schema/v1.0.0/schema.json",
            )
            if success:
                logger.info("Successfully updated metadata.yml")
            return success
        logger.info("No updates needed")
        return True

    except Exception:
        logger.exception("Unexpected error in update_version_from_tag")
        return False


if __name__ == "__main__":
    success = update_version_from_tag()
    sys.exit(0 if success else 1)
