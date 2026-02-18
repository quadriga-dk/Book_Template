"""
Extract the title from _config.yml and the first level of the TOC from _toc.yml.

It then uses this information to update metadata.yml. The titles for the TOC chapters are extracted
from the first heading of the corresponding files.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from .utils import (
    extract_first_heading,
    get_file_path,
    get_repo_root,
    load_yaml_file,
    save_yaml_file,
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def extract_and_update() -> bool | None:
    """
    Extract information from _config.yml and _toc.yml files and update metadata.yml.

    Returns
    -------
        bool: True if successful, False otherwise.
    """
    try:
        # Get the repository root directory
        try:
            repo_root = get_repo_root()
        except Exception:
            logger.exception("Failed to get repository root")
            return False

        # Define file paths using the get_file_path utility function
        config_path = get_file_path("_config.yml", repo_root)
        toc_path = get_file_path("_toc.yml", repo_root)
        metadata_path = get_file_path("metadata.yml", repo_root)

        # Verify files exist before loading
        for path, name in [
            (config_path, "_config.yml"),
            (toc_path, "_toc.yml"),
            (metadata_path, "metadata.yml"),
        ]:
            if not path.exists():
                logger.error("Required file %s not found at %s", name, path)
                return False

        # Load the files
        config_data = load_yaml_file(config_path)
        toc_data = load_yaml_file(toc_path)
        metadata_data = load_yaml_file(metadata_path)

        if not config_data or not isinstance(config_data, dict):
            logger.error("Could not load _config.yml or invalid format. Exiting.")
            return False
        if not toc_data or not isinstance(toc_data, dict):
            logger.error("Could not load _toc.yml or invalid format. Exiting.")
            return False
        if not metadata_data or not isinstance(metadata_data, dict):
            logger.error("Could not load metadata.yml or invalid format. Exiting.")
            return False

        # Extract information from _config.yml
        title = config_data.get("title", "")

        if not title:
            logger.warning("No title found in _config.yml")

        # Extract chapters and their titles from _toc.yml
        toc_chapters = []
        missing_files = []

        if "chapters" not in toc_data:
            logger.warning("No 'chapters' section found in _toc.yml")
        else:
            for chapter in toc_data["chapters"]:
                if "file" not in chapter:
                    logger.warning("Found chapter entry without 'file' attribute in _toc.yml")
                    continue

                try:
                    # Get the file path as a Path object
                    file_path_str = chapter["file"]
                    p = Path(file_path_str)

                    # Ensure the file has an extension (default to .md if none)
                    if p.suffix not in [".md", ".ipynb"]:
                        p = p.with_suffix(".md")

                    # Create the full path to the file
                    full_path = get_file_path(p, repo_root)

                    # Check if file exists
                    if not full_path.exists():
                        missing_files.append(str(full_path))
                        logger.warning("Chapter file not found: %s", full_path)
                        # Use filename as fallback title
                        toc_chapters.append(f"[Missing: {p.stem}]")
                        continue

                    # Extract the chapter title from the file's first heading
                    chapter_title = extract_first_heading(full_path)

                    # Add to the list of chapters
                    toc_chapters.append(chapter_title)
                except Exception:
                    logger.exception("Error processing chapter %s", chapter.get("file", "unknown"))
                    # Add a placeholder with the filename if possible
                    try:
                        toc_chapters.append(f"[Error: {p.stem}]")
                    except Exception:
                        toc_chapters.append("[Error: unknown chapter]")

        if missing_files:
            logger.warning("Missing %d chapter files", len(missing_files))

        if not toc_chapters:
            logger.warning("No chapter titles were extracted")

        # Format the TOC as a string with proper indentation and single newline between items
        toc_formatted = "- " + "\n- ".join(toc_chapters)

        # Update metadata.yml
        if metadata_data:
            try:
                # Update the title by using the data from _config.yml
                if "title" in metadata_data and title:
                    metadata_data["title"] = title

                # Update the description table of contents
                if "table-of-contents" in metadata_data:
                    metadata_data["table-of-contents"] = toc_formatted
                else:
                    logger.warning("No 'table-of-contents' field found in metadata.yml")

                # Save the updated metadata
                if save_yaml_file(
                    metadata_path,
                    metadata_data,
                    schema_comment="# yaml-language-server: $schema=https://quadriga-dk.github.io/quadriga-schema/v1.0.0/schema.json",
                ):
                    logger.info("Metadata updated successfully!")
                    return True
                logger.error("Failed to save metadata.yml")
                return False
            except Exception:
                logger.exception("Error updating metadata.yml")
                return False
        else:
            logger.error("Metadata file couldn't be loaded or is empty.")
            return False

    except Exception:
        logger.exception("Unexpected error in extract_and_update")
        return False


if __name__ == "__main__":
    success = extract_and_update()
    sys.exit(0 if success else 1)
