"""
Injects JSON-LD structured data into generated HTML files.

This script reads the metadata.jsonld file and injects it as a
<script type="application/ld+json"> tag into the <head> section
of the generated HTML files, making the structured data discoverable
by search engines.

It injects:
- Full book metadata into index.html
- Chapter-specific metadata into each chapter's first page
"""

import json
import logging
import sys
from pathlib import Path
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def inject_jsonld_into_html(html_path: Path, jsonld_content: str) -> bool:
    """
    Inject JSON-LD script tag into an HTML file's <head> section.

    Args:
        html_path (Path): Path to the HTML file
        jsonld_content (str): JSON-LD content as a string

    Returns
    -------
        bool: True if successful, False otherwise
    """
    try:
        # Read the HTML file
        with html_path.open(encoding="utf-8") as f:
            html_content = f.read()

        # Check if JSON-LD is already present
        if '<script type="application/ld+json">' in html_content:
            logging.debug(f"JSON-LD already present in {html_path.name}, skipping")
            return True

        # Create the JSON-LD script tag with proper indentation
        jsonld_script = f'\n  <script type="application/ld+json">\n{jsonld_content}\n  </script>\n'

        # Find the </head> tag and inject before it
        if "</head>" in html_content:
            # Inject before </head>
            html_content = html_content.replace("</head>", f"{jsonld_script}</head>", 1)
        else:
            logging.warning(f"No </head> tag found in {html_path.name}, skipping")
            return False

        # Write the modified HTML back
        with html_path.open("w", encoding="utf-8") as f:
            f.write(html_content)

        logging.info(f"Injected JSON-LD into {html_path.name}")
        return True

    except FileNotFoundError:
        logging.exception(f"HTML file not found: {html_path}")
        return False
    except Exception:
        logging.exception(f"Error injecting JSON-LD into {html_path}")
        return False


def get_html_path_from_url(url: str, build_dir: Path, base_url: str = None) -> Path | None:
    """
    Extract the HTML file path from a chapter URL.

    Args:
        url (str): Full URL like "https://quadriga-dk.github.io/Book_Template/präambel/toc.html"
        build_dir (Path): Path to _build/html directory
        base_url (str, optional): Base URL to strip. If None, will be extracted from url

    Returns
    -------
        Path: Path to the HTML file, or None if invalid
    """
    try:
        parsed = urlparse(url)
        path = parsed.path

        # Remove leading slash
        path = path.removeprefix("/")

        # If base_url provided, try to extract relative path
        # e.g., from "https://quadriga-dk.github.io/Book_Template/präambel/toc.html"
        # we want "präambel/toc.html"
        parts = path.split("/")
        if len(parts) > 1:
            # Assume first part might be the repo name, try both with and without it
            relative_path = "/".join(parts[1:]) if len(parts) > 2 else path

            # Try the path with repo name removed
            html_path = build_dir / relative_path
            if html_path.exists():
                return html_path

        # Try the full path
        html_path = build_dir / path
        if html_path.exists():
            return html_path

        logging.warning(f"Could not find HTML file for URL: {url}")
        return None

    except Exception:
        logging.exception(f"Error parsing URL {url}")
        return None


def create_chapter_jsonld(chapter_data: dict, book_data: dict) -> dict:
    """
    Create chapter-specific JSON-LD from chapter data and book metadata.

    Args:
        chapter_data (dict): Chapter object from the hasPart array
        book_data (dict): Full book JSON-LD data

    Returns
    -------
        dict: Chapter-specific JSON-LD object
    """
    # Create a LearningResource for this chapter
    chapter_jsonld = {
        "@context": {
            "schema": "http://schema.org/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "lrmi": "http://purl.org/dcx/lrmi-terms/",
            "@vocab": "http://schema.org/",
        },
        "@type": "LearningResource",
    }

    # Copy chapter-specific properties
    if "name" in chapter_data:
        chapter_jsonld["name"] = chapter_data["name"]

    if "description" in chapter_data:
        chapter_jsonld["description"] = chapter_data["description"]

    if "url" in chapter_data:
        chapter_jsonld["url"] = chapter_data["url"]

    if "timeRequired" in chapter_data:
        chapter_jsonld["timeRequired"] = chapter_data["timeRequired"]

    if "teaches" in chapter_data:
        chapter_jsonld["teaches"] = chapter_data["teaches"]

    if "educationalAlignment" in chapter_data:
        chapter_jsonld["educationalAlignment"] = chapter_data["educationalAlignment"]

    # Include relevant book-level metadata
    # Authors (from book)
    if "author" in book_data:
        chapter_jsonld["author"] = book_data["author"]

    # Contributors (from book)
    if "contributor" in book_data:
        chapter_jsonld["contributor"] = book_data["contributor"]

    # Language - prefer chapter-level language if present, otherwise use book-level
    # Support both single language and multiple languages (array)
    if "inLanguage" in chapter_data:
        # Chapter has its own language specification
        chapter_jsonld["inLanguage"] = chapter_data["inLanguage"]
    elif "inLanguage" in book_data:
        # Fall back to book-level language
        chapter_jsonld["inLanguage"] = book_data["inLanguage"]

    # License (from book)
    if "license" in book_data:
        chapter_jsonld["license"] = book_data["license"]

    # Publication dates (from book)
    if "datePublished" in book_data:
        chapter_jsonld["datePublished"] = book_data["datePublished"]

    if "dateModified" in book_data:
        chapter_jsonld["dateModified"] = book_data["dateModified"]

    # Keywords/subjects from book level
    if "keywords" in book_data:
        chapter_jsonld["keywords"] = book_data["keywords"]

    # Audience (from book)
    if "audience" in book_data:
        chapter_jsonld["audience"] = book_data["audience"]

    # Funding/context (from book)
    if "funding" in book_data:
        chapter_jsonld["funding"] = book_data["funding"]

    # Add reference to parent book
    book_url = book_data.get("url", "")
    parent_ref = {"@type": "Book", "url": book_url}

    # Include book name in parent reference
    if "name" in book_data:
        parent_ref["name"] = book_data["name"]

    # Include book identifier in parent reference
    if "identifier" in book_data:
        parent_ref["identifier"] = book_data["identifier"]

    chapter_jsonld["isPartOf"] = parent_ref

    return chapter_jsonld


