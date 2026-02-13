"""Script to coordinate the different metadata transformation scripts for QUADRIGA Jupyter Books."""

from __future__ import annotations

import logging
import os
import sys

# Add current working directory to sys.path if not present
# This allows the script to run with python -m without package installation
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from quadriga.metadata.create_bibtex import create_bibtex_from_cff
from quadriga.metadata.create_jsonld import create_jsonld
from quadriga.metadata.create_rdfxml import create_rdfxml
from quadriga.metadata.create_zenodo_json import create_zenodo_json
from quadriga.metadata.extract_from_book_config import extract_and_update
from quadriga.metadata.update_citation_cff import update_citation
from quadriga.metadata.validate_schema import validate_schema

logger = logging.getLogger(__name__)


def main() -> bool | None:
    """Run the different metadata transformation scripts in order."""
    try:
        # Configure logging with timestamp
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        logger.info("Running all metadata update scripts...")

        # Validate metadata.yml against QUADRIGA schema first
        try:
            logger.info("Validating metadata.yml against QUADRIGA schema...")
            if not validate_schema():
                logger.error("Schema validation failed.")
                return False
        except Exception:
            logger.exception("Unexpected error during schema validation")
            return False

        # Execute extract_and_update with error handling
        try:
            logger.info("Extracting metadata from _config.yml and _toc.yml...")
            if not extract_and_update():
                logger.error("Extract and update process failed.")
                return False
        except Exception:
            logger.exception("Unexpected error during extract_and_update")
            return False

        # Execute update_citation with error handling
        try:
            logger.info("Updating CITATION.cff...")
            if not update_citation():
                logger.error("Update citation process failed.")
                return False
        except Exception:
            logger.exception("Unexpected error during update_citation")
            return False

        # Execute create_bibtex_from_cff with error handling
        try:
            logger.info("Creating CITATION.bib from CITATION.cff...")
            if not create_bibtex_from_cff():
                logger.error("Create BibTeX process failed.")
                return False
        except Exception:
            logger.exception("Unexpected error during create_bibtex_from_cff")
            return False

        # Execute create_zenodo_json with error handling
        try:
            logger.info("Creating .zenodo.json from CITATION.cff and metadata.yml...")
            if not create_zenodo_json():
                logger.error("Create Zenodo JSON process failed.")
                return False
        except Exception:
            logger.exception("Unexpected error during create_zenodo_json")
            return False

        # Execute create_jsonld with error handling
        try:
            logger.info("Creating metadata.jsonld from metadata.yml...")
            if not create_jsonld():
                logger.error("Create JSON-LD process failed.")
                return False
        except Exception:
            logger.exception("Unexpected error during create_jsonld")
            return False

        # Execute create_rdfxml with error handling
        try:
            logger.info("Creating metadata.rdf from metadata.yml...")
            if not create_rdfxml():
                logger.error("Create RDF/XML process failed.")
                return False
        except Exception:
            logger.exception("Unexpected error during create_rdfxml")
            return False

        logger.info("All scripts executed successfully.")
        return True

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user.")
        return False
    except Exception:
        logger.exception("Unexpected error in main")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
