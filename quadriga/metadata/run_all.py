"""
This script runs the various metadata update scripts in the correct order.
"""
from .extract_from_config_toc import extract_and_update
from .update_citation_cff import update_citation
from .create_bibtex import create_bibtex_from_cff

def main():
    print("Running all metadata update scripts...")
    print()
    print("Extracting metadata from _config.yml and _toc.yml...")
    extract_and_update()
    print()
    print("Updating CITATION.cff...")
    update_citation()
    print()
    print("Creating CITATION.bib from CITATION.cff...")
    create_bibtex_from_cff()
    print()
    print("All scripts executed successfully.")

if __name__ == "__main__":
    main()
    