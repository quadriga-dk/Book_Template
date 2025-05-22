"""
This script runs the various metadata update scripts in the correct order.
"""
import logging
import sys
from .extract_from_book_config import extract_and_update
from .update_citation_cff import update_citation
from .create_bibtex import create_bibtex_from_cff

def main():
    try:
        # Configure logging with timestamp
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        logging.info("Running all metadata update scripts...")
        
        # Execute extract_and_update with error handling
        try:
            logging.info("Extracting metadata from _config.yml and _toc.yml...")
            if not extract_and_update():
                logging.error("Extract and update process failed.")
                return False
        except Exception as e:
            logging.exception(f"Unexpected error during extract_and_update: {str(e)}")
            return False
            
        # Execute update_citation with error handling
        try:
            logging.info("Updating CITATION.cff...")
            if not update_citation():
                logging.error("Update citation process failed.")
                return False
        except Exception as e:
            logging.exception(f"Unexpected error during update_citation: {str(e)}")
            return False
        
        # Execute create_bibtex_from_cff with error handling
        try:
            logging.info("Creating CITATION.bib from CITATION.cff...")
            if not create_bibtex_from_cff():
                logging.error("Create BibTeX process failed.")
                return False
        except Exception as e:
            logging.exception(f"Unexpected error during create_bibtex_from_cff: {str(e)}")
            return False
        
        logging.info("All scripts executed successfully.")
        return True
        
    except KeyboardInterrupt:
        logging.warning("Process interrupted by user.")
        return False
    except Exception as e:
        logging.exception(f"Unexpected error in main: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
