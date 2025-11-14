"""
Injects all metadata (JSON-LD, OpenGraph, and RDF links) into generated HTML files.

This unified script combines JSON-LD structured data injection and OpenGraph
social media metadata into a single efficient pass through HTML files.

It reads metadata.jsonld and injects:
- OpenGraph <meta> tags for social media previews
- JSON-LD <script> tags for search engine structured data
- <link> elements to standalone metadata files

For the root page:
- OpenGraph: og:type="book" with book:author, book:release_date, book:tag
- JSON-LD: Full book metadata

For chapter pages:
- OpenGraph: og:type="article" with article:author, article:published_time, article:modified_time
- JSON-LD: Chapter-specific LearningResource with isPartOf reference to book

All metadata is injected in a single operation per HTML file for optimal performance.
"""

from __future__ import annotations

import html as html_module
import json
import logging
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Minimum number of path parts to consider removing a repository name prefix
MIN_PARTS_FOR_REPO_STRIPPING = 2

# Locale mapping for OpenGraph og:locale property
LOCALE_MAP = {
    "de": "de_DE",
    "en": "en_US",
    "en-gb": "en_GB",
    "fr": "fr_FR",
    "es": "es_ES",
    "it": "it_IT",
    "pt": "pt_PT",
    "pt-br": "pt_BR",
    "nl": "nl_NL",
    "pl": "pl_PL",
    "ru": "ru_RU",
    "ja": "ja_JP",
    "zh": "zh_CN",
    "zh-tw": "zh_TW",
    "ko": "ko_KR",
    "ar": "ar_AR",
}


# ============================================================================
# Shared Utility Functions
# ============================================================================


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


def get_logo_from_config(config_path: Path) -> str:
    """
    Extract logo filename from _config.yml.

    Args:
        config_path (Path): Path to _config.yml file

    Returns
    -------
        str: Logo filename (e.g., 'logo.jpg', 'logo.png')
    """
    try:
        import yaml

        with config_path.open(encoding="utf-8") as f:
            config = yaml.safe_load(f)

        logo_path = config.get("logo", "assets/logo.jpg")

        # Extract filename from path (e.g., 'assets/logo.jpg' -> 'logo.jpg')
        return Path(logo_path).name

    except FileNotFoundError:
        logger.warning("Config file not found at %s, using default logo", config_path)
        return "logo.jpg"
    except Exception:
        logger.exception("Could not read logo from _config.yml, using default")
        return "logo.jpg"


def get_root_page_from_toc(toc_path: Path, build_dir: Path) -> Path | None:
    """
    Determine the root page HTML file from _toc.yml.

    Args:
        toc_path (Path): Path to _toc.yml file
        build_dir (Path): Path to _build/html directory

    Returns
    -------
        Path: Path to root HTML file, or None if not found
    """
    if not toc_path.exists():
        return None

    try:
        import yaml

        with toc_path.open(encoding="utf-8") as f:
            toc_config = yaml.safe_load(f)

        root_file = toc_config.get("root")
        if root_file:
            # Convert root file path to HTML filename
            root_html = build_dir / f"{root_file}.html"
            if root_html.exists():
                logger.info("Found root page in _toc.yml: %s", root_file)
                return root_html

    except Exception:
        logger.exception("Error reading _toc.yml")

    return None


# ============================================================================
# OpenGraph Functions
# ============================================================================


def escape_html(text: str) -> str:
    """
    Escape HTML special characters in text.

    Args:
        text (str): Text to escape

    Returns
    -------
        str: HTML-escaped text
    """
    return html_module.escape(text, quote=True)


def format_locale(language_code: str) -> str:
    """
    Convert ISO 639-1 language code to OpenGraph locale format.

    Args:
        language_code (str): ISO 639-1 code (e.g., 'de', 'en', 'fr')

    Returns
    -------
        str: OpenGraph locale format (e.g., 'de_DE', 'en_US', 'fr_FR')
    """
    # Convert to lowercase for lookup
    lang_lower = language_code.lower()

    # Try exact match first
    if lang_lower in LOCALE_MAP:
        return LOCALE_MAP[lang_lower]

    # Fallback: construct as {lang}_{LANG.upper()}
    return f"{lang_lower}_{lang_lower.upper()}"


