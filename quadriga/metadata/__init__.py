"""
Metadata management tools for QUADRIGA OERs.

This subpackage contains scripts for managing metadata across different formats
including CITATION.cff, CITATION.bib, and extracting metadata from _config.yml.
"""

__all__ = [
    "create_bibtex",
    "create_citation_cff",
    "extract_from_book_config",
    "update_version_from_tag",
    "utils",
]

# Import the modules to make their functions available
from . import (
    create_bibtex,
    create_citation_cff,
    extract_from_book_config,
    update_version_from_tag,
    utils,
)
