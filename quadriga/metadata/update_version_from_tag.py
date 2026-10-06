"""Update version and dateModified in quadriga-metadata.yml based on git tag."""

import logging
import os
import sys
from datetime import UTC, datetime

from .utils import METADATA_FILENAME, SCHEMA_COMMENT, get_file_path, load_yaml_file, save_yaml_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def update_version_from_tag() -> bool:
    """
    Update book and dateModified in quadriga-metadata.yml from git tag.

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
            metadata_path = get_file_path(METADATA_FILENAME, repo_root)
        except Exception:
            logger.exception("Failed to resolve file paths")
            return False

        # Load quadriga-metadata.yml
        metadata = load_yaml_file(metadata_path)
        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load %s or invalid format", METADATA_FILENAME)
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

        # Update dateModified
        current_date = datetime.now(UTC).strftime("%Y-%m-%d")
        old_date = metadata.get("dateModified")
        if old_date != current_date:
            metadata["dateModified"] = current_date
            updates_made = True
            logger.info("Updated dateModified from '%s' to '%s'", old_date, current_date)
        else:
            logger.info("dateModified already current: %s", current_date)

        # Save if updates were made
        if updates_made:
            success = save_yaml_file(
                metadata_path,
                metadata,
                schema_comment=SCHEMA_COMMENT,
            )
            if success:
                logger.info("Successfully updated %s", METADATA_FILENAME)
            return success
        logger.info("No updates needed")
        return True

    except Exception:
        logger.exception("Unexpected error in update_version_from_tag")
        return False


if __name__ == "__main__":
    success = update_version_from_tag()
    sys.exit(0 if success else 1)