def get_logo_url(base_url: str, logo_filename: str) -> str:
    """
    Get the full URL to the logo image.

    The logo is copied to _static/ during Jupyter Book build.

    Args:
        base_url (str): Base URL of the site (from metadata)
        logo_filename (str): Logo filename (e.g., 'logo.jpg')

    Returns
    -------
        str: Full URL to logo (e.g., 'https://example.com/_static/logo.jpg')
    """
    # Logo is copied to _static/ during Jupyter Book build
    return f"{base_url.rstrip('/')}/_static/{logo_filename}"


def format_author_name(author_data: dict) -> str:
    """
    Format author information as full name string.

    Args:
        author_data (dict): Person object with givenName and familyName

    Returns
    -------
        str: Full name as single string (e.g., "Hannes Schnaitter")
    """
    given = author_data.get("givenName", "")
    family = author_data.get("familyName", "")
    name = author_data.get("name", "")  # Fallback to name if available

    if given and family:
        return f"{given} {family}"
    elif name:
        return name

    return given or family


def ensure_absolute_url(url: str, base_url: str) -> str:
    """
    Ensure URL is absolute, construct from base if needed.

    OpenGraph requires absolute URLs for all URL properties.

    Args:
        url (str): URL to check/convert
        base_url (str): Base URL to use for relative URLs

    Returns
    -------
        str: Absolute URL
    """
    if not urlparse(url).netloc:
        return urljoin(base_url, url)
    return url


def create_opengraph_meta_tags(
    jsonld_data: dict,
    base_url: str,
    book_title: str,
    logo_filename: str,
    is_chapter: bool = False,
) -> str:
    """
    Transform JSON-LD metadata into OpenGraph <meta> tags.

    For root page: Uses og:type="book" with book:* properties
    For chapters: Uses og:type="article" with article:* properties

    Args:
        jsonld_data (dict): JSON-LD metadata object (schema.org format)
        base_url (str): Base URL of the site (for constructing absolute URLs)
        book_title (str): Title of the book (for og:site_name)
        logo_filename (str): Logo filename (e.g., 'logo.jpg')
        is_chapter (bool): Whether this is a chapter page or root page

    Returns
    -------
        str: String containing all OpenGraph meta tags
    """
    tags = []

    # Required: og:title
    if "name" in jsonld_data:
        tags.append(f'  <meta property="og:title" content="{escape_html(jsonld_data["name"])}" />')

    # Required: og:type
    # Root page = "book", chapters = "article"
    content_type = "article" if is_chapter else "book"
    tags.append(f'  <meta property="og:type" content="{content_type}" />')

    # Required: og:url (ensure absolute)
    if "url" in jsonld_data:
        url = ensure_absolute_url(jsonld_data["url"], base_url)
        tags.append(f'  <meta property="og:url" content="{escape_html(url)}" />')

    # Required: og:image
    image_url = get_logo_url(base_url, logo_filename)
    tags.append(f'  <meta property="og:image" content="{escape_html(image_url)}" />')

    # Recommended: og:description
    if "description" in jsonld_data:
        tags.append(
            f'  <meta property="og:description" content="{escape_html(jsonld_data["description"])}" />'
        )

    # og:site_name (use book title for all pages)
    tags.append(f'  <meta property="og:site_name" content="{escape_html(book_title)}" />')

    # og:locale
    if "inLanguage" in jsonld_data:
        language = jsonld_data["inLanguage"]
        # Handle both single language (string) and multiple languages (array)
        if isinstance(language, list):
            language = language[0]  # Use first language
        locale = format_locale(language)
        tags.append(f'  <meta property="og:locale" content="{locale}" />')

    # Author tags - use book:author for root page, article:author for chapters
    if "author" in jsonld_data:
        authors = jsonld_data["author"]
        if not isinstance(authors, list):
            authors = [authors]

        author_property = "book:author" if not is_chapter else "article:author"
        for author in authors:
            author_name = format_author_name(author)
            if author_name:
                tags.append(
                    f'  <meta property="{author_property}" content="{escape_html(author_name)}" />'
                )

    # Date properties - different for books vs articles
    if not is_chapter:
        # Root page: book:release_date
        if "datePublished" in jsonld_data:
            tags.append(f'  <meta property="book:release_date" content="{jsonld_data["datePublished"]}" />')
        # Note: books don't have a modified_time property in OpenGraph
    else:
        # Chapters: article:published_time and article:modified_time
        if "datePublished" in jsonld_data:
            tags.append(f'  <meta property="article:published_time" content="{jsonld_data["datePublished"]}" />')
        if "dateModified" in jsonld_data:
            tags.append(f'  <meta property="article:modified_time" content="{jsonld_data["dateModified"]}" />')

    # Tags/keywords - use book:tag for root page only
    if not is_chapter and "keywords" in jsonld_data:
        keywords = jsonld_data["keywords"]
        # Handle string (comma-separated) or array
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(",")]
        elif not isinstance(keywords, list):
            keywords = []

        for keyword in keywords:
            if keyword:  # Skip empty strings
                tags.append(f'  <meta property="book:tag" content="{escape_html(keyword)}" />')

    return "\n".join(tags)