def inject_jsonld(build_dir: Path = None, jsonld_path: Path = None) -> bool:
    """
    Inject JSON-LD metadata into HTML files of a Jupyter Book.

    This function reads the metadata.jsonld file and injects:
    1. Full book metadata into index.html
    2. Chapter-specific metadata into each chapter's first page

    For chapters, it creates a LearningResource JSON-LD object with an
    "isPartOf" reference to the parent book, providing better structured
    data when individual chapters are shared or indexed.

    Args:
        build_dir (Path, optional): Path to the _build/html directory.
                                    If None, uses current directory's _build/html
        jsonld_path (Path, optional): Path to metadata.jsonld file.
                                      If None, uses current directory's metadata.jsonld

    Returns
    -------
        bool: True if successful, False otherwise
    """
    try:
        # Determine paths
        if build_dir is None:
            build_dir = Path.cwd() / "_build" / "html"
        if jsonld_path is None:
            jsonld_path = Path.cwd() / "metadata.jsonld"

        # Check if build directory exists
        if not build_dir.exists():
            logging.error(f"Build directory not found: {build_dir}")
            return False

        # Check if JSON-LD file exists
        if not jsonld_path.exists():
            logging.error(f"JSON-LD file not found: {jsonld_path}")
            return False

        # Read and validate JSON-LD
        try:
            with open(jsonld_path, encoding="utf-8") as f:
                jsonld_data = json.load(f)
            logging.info(f"Loaded JSON-LD from {jsonld_path}")
        except json.JSONDecodeError as e:
            logging.exception(f"Invalid JSON in {jsonld_path}: {e}")
            return False

        # Convert back to formatted JSON string with indentation
        # Indent by 4 spaces to align nicely within the script tag
        jsonld_content = json.dumps(jsonld_data, ensure_ascii=False, indent=2)
        # Add extra indentation for each line to align within the script tag
        jsonld_content = "\n".join("    " + line for line in jsonld_content.split("\n"))

        # Inject into index.html (main page)
        index_html = build_dir / "index.html"
        if index_html.exists():
            if not inject_jsonld_into_html(index_html, jsonld_content):
                logging.error("Failed to inject JSON-LD into index.html")
                return False
        else:
            logging.warning(f"index.html not found at {index_html}")
            return False

        # Inject chapter-specific metadata into each chapter page
        chapters_injected = 0
        if jsonld_data.get("hasPart"):
            logging.info(f"Processing {len(jsonld_data['hasPart'])} chapters...")

            for chapter in jsonld_data["hasPart"]:
                if not isinstance(chapter, dict):
                    continue

                # Get chapter URL
                chapter_url = chapter.get("url")
                if not chapter_url:
                    logging.warning(f"Chapter missing URL: {chapter.get('name', 'Unknown')}")
                    continue

                # Find the HTML file for this chapter
                chapter_html_path = get_html_path_from_url(chapter_url, build_dir)
                if not chapter_html_path:
                    logging.warning(
                        f"Could not find HTML file for chapter: {chapter.get('name', 'Unknown')}"
                    )
                    continue

                # Create chapter-specific JSON-LD with book-level metadata
                chapter_jsonld = create_chapter_jsonld(chapter, jsonld_data)

                # Convert to formatted string
                chapter_jsonld_str = json.dumps(chapter_jsonld, ensure_ascii=False, indent=2)
                chapter_jsonld_str = "\n".join(
                    "    " + line for line in chapter_jsonld_str.split("\n")
                )

                # Inject into chapter HTML
                if inject_jsonld_into_html(chapter_html_path, chapter_jsonld_str):
                    chapters_injected += 1
                else:
                    logging.warning(
                        f"Failed to inject JSON-LD into chapter: {chapter.get('name', 'Unknown')}"
                    )

            logging.info(f"Injected JSON-LD into {chapters_injected} chapter pages")

        logging.info("JSON-LD injection completed successfully")
        return True

    except Exception as e:
        logging.exception(f"Unexpected error in inject_jsonld: {e!s}")
        return False


def main():
    """
    Main entry point for the script.

    Usage:
        python -m quadriga.metadata.inject_jsonld
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Inject JSON-LD structured data into Jupyter Book HTML"
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        help="Path to _build/html directory (default: ./_build/html)",
    )
    parser.add_argument(
        "--jsonld-path",
        type=Path,
        help="Path to metadata.jsonld file (default: ./metadata.jsonld)",
    )

    args = parser.parse_args()

    success = inject_jsonld(build_dir=args.build_dir, jsonld_path=args.jsonld_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
