"""
Injects metadata (JSON-LD and RDF links) into generated HTML files.

This script reads the metadata.jsonld file and injects it as a
<script type="application/ld+json"> tag into the <head> section
of the generated HTML files, making the structured data discoverable
by search engines.

It also adds <link> elements pointing to the standalone metadata files
(metadata.jsonld and metadata.rdf) for RDF consumers and Linked Data tools.

It injects:
- Full book metadata into the root page (determined from _toc.yml)
- Chapter-specific metadata into each chapter's first page
- Link elements to standalone metadata files in all pages

Note: index.html in Jupyter Book is typically just a redirect to the
actual root page, so we determine the real root from _toc.yml.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Minimum number of path parts to consider removing a repository name prefix
MIN_PARTS_FOR_REPO_STRIPPING = 2


def inject_metadata_into_html(html_path: Path, jsonld_content: str, add_link_elements: bool = True) -> bool:
    """
    Inject JSON-LD script tag and metadata link elements into an HTML file's <head> section.

    Args:
        html_path (Path): Path to the HTML file
        jsonld_content (str): JSON-LD content as a string
        add_link_elements (bool): Whether to add <link> elements for metadata files (default: True)

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
            logger.debug("JSON-LD already present in %s, skipping", html_path.name)
            return True

        # Create the JSON-LD script tag with proper indentation
        jsonld_script = f'\n  <script type="application/ld+json">\n{jsonld_content}\n  </script>\n'

        # Create link elements for RDF discovery if requested
        link_elements = ""
        if add_link_elements:
            link_elements = (
                '  <link rel="alternate" type="application/ld+json" '
                'href="/metadata.jsonld" title="JSON-LD Metadata" />\n'
                '  <link rel="alternate" type="application/rdf+xml" '
                'href="/metadata.rdf" title="RDF/XML Metadata" />\n'
            )

        # Find the </head> tag and inject before it
        if "</head>" in html_content:
            # Inject both JSON-LD script and link elements before </head>
            injection = f"{link_elements}{jsonld_script}"
            html_content = html_content.replace("</head>", f"{injection}</head>", 1)
        else:
            logger.warning("No </head> tag found in %s, skipping", html_path.name)
            return False

        # Write the modified HTML back
        with html_path.open("w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info("Injected metadata into %s", html_path.name)

        return True

    except FileNotFoundError:
        logger.exception("HTML file not found")
        return False
    except Exception:
        logger.exception("Error injecting metadata into %s", html_path.name)
        return False


def get_html_path_from_url(url: str, build_dir: Path) -> Path | None:
    """
    Extract the HTML file path from a chapter URL.

    Args:
        url (str): Full URL like "https://quadriga-dk.github.io/Book_Template/präambel/toc.html"
        build_dir (Path): Path to _build/html directory

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
            relative_path = (
                "/".join(parts[1:]) if len(parts) > MIN_PARTS_FOR_REPO_STRIPPING else path
            )

            # Try the path with repo name removed
            html_path = build_dir / relative_path
            if html_path.exists():
                return html_path

        # Try the full path
        html_path = build_dir / path
        if html_path.exists():
            return html_path

        logger.warning("Could not find HTML file for URL: %s", url)
        return None

    except Exception:
        logger.exception("Error parsing URL %s", url)
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


def inject_metadata(
    build_dir: Path | None = None,
    jsonld_path: Path | None = None,
    config_path: Path | None = None,
) -> bool:
    """
    Inject metadata (JSON-LD and RDF links) into HTML files of a Jupyter Book.

    This function reads the metadata.jsonld file and injects:
    1. Full book metadata into the root page (determined from _toc.yml)
    2. Chapter-specific metadata into each chapter's first page
    3. Link elements pointing to standalone metadata files (metadata.jsonld and metadata.rdf)

    For chapters, it creates a LearningResource JSON-LD object with an
    "isPartOf" reference to the parent book, providing better structured
    data when individual chapters are shared or indexed.

    Note: index.html in Jupyter Book is typically just a redirect to the
    actual root page, so we determine the real root from _toc.yml.

    Args:
        build_dir (Path, optional): Path to the _build/html directory.
                                    If None, uses current directory's _build/html
        jsonld_path (Path, optional): Path to metadata.jsonld file.
                                      If None, uses current directory's metadata.jsonld
        config_path (Path, optional): Path to _toc.yml file.
                                      If None, uses current directory's _toc.yml

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
        if config_path is None:
            config_path = Path.cwd() / "_toc.yml"

        # Check if build directory exists
        if not build_dir.exists():
            logger.error("Build directory not found: %s", build_dir)
            return False

        # Check if JSON-LD file exists
        if not jsonld_path.exists():
            logger.error("JSON-LD file not found: %s", jsonld_path)
            return False

        # Read and validate JSON-LD
        try:
            with jsonld_path.open(encoding="utf-8") as f:
                jsonld_data = json.load(f)
            logger.info("Loaded JSON-LD from %s", jsonld_path)
        except json.JSONDecodeError:
            logger.exception("Invalid JSON in %s", jsonld_path)
            return False

        # Convert back to formatted JSON string with indentation
        # Indent by 4 spaces to align nicely within the script tag
        jsonld_content = json.dumps(jsonld_data, ensure_ascii=False, indent=2)
        # Add extra indentation for each line to align within the script tag
        jsonld_content = "\n".join("    " + line for line in jsonld_content.split("\n"))

        # Determine the actual root page from _toc.yml
        root_html = None
        if config_path.exists():
            try:
                import yaml

                with config_path.open(encoding="utf-8") as f:
                    toc_config = yaml.safe_load(f)

                root_file = toc_config.get("root")
                if root_file:
                    # Convert root file path to HTML filename
                    root_html = build_dir / f"{root_file}.html"
                    logger.info("Found root page in _toc.yml: %s", root_file)
            except Exception:
                logger.exception("Error reading _toc.yml, falling back to index.html")

        # Fall back to index.html if we couldn't determine the root
        if root_html is None or not root_html.exists():
            root_html = build_dir / "index.html"
            logger.info("Using index.html as root page")

        # Inject into root page
        if root_html.exists():
            if not inject_metadata_into_html(root_html, jsonld_content):
                logger.error("Failed to inject metadata into %s", root_html.name)
                return False
        else:
            logger.warning("Root HTML file not found at %s", root_html)
            return False

        # Inject chapter-specific metadata into each chapter page
        chapters_injected = 0
        if jsonld_data.get("hasPart"):
            logger.info("Processing %d chapters...", len(jsonld_data["hasPart"]))

            for chapter in jsonld_data["hasPart"]:
                if not isinstance(chapter, dict):
                    continue

                # Get chapter URL
                chapter_url = chapter.get("url")
                if not chapter_url:
                    logger.warning("Chapter missing URL: %s", chapter.get("name", "Unknown"))
                    continue

                # Find the HTML file for this chapter
                chapter_html_path = get_html_path_from_url(chapter_url, build_dir)
                if not chapter_html_path:
                    logger.warning(
                        "Could not find HTML file for chapter: %s", chapter.get("name", "Unknown")
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
                if inject_metadata_into_html(chapter_html_path, chapter_jsonld_str):
                    chapters_injected += 1
                else:
                    logger.warning(
                        "Failed to inject metadata into chapter: %s", chapter.get("name", "Unknown")
                    )

            logger.info("Injected metadata into %d chapter pages", chapters_injected)

        logger.info("Metadata injection completed successfully")
        return True

    except Exception:
        logger.exception("Unexpected error in inject_metadata")
        return False


def main() -> None:
    """
    Run the metadata injection script.

    Usage:
        python -m quadriga.metadata.inject_metadata
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Inject metadata (JSON-LD and RDF links) into Jupyter Book HTML"
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
    parser.add_argument(
        "--config-path",
        type=Path,
        help="Path to _toc.yml file (default: ./_toc.yml)",
    )

    args = parser.parse_args()

    success = inject_metadata(
        build_dir=args.build_dir,
        jsonld_path=args.jsonld_path,
        config_path=args.config_path,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
