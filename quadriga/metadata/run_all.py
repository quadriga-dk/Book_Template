"""
This script runs the various metadata update scripts in the correct order.
"""
import logging
from .extract_from_book_config import extract_and_update
from .update_citation_cff import update_citation
from .create_bibtex import create_bibtex_from_cff

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logging.info("Running all metadata update scripts...")
    logging.info("Extracting metadata from _config.yml and _toc.yml...")
    extract_and_update()
    logging.info("Updating CITATION.cff...")
    update_citation()
    logging.info("Creating CITATION.bib from CITATION.cff...")
    create_bibtex_from_cff()
    logging.info("All scripts executed successfully.")

if __name__ == "__main__":
    main()
