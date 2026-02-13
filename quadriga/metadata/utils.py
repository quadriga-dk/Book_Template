"""
Common utility functions for metadata management in the Quadriga Book Template.

This module provides reused functionality across different metadata scripts.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---- File Path Handling ----


def get_repo_root() -> Path:
    """
    Get the path to the repository root, assuming this module is in quadriga/metadata/.

    Returns
    -------
        Path: Absolute path to the repository root

    Raises
    ------
        FileNotFoundError: If the repository structure is not as expected
    """
    try:
        quadriga_metadata_dir = Path(__file__).resolve().parent
        quadriga_dir = quadriga_metadata_dir.parent
        repo_root = quadriga_dir.parent

        # Verify the path looks like a repository root
        required_files = ["_config.yml", "_toc.yml"]
        found_files = [f for f in required_files if (repo_root / f).exists()]

        if len(found_files) < 1:
            msg = (
                f"Repository root at {repo_root} doesn't contain expected files "
                "(_config.yml or _toc.yml)"
            )
            raise FileNotFoundError(msg)
    except Exception:
        logger.exception("Error resolving repository root")
        raise
    else:
        return repo_root


def get_file_path(relative_path: str | Path, repo_root: Path | None = None) -> Path:
    """
    Get the absolute path to a file in the repository.

    Args:
        relative_path (str | Path): Relative path from the repository root
        repo_root (Path, optional): Repository root path. If None, it will be determined

    Returns
    -------
        Path: Absolute path to the file
    """
    if repo_root is None:
        repo_root = get_repo_root()
    return repo_root / Path(relative_path)


# ---- YAML Handling ----


def load_yaml_file(file_path: str | Path) -> dict | list | None:
    """
    Load a YAML file and return its contents as a Python object.

    Args:
        file_path (str | Path): Path to the YAML file

    Returns
    -------
        dict/list: Contents of the YAML file, or None if an error occurs
    """
    # Convert to Path at the edge
    path = Path(file_path)

    try:
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file)
            # yaml.safe_load returns Any; ensure it's dict or list
            if isinstance(data, (dict, list)):
                return data
            return None
    except FileNotFoundError:
        logger.exception("File not found: %s", path.name)
        return None
    except yaml.YAMLError:
        logger.exception("YAML parsing error in %s", path.name)
        return None
    except Exception:
        logger.exception("Error loading %s", path.name)
        return None


def save_yaml_file(
    file_path: str | Path, data: dict | list, schema_comment: str | None = None
) -> bool:
    """
    Save Python object as YAML to the specified file.

    Args:
        file_path (str | Path): Path where the YAML file should be saved
        data (dict/list): Data to save
        schema_comment (str, optional): Schema comment to add at the start of the file
                                        e.g. "# yaml-language-server: $schema=https://quadriga-dk.github.io/quadriga-schema/latest/schema.json"

    Returns
    -------
        bool: True if successful, False otherwise
    """
    # Convert to Path at the edge
    path = Path(file_path)

    try:
        # Create directories if they don't exist
        directory = path.parent
        if not directory.exists():
            directory.mkdir(parents=True)
            logger.info("Created directory: %s", directory)

        with path.open("w", encoding="utf-8") as file:
            yaml.dump(
                data,
                file,
                sort_keys=False,
                default_flow_style=False,
                allow_unicode=True,
            )

        if schema_comment:
            try:
                with path.open("r+", encoding="utf-8") as file:
                    content = file.read()
                    file.seek(0, 0)
                    file.write(f"{schema_comment}\n" + content)
            except Exception:
                logger.exception("Failed to add schema comment to %s", path.name)
                # Not a critical error, proceed
    except yaml.YAMLError:
        logger.exception("YAML encoding error for %s", path.name)
        return False
    except PermissionError:
        logger.exception("Permission denied when saving %s", path.name)
        return False
    except Exception:
        logger.exception("Error saving to %s", path.name)
        return False
    else:
        logger.info("Successfully updated %s", path.name)
        return True


# ---- Markdown and Jupyter Content Handling ----


def remove_yaml_frontmatter(text: str) -> str:
    """
    Remove YAML frontmatter from markdown content.

    YAML frontmatter is expected to be at the beginning of the file
    and delimited by triple dashes (---) on their own lines.

    Args:
        text (str): Markdown content that may contain frontmatter

    Returns
    -------
        str: Content with frontmatter removed
    """
    pattern = r"^\s*---\s*\n(.*?)\n\s*---\s*(\n|$)"
    return re.sub(pattern, "", text, count=1, flags=re.DOTALL)


def extract_first_heading(file_path: str | Path) -> str:
    """
    Extract the first heading from a markdown or jupyter notebook file.

    Args:
        file_path (str | Path): Path to the file

    Returns
    -------
        str: The content of the first heading or filename if no heading found
    """
    # Convert to Path at the edge
    file_path_obj = Path(file_path)
    try:
        if file_path_obj.suffix == ".ipynb":
            try:
                with file_path_obj.open(encoding="utf-8") as file:
                    notebook = json.load(file)

                for cell in notebook.get("cells", []):
                    if cell.get("cell_type") == "markdown":
                        content = "".join(cell.get("source", []))
                        heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                        if heading_match:
                            return heading_match.group(1).strip()
            except json.JSONDecodeError:
                logger.exception("Invalid JSON in notebook %s", file_path_obj.name)
            except Exception:
                logger.exception("Error reading notebook %s", file_path_obj.name)

        elif file_path_obj.suffix == ".md":
            try:
                with file_path_obj.open(encoding="utf-8") as file:
                    content = file.read()

                content = remove_yaml_frontmatter(content)
                heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if heading_match:
                    return heading_match.group(1).strip()
            except Exception:
                logger.exception("Error reading markdown %s", file_path_obj.name)
        else:
            logger.warning("Unsupported file type for heading extraction: %s", file_path_obj.name)
            return file_path_obj.stem

    except FileNotFoundError:
        logger.exception("File not found: %s", file_path_obj.name)
    except Exception:
        logger.exception("Error processing %s", file_path_obj.name)

    return file_path_obj.stem


# ---- Citation Handling ----


def format_authors_for_bibtex(authors: list) -> str:
    """
    Format a list of authors in the proper BibTeX format.

    Args:
        authors (list): List of author dictionaries with 'given-names' and 'family-names'

    Returns
    -------
        str: Authors formatted for BibTeX
    """
    try:
        if not authors:
            logger.warning("No authors provided to format_authors_for_bibtex")
            return ""

        formatted_authors = []
        for i, author in enumerate(authors):
            if not isinstance(author, dict):
                logger.warning("Author at index %s is not a dictionary: %s", i, author)
                continue

            family = author.get("family-names", "")
            given = author.get("given-names", "")

            if not family and not given:
                logger.warning("Author at index %s is missing both family-names and given-names", i)
                continue

            formatted_authors.append(f"{family}, {given}")

        return " and ".join(formatted_authors)
    except Exception:
        logger.exception("Error formatting authors for BibTeX")
        return ""


def generate_citation_key(authors: list, title: str, year: str) -> str:
    """
    Generate a citation key for BibTeX.

    Args:
        authors (list): List of author dictionaries
        title (str): Title of the work
        year (str): Year of publication

    Returns
    -------
        str: Citation key
    """
    try:
        # Get the first author's family name or use 'Unknown'
        if authors and isinstance(authors, list) and authors[0]:
            first_author = authors[0]
            family_name = first_author.get("family-names", "Unknown")
        else:
            family_name = "Unknown"
            logger.warning("No valid authors provided for citation key generation")

        # Get the first word of the title or use 'Untitled'
        if title and isinstance(title, str):
            title_words = title.split()
            first_word = title_words[0] if title_words else "Untitled"
        else:
            first_word = "Untitled"
            logger.warning("No valid title provided for citation key generation")

        # Use the year or empty string
        if not year:
            logger.warning("No year provided for citation key generation")
            year = ""

        # Create a citation key with no invalid characters
        raw_key = f"{family_name}_{first_word}_{year}"

        # Clean the key - remove special characters
        clean_key = re.sub(r"[^a-zA-Z0-9_]", "", raw_key)
    except Exception:
        logger.exception("Error generating citation key")
        return "Unknown_Citation_Error"
    else:
        return clean_key or "Unknown_Citation"


# ---- Keyword Handling ----


def extract_keywords(keywords_data: list | None) -> list:
    """
    Extract keywords from various formats.

    Supports:
    1. Simple list of strings: ["keyword1", "keyword2"]
    2. List of dictionaries with language codes: [{"de": "Keyword1"}, {"en": "Keyword2"}]
    3. Mixed list: ["keyword1", {"de": "Keyword2"}, "keyword3", {"en": "Keyword4"}]

    Args:
        keywords_data: Keywords in various formats

    Returns
    -------
        list: List of keyword strings
    """
    if not keywords_data:
        return []

    keywords = []
    for item in keywords_data:
        if isinstance(item, str):
            # Simple string format
            keywords.append(item)
        elif isinstance(item, dict):
            # Dictionary format with language codes
            # Extract all values from the dictionary (should be only one per item)
            keywords.extend(str(keyword) for keyword in item.values() if keyword)
        else:
            logger.warning("Unexpected keyword format: %s", item)

    return keywords