# ============================================================================
# JSON-LD Functions
# ============================================================================


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


# ============================================================================
# Unified HTML Injection
# ============================================================================


def inject_all_metadata_into_html(
    html_path: Path,
    og_tags: str,
    jsonld_content: str,
    add_link_elements: bool = True,
) -> bool:
    """
    Inject all metadata (OpenGraph, JSON-LD, and RDF links) into an HTML file's <head>.

    This unified injection function combines OpenGraph meta tags, JSON-LD structured data,
    and RDF link elements into a single efficient operation.

    Injection strategy:
    1. Find optimal position (after viewport/charset meta tags, or before </head>)
    2. Inject in this order:
       - OpenGraph meta tags (for social media crawlers)
       - JSON-LD script tag (for search engines)
       - Link elements (for RDF discovery)

    Args:
        html_path (Path): Path to the HTML file
        og_tags (str): OpenGraph meta tags as string
        jsonld_content (str): JSON-LD content as formatted string
        add_link_elements (bool): Whether to add <link> elements for metadata files (default: True)

    Returns
    -------
        bool: True if successful, False otherwise
    """
    try:
        # Read the HTML file
        with html_path.open(encoding="utf-8") as f:
            html_content = f.read()

        # Check if metadata is already present (avoid duplicates)
        if '<meta property="og:' in html_content or '<script type="application/ld+json">' in html_content:
            logger.debug("Metadata already present in %s, skipping", html_path.name)
            return True

        # Build the complete injection content
        injection_parts = []

        # 1. OpenGraph metadata
        if og_tags:
            injection_parts.append(og_tags)

        # 2. JSON-LD structured data
        if jsonld_content:
            injection_parts.append(f'  <script type="application/ld+json">\n{jsonld_content}\n  </script>')

        # 3. RDF discovery links
        if add_link_elements:
            injection_parts.append(
                '  <link rel="alternate" type="application/ld+json" '
                'href="/metadata.jsonld" title="JSON-LD Metadata" />'
            )
            injection_parts.append(
                '  <link rel="alternate" type="application/rdf+xml" '
                'href="/metadata.rdf" title="RDF/XML Metadata" />'
            )

        # Join all parts with newlines
        full_injection = "\n".join(injection_parts)

        # Find optimal injection point
        # Priority: after viewport, after charset, before </head> (fallback)
        injection_point = None

        # Try to inject after viewport meta tag (best practice for OpenGraph)
        viewport_match = re.search(r"(<meta\s+name=\"viewport\"[^>]*>\s*)", html_content, re.IGNORECASE)
        if viewport_match:
            injection_point = viewport_match.end()
        else:
            # Fallback: try after charset meta tag
            charset_match = re.search(r"(<meta\s+charset[^>]*>\s*)", html_content, re.IGNORECASE)
            if charset_match:
                injection_point = charset_match.end()

        # Final fallback: inject before </head>
        if injection_point is None:
            injection_point = html_content.find("</head>")
            if injection_point == -1:
                logger.warning("No </head> tag found in %s, skipping", html_path.name)
                return False
            # For </head> injection, add before the tag
            html_content = html_content[:injection_point] + f"\n{full_injection}\n" + html_content[injection_point:]
        else:
            # For after viewport/charset injection, insert at found position
            html_content = html_content[:injection_point] + f"\n{full_injection}\n\n" + html_content[injection_point:]

        # Write the modified HTML back
        with html_path.open("w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info("Injected all metadata into %s", html_path.name)
        return True

    except FileNotFoundError:
        logger.exception("HTML file not found: %s", html_path)
        return False
    except Exception:
        logger.exception("Error injecting metadata into %s", html_path)
        return False


# ============================================================================
# Main Injection Orchestration
# ============================================================================


def inject_all_metadata(
    build_dir: Path | None = None,
    jsonld_path: Path | None = None,
    config_path: Path | None = None,
    toc_path: Path | None = None,
) -> bool:
    """
    Inject all metadata (OpenGraph, JSON-LD, and RDF links) into Jupyter Book HTML files.

    This unified function combines OpenGraph social media metadata and JSON-LD structured
    data injection into a single efficient operation.

    For the root page, it injects:
    - OpenGraph: og:type="book" with book:author, book:release_date, book:tag
    - JSON-LD: Full book metadata

    For chapter pages, it injects:
    - OpenGraph: og:type="article" with article:author, article:published_time, article:modified_time
    - JSON-LD: Chapter-specific LearningResource with isPartOf reference to book

    Args:
        build_dir (Path, optional): Path to _build/html directory (default: ./_build/html)
        jsonld_path (Path, optional): Path to metadata.jsonld (default: ./metadata.jsonld)
        config_path (Path, optional): Path to _config.yml (default: ./_config.yml)
        toc_path (Path, optional): Path to _toc.yml (default: ./_toc.yml)

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
            config_path = Path.cwd() / "_config.yml"
        if toc_path is None:
            toc_path = Path.cwd() / "_toc.yml"

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

        # Extract base URL from metadata
        base_url = jsonld_data.get("url", "")
        if not base_url:
            logger.error("No URL found in metadata.jsonld")
            return False

        # Extract book title for og:site_name
        book_title = jsonld_data.get("name", "")
        if not book_title:
            logger.warning("No book title found in metadata.jsonld")

        # Get logo filename from config
        logo_filename = get_logo_from_config(config_path)
        logger.info("Using logo: %s", logo_filename)

        # Determine the actual root page from _toc.yml
        root_html = get_root_page_from_toc(toc_path, build_dir)

        # Fall back to index.html if we couldn't determine the root
        if root_html is None or not root_html.exists():
            root_html = build_dir / "index.html"
            logger.info("Using index.html as root page")

        # ====================================================================
        # Process root page
        # ====================================================================
        if root_html.exists():
            # Generate OpenGraph tags for root page (og:type="book")
            og_tags = create_opengraph_meta_tags(
                jsonld_data,
                base_url,
                book_title,
                logo_filename,
                is_chapter=False,
            )

            # Format JSON-LD content with proper indentation
            jsonld_content = json.dumps(jsonld_data, ensure_ascii=False, indent=2)
            jsonld_content = "\n".join("    " + line for line in jsonld_content.split("\n"))

            # Inject both OpenGraph and JSON-LD into root page
            if not inject_all_metadata_into_html(root_html, og_tags, jsonld_content):
                logger.error("Failed to inject metadata into %s", root_html.name)
                return False
        else:
            logger.warning("Root HTML file not found at %s", root_html)
            return False

        # ====================================================================
        # Process index.html redirect page (if different from root)
        # ====================================================================
        # Jupyter Book may create index.html as a meta-refresh redirect
        # Social media crawlers don't follow these redirects, so we need
        # to inject OpenGraph metadata into index.html as well
        index_html = build_dir / "index.html"
        if index_html.exists() and index_html != root_html:
            try:
                with index_html.open(encoding="utf-8") as f:
                    index_content = f.read()

                # Check if this is a simple meta-refresh redirect page (with or without proper HTML structure)
                if "meta http-equiv" in index_content.lower():
                    logger.info("Found index.html redirect page, injecting OpenGraph metadata")

                    # Generate OpenGraph tags (but skip JSON-LD for redirect page)
                    og_tags = create_opengraph_meta_tags(
                        jsonld_data,
                        base_url,
                        book_title,
                        logo_filename,
                        is_chapter=False,
                    )

                    # Check if the redirect page has proper HTML structure
                    if "<html" not in index_content.lower() or "<head" not in index_content.lower():
                        # Minimal redirect without proper structure - create proper HTML
                        logger.info("Minimal redirect detected, creating proper HTML structure with OpenGraph")

                        # Extract the meta refresh tag
                        meta_refresh_match = re.search(r'<meta\s+http-equiv[^>]*>', index_content, re.IGNORECASE)
                        meta_refresh = meta_refresh_match.group(0) if meta_refresh_match else ""

                        # Create proper HTML with OpenGraph metadata and meta refresh
                        new_index_content = f"""<!DOCTYPE html>
<html lang="{jsonld_data.get('inLanguage', 'en')}">
<head>
  <meta charset="utf-8" />
  {meta_refresh}
{og_tags}
  <title>{escape_html(book_title)}</title>
</head>
<body>
  <p>Redirecting to <a href="{root_html.name}">{root_html.name}</a>...</p>
</body>
</html>
"""
                        # Write the new index.html
                        with index_html.open("w", encoding="utf-8") as f:
                            f.write(new_index_content)
                        logger.info("Successfully created index.html with OpenGraph metadata and redirect")
                    else:
                        # Has proper HTML structure, inject normally
                        if not inject_all_metadata_into_html(index_html, og_tags, "", add_link_elements=False):
                            logger.warning("Failed to inject OpenGraph into index.html redirect page")
                        else:
                            logger.info("Successfully injected OpenGraph metadata into index.html redirect page")
            except Exception:
                logger.exception("Error processing index.html redirect page")

        # ====================================================================
        # Process chapter pages
        # ====================================================================
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
                    logger.warning("Could not find HTML file for chapter: %s", chapter.get("name", "Unknown"))
                    continue

                # Create chapter metadata for OpenGraph (combining chapter + book data)
                chapter_og_metadata = {
                    "name": chapter.get("name", ""),
                    "url": chapter_url,
                    "description": chapter.get("description", ""),
                    "author": jsonld_data.get("author", []),  # Inherit from book
                    "datePublished": jsonld_data.get("datePublished"),  # Inherit from book
                    "dateModified": jsonld_data.get("dateModified"),  # Inherit from book
                    "inLanguage": jsonld_data.get("inLanguage"),  # Inherit from book
                }

                # Generate OpenGraph tags for chapter (og:type="article")
                chapter_og_tags = create_opengraph_meta_tags(
                    chapter_og_metadata,
                    base_url,
                    book_title,
                    logo_filename,
                    is_chapter=True,
                )

                # Create chapter-specific JSON-LD with book-level metadata
                chapter_jsonld = create_chapter_jsonld(chapter, jsonld_data)

                # Convert to formatted string
                chapter_jsonld_str = json.dumps(chapter_jsonld, ensure_ascii=False, indent=2)
                chapter_jsonld_str = "\n".join("    " + line for line in chapter_jsonld_str.split("\n"))

                # Inject both OpenGraph and JSON-LD into chapter HTML
                if inject_all_metadata_into_html(chapter_html_path, chapter_og_tags, chapter_jsonld_str):
                    chapters_injected += 1
                else:
                    logger.warning("Failed to inject metadata into chapter: %s", chapter.get("name", "Unknown"))

            logger.info("Injected metadata into %d chapter pages", chapters_injected)

        logger.info("All metadata injection completed successfully")
        return True

    except Exception:
        logger.exception("Unexpected error in inject_all_metadata")
        return False


# ============================================================================
# CLI Entry Point
# ============================================================================


def main() -> None:
    """
    Run the unified metadata injection script.

    Usage:
        python -m quadriga.metadata.inject_all_metadata
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Inject all metadata (OpenGraph, JSON-LD, RDF links) into Jupyter Book HTML"
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
        help="Path to _config.yml file (default: ./_config.yml)",
    )
    parser.add_argument(
        "--toc-path",
        type=Path,
        help="Path to _toc.yml file (default: ./_toc.yml)",
    )

    args = parser.parse_args()

    success = inject_all_metadata(
        build_dir=args.build_dir,
        jsonld_path=args.jsonld_path,
        config_path=args.config_path,
        toc_path=args.toc_path,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
