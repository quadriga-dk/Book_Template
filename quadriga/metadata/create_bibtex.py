#!/usr/bin/env python3
import sys
import logging 
from .utils import load_yaml_file, get_file_path, format_authors_for_bibtex, generate_citation_key

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_bibtex_from_cff():
    """
    Creates a CITATION.bib file from CITATION.cff.

    It reads citation data, prioritizing the 'preferred-citation' block if available,
    formats authors, generates a citation key, and constructs a BibTeX entry.
    The resulting BibTeX entry is written to 'CITATION.bib'.
    """
    # Define file paths using utility functions
    repo_root = get_file_path('') # Get repo root
    citation_cff_path = get_file_path('CITATION.cff', repo_root)
    citation_bib_path = get_file_path('CITATION.bib', repo_root)

    # Read CITATION.cff using utility function
    citation_data = load_yaml_file(citation_cff_path)
    
    if not citation_data:
        logging.error(f"Could not load {citation_cff_path}. Exiting.")
        return

    # Extract data from preferred-citation or root
    pref = citation_data.get('preferred-citation', citation_data)
    
    authors = pref.get('authors', [])
    title = pref.get('title', 'Untitled')
    year = str(pref.get('year', '')) # Ensure year is a string for generate_citation_key

    # Use utility function to format authors
    author_str = format_authors_for_bibtex(authors)
    
    # Choose entry type based on type field
    entry_type = 'book' if pref.get('type') == 'book' else 'misc'
    
    # Use utility function to generate citation key
    citation_key = generate_citation_key(authors, title, year)
    
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
            bibtex_lines.append(f"  {field:<9} = {{{pref[field]}}},")
            
    if 'languages' in pref and pref['languages']: # Handle list of languages
        bibtex_lines.append(f"  language  = {{{', '.join(pref['languages'])}}},")
    
    # Close the entry
    bibtex_lines.append("}")
    bibtex = "\n".join(bibtex_lines)
    
    # Write to CITATION.bib
    try:
        with open(citation_bib_path, 'w', encoding='utf-8') as f:
            f.write(bibtex)
        logging.info(f"BibTeX citation successfully created at {citation_bib_path}")
    except IOError as e:
        logging.error(f"Error writing to {citation_bib_path}: {e}")

if __name__ == "__main__":
    create_bibtex_from_cff()