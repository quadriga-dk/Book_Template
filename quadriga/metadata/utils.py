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
            msg = f"Repository root at {repo_root} doesn't contain expected files (_config.yml or _toc.yml)"
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


def iter_toc_files(node: dict | list):
    """Yield all 'file' path strings from a parsed _toc.yml, at any nesting depth.

    _toc.yml entries can be deeply nested under chapters, sections, and parts.
    This walks the entire tree and yields each file path in document order.

    Example — given::

        chapters:
          - file: einstieg/toc
            sections:
              - file: einstieg/Lernziele

    Yields: ``"einstieg/toc"``, ``"einstieg/Lernziele"``
    """
    if isinstance(node, dict):
        if "file" in node:
            yield node["file"]
        for v in node.values():
            yield from iter_toc_files(v)
    elif isinstance(node, list):
        for item in node:
            yield from iter_toc_files(item)


def resolve_toc_file(file_str: str, repo_root: Path | None = None) -> Path:
    """Resolve a _toc.yml 'file' entry to an absolute path.

    _toc.yml entries usually omit the file extension, and the file names may
    contain dots (e.g. "1_einstieg/1.0_einleitung"), so the extension must be
    appended — Path.with_suffix would truncate the name at the last dot and
    turn "1_einstieg/1.0_einleitung" into "1_einstieg/1.md".

    Args:
        file_str (str): The 'file' value from _toc.yml
        repo_root (Path, optional): Repository root path. If None, it will be determined

    Returns
    -------
        Path: Absolute path to the file. If no existing file is found, the
              path with ".md" appended is returned so callers can report a
              sensible missing path.
    """
    path = get_file_path(file_str, repo_root)

    # Entry already carries an explicit extension
    if path.suffix in {".md", ".ipynb"}:
        return path

    for ext in (".md", ".ipynb"):
        candidate = path.with_name(path.name + ext)
        if candidate.exists():
            return candidate

    return path.with_name(path.name + ".md")


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


def save_yaml_file(file_path: str | Path, data: dict | list, schema_comment: str | None = None) -> bool:
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


# ---- Identifier Handling ----


def clean_doi(doi_string: str | None) -> str | None:
    """
    Extract DOI identifier from a DOI string or URL.

    Args:
        doi_string (str): DOI string which may include URL prefix

    Returns
    -------
        str: Clean DOI identifier (e.g., "10.5281/zenodo.14970672")
    """
    if not doi_string:
        return None

    # Remove common DOI URL prefixes
    doi = str(doi_string)
    prefixes = ["https://doi.org/", "http://doi.org/", "doi:"]
    for prefix in prefixes:
        if doi.startswith(prefix):
            doi = doi[len(prefix) :]
            break

    return doi.strip()


def clean_orcid(orcid_string: str | None) -> str | None:
    """
    Extract ORCID identifier from an ORCID string or URL.

    Args:
        orcid_string (str): ORCID string which may include URL prefix

    Returns
    -------
        str: Clean ORCID identifier (e.g., "0000-0002-1602-6032")
    """
    if not orcid_string:
        return None

    # Remove common ORCID URL prefixes
    orcid = str(orcid_string)
    prefixes = ["https://orcid.org/", "http://orcid.org/", "orcid:"]
    for prefix in prefixes:
        if orcid.startswith(prefix):
            orcid = orcid[len(prefix) :]
            break

    return orcid.strip()


# ---- Metadata Field Derivation ----
#
# metadata.yml is the single source of truth. These helpers derive common
# fields from it so every output format (CFF, BibTeX, Zenodo, JSON-LD, RDF)
# interprets the metadata identically.

# ISO 639-1 (two-letter) to ISO 639-3 (three-letter) codes for languages
# likely to appear in QUADRIGA OERs. Zenodo and CFF citations use ISO 639-3.
ISO_639_1_TO_3 = {
    "de": "deu",
    "en": "eng",
    "es": "spa",
    "fr": "fra",
    "it": "ita",
    "nl": "nld",
    "pl": "pol",
    "pt": "por",
    "ru": "rus",
}


def get_doi(metadata: dict) -> str | None:
    """
    Get the clean DOI from the 'identifier' field of metadata.yml.

    Returns None if the identifier is missing, not a DOI, or a placeholder.
    As long as no real DOI has been assigned yet, the identifier should hold
    a sentinel containing "TODO" (e.g. "https://doi.org/10.5281/zenodo.TODOTODO")
    rather than a DOI that belongs to another object; the DOI is then simply
    omitted from all generated outputs.

    Args:
        metadata (dict): Parsed metadata.yml data

    Returns
    -------
        str: Clean DOI identifier (e.g., "10.5281/zenodo.14970672") or None
    """
    doi = clean_doi(metadata.get("identifier"))
    if doi and doi.startswith("10.") and "TODO" not in doi:
        return doi
    return None


def get_publication_date(metadata: dict) -> str | None:
    """
    Get the publication date (ISO string) from metadata.yml.

    Prefers 'date-modified' over 'date-issued' so re-releases carry
    their current date.

    Args:
        metadata (dict): Parsed metadata.yml data

    Returns
    -------
        str: ISO date string (e.g., "2026-06-26") or None
    """
    for field in ("date-modified", "date-issued"):
        value = metadata.get(field)
        if value:
            # YAML may parse dates as date objects or leave them as strings
            return value.isoformat() if hasattr(value, "isoformat") else str(value)
    return None


def get_publication_year(metadata: dict) -> str | None:
    """
    Get the publication year from metadata.yml (see get_publication_date).

    Args:
        metadata (dict): Parsed metadata.yml data

    Returns
    -------
        str: Four-digit year (e.g., "2026") or None
    """
    year_digits = 4
    date = get_publication_date(metadata)
    if date and len(date) >= year_digits:
        return date[:year_digits]
    return None


def get_languages(metadata: dict) -> list[str]:
    """
    Get the languages from metadata.yml as ISO 639-3 codes.

    The 'language' field may be a single code or a list; two-letter
    ISO 639-1 codes are converted to their three-letter equivalents.

    Args:
        metadata (dict): Parsed metadata.yml data

    Returns
    -------
        list: ISO 639-3 language codes (e.g., ["deu"])
    """
    value = metadata.get("language")
    if not value:
        return []
    codes = value if isinstance(value, list) else [value]
    return [ISO_639_1_TO_3.get(str(code).lower(), str(code)) for code in codes]


def get_content_license(metadata: dict) -> str | None:
    """
    Get the content license identifier (e.g., "CC-BY-4.0") from metadata.yml.

    The 'license' field may be a plain string or a dict with 'content' and
    'code' licenses; the content license is the relevant one for citations.
    The content license itself may be a string, a list, or a dict with
    'name' and 'url'.

    Args:
        metadata (dict): Parsed metadata.yml data

    Returns
    -------
        str: License identifier or None
    """
    license_data = metadata.get("license")
    if isinstance(license_data, str):
        return license_data
    if isinstance(license_data, dict) and "content" in license_data:
        content = license_data["content"]
        if isinstance(content, str):
            return content
        if isinstance(content, dict) and "name" in content:
            return str(content["name"])
        if isinstance(content, list) and content:
            return str(content[0])
    return None


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
