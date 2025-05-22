#!/usr/bin/env python3
import sys
import logging
from pathlib import Path
from .utils import load_yaml_file, get_file_path, format_authors_for_bibtex, generate_citation_key

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_bibtex_from_cff():
    """
    Creates a CITATION.bib file from CITATION.cff.

    It reads citation data, prioritizing the 'preferred-citation' block if available,
    formats authors, generates a citation key, and constructs a BibTeX entry.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Define file paths using utility functions
        try:
            repo_root = get_file_path('') # Get repo root
            citation_cff_path = get_file_path('CITATION.cff', repo_root)
            citation_bib_path = get_file_path('CITATION.bib', repo_root)
        except Exception as e:
            logging.error(f"Failed to resolve file paths: {str(e)}")
            return False

        # Check if citation_cff_path exists
        if not Path(citation_cff_path).exists():
            logging.error(f"CITATION.cff file not found at {citation_cff_path}")
            return False

        # Read CITATION.cff using utility function
        citation_data = load_yaml_file(citation_cff_path)
        
        if not citation_data:
            logging.error(f"Could not load {citation_cff_path}. Exiting.")
            return False

        # Extract data from preferred-citation or root
        if 'preferred-citation' in citation_data:
            logging.info("Using 'preferred-citation' section from CITATION.cff")
            pref = citation_data.get('preferred-citation')
        else:
            logging.info("No 'preferred-citation' section found, using root data")
            pref = citation_data
        
        # Validate required fields
        authors = pref.get('authors', [])
        title = pref.get('title', 'Untitled')
        year = str(pref.get('year', '')) # Ensure year is a string for generate_citation_key
        
        if not authors:
            logging.warning("No authors found in CITATION.cff")
        
        if title == 'Untitled':
            logging.warning("No title found in CITATION.cff, using 'Untitled'")
            
        if not year:
            logging.warning("No year found in CITATION.cff")

        # Use utility function to format authors
        try:
            author_str = format_authors_for_bibtex(authors)
        except Exception as e:
            logging.error(f"Error formatting authors: {str(e)}")
            author_str = ""
        
        # Choose entry type based on type field
        entry_type = 'book' if pref.get('type') == 'book' else 'misc'
        logging.info(f"Using BibTeX entry type: {entry_type}")
        
        # Use utility function to generate citation key
        try:
            citation_key = generate_citation_key(authors, title, year)
        except Exception as e:
            logging.error(f"Error generating citation key: {str(e)}")
            citation_key = "Unknown_Citation_Key"
        
        # Compile BibTeX entry
        bibtex_lines = [f"@{entry_type}{{{citation_key},"]
        
        # Add fields
        if title != 'Untitled': # Only add title if it's not the default placeholder
            bibtex_lines.append(f"  title     = {{{title}}},")
        if author_str:
            bibtex_lines.append(f"  author    = {{{author_str}}},")
        if year:
            bibtex_lines.append(f"  year      = {{{year}}},")
        
        simple_fields = ['doi', 'url', 'copyright', 'publisher', 'address', 'edition', 'isbn']
        for field in simple_fields:
            if field in pref:
                # Sanitize field value to avoid BibTeX syntax errors
                field_value = str(pref[field]).replace('{', '').replace('}', '')
                bibtex_lines.append(f"  {field:<9} = {{{field_value}}},")
                
        if 'languages' in pref and pref['languages']: # Handle list of languages
            try:
                languages_str = ', '.join(pref['languages'])
                bibtex_lines.append(f"  language  = {{{languages_str}}},")
            except Exception as e:
                logging.warning(f"Error processing languages field: {str(e)}")
        
        # Close the entry
        bibtex_lines.append("}")
        bibtex = "\n".join(bibtex_lines)
        
        # Write to CITATION.bib
        try:
            with open(citation_bib_path, 'w', encoding='utf-8') as f:
                f.write(bibtex)
            logging.info(f"BibTeX citation successfully created at {citation_bib_path}")
            return True
        except IOError as e:
            logging.error(f"Error writing to {citation_bib_path}: {e}")
            return False
            
    except Exception as e:
        logging.exception(f"Unexpected error in create_bibtex_from_cff: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_bibtex_from_cff()
    sys.exit(0 if success else 1)