"""
Updates book-version and date-modified in metadata.yml based on git tag.
"""

import logging
import os
import sys
from datetime import datetime

from .utils import get_file_path, load_yaml_file, save_yaml_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def update_version_from_tag():
    """
    Updates book-version and date-modified in metadata.yml from git tag.

    Expects the version to be passed via environment variable TAG_VERSION.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Get version from environment variable (set by GitHub Actions)
        version = os.environ.get("TAG_VERSION")
        if not version:
            logging.info("No TAG_VERSION environment variable found - skipping version update")
            return True

        logging.info(f"Updating metadata for version: {version}")

        # Get file path
        try:
            repo_root = get_file_path("")
            metadata_path = get_file_path("metadata.yml", repo_root)
        except Exception as e:
            logging.error(f"Failed to resolve file paths: {str(e)}")
            return False

        # Load metadata.yml
        metadata = load_yaml_file(metadata_path)
        if not metadata:
            logging.error("Could not load metadata.yml")
            return False

        # Track if updates were made
        updates_made = False

        # Update book-version
        current_version = metadata.get("book-version")
        if current_version != version:
            metadata["book-version"] = version
            updates_made = True
            logging.info(f"Updated book-version from '{current_version}' to '{version}'")
        else:
            logging.info(f"book-version already matches tag version: {version}")

        # Update date-modified
        current_date = datetime.now().strftime("%Y-%m-%d")
        old_date = metadata.get("date-modified")
        if old_date != current_date:
            metadata["date-modified"] = current_date
            updates_made = True
            logging.info(f"Updated date-modified from '{old_date}' to '{current_date}'")
        else:
            logging.info(f"date-modified already current: {current_date}")

        # Save if updates were made
        if updates_made:
            success = save_yaml_file(
                metadata_path,
                metadata,
                schema_comment="# yaml-language-server: $schema=https://quadriga-dk.github.io/quadriga-schema/v1.0.0/schema.json",
            )
            if success:
                logging.info("Successfully updated metadata.yml")
            return success
        else:
            logging.info("No updates needed")
            return True

    except Exception as e:
        logging.exception(f"Unexpected error in update_version_from_tag: {str(e)}")
        return False


if __name__ == "__main__":
    success = update_version_from_tag()
    sys.exit(0 if success else 1)
