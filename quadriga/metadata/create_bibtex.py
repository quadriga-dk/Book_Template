#!/usr/bin/env python3
import sys
import logging
from pathlib import Path
from .utils import load_yaml_file, get_file_path, format_authors_for_bibtex, generate_citation_key

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Map CFF types to BibTeX entry types
CFF_TO_BIBTEX_TYPES = {
    # Academic publications
    'article': 'article',             # Journal article
    'magazine-article': 'article',    # Magazine article
    'newspaper-article': 'article',   # Newspaper article
    'book': 'book',                   # Complete book
    'edited-work': 'incollection',    # Edited work should be incollection (contribution in book)
    'conference-paper': 'inproceedings', # Conference paper
    'proceedings': 'proceedings',     # Conference proceedings
    'conference': 'proceedings',      # Conference (same as proceedings)
    'thesis': 'thesis',               # Generic thesis - will be refined in the code based on type field
    'report': 'techreport',           # Technical report
    'pamphlet': 'booklet',            # Short printed work
    'unpublished': 'unpublished',     # Unpublished work
    'manual': 'manual',               # Technical documentation/manual
    
    # Digital resources
    'software': 'misc',               # Software/code - use misc with howpublished field
    'software-code': 'misc',          # Software source code
    'software-container': 'misc',     # Software container
    'software-executable': 'misc',    # Executable software
    'software-virtual-machine': 'misc', # Software VM
    'data': 'misc',                   # Dataset
    'database': 'misc',               # Database
    'website': 'misc',                # Website - use misc with howpublished=URL
    'blog': 'misc',                   # Blog post - use misc with howpublished=URL
    
    # Media and audiovisual
    'art': 'misc',                    # Artwork
    'audiovisual': 'misc',            # Audiovisual material
    'film-broadcast': 'misc',         # Film or broadcast
    'sound-recording': 'misc',        # Sound recording
    'video': 'misc',                  # Video
    'multimedia': 'misc',             # Multimedia
    'music': 'misc',                  # Music
    'slides': 'misc',                 # Presentation slides
    
    # Reference works
    'catalogue': 'book',              # Catalogue
    'dictionary': 'book',             # Dictionary
    'encyclopedia': 'book',           # Encyclopedia
    'map': 'misc',                    # Map
    
    # Legal and government
    'bill': 'misc',                   # Legislative bill
    'legal-case': 'misc',             # Legal case
    'legal-rule': 'misc',             # Legal rule or regulation
    'government-document': 'techreport', # Government document
    'hearing': 'misc',                # Hearing
    'statute': 'misc',                # Statute
    'standard': 'misc',               # Standard (could be techreport in some contexts)
    'patent': 'patent',               # Patent - supported in some BibTeX styles
    
    # Other types
    'generic': 'misc',                # Generic document
    'grant': 'misc',                  # Grant
    'historical-work': 'book',        # Historical work
    'personal-communication': 'misc', # Personal communication
    'serial': 'periodical',           # Serial publication
}

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
        cff_type = pref.get('type', 'software')  # Default to software if not specified
        
        # Get the entry type from the mapping, default to 'misc' if not found
        entry_type = CFF_TO_BIBTEX_TYPES.get(cff_type.lower(), 'misc')
        
        # Special handling for thesis types
        if entry_type == 'thesis':
            # Check for thesis type information
            thesis_type = pref.get('thesis-type', '').lower()
            if thesis_type == 'master' or thesis_type == 'masters' or thesis_type == "master's":
                entry_type = 'mastersthesis'
            else:
                # Default to phdthesis if type is not specified or is something else
                entry_type = 'phdthesis'
                
        logging.info(f"Converting CFF type '{cff_type}' to BibTeX entry type: {entry_type}")
        
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
        
        # Define common fields for all entry types
        simple_fields = ['doi', 'url', 'copyright', 'publisher', 'address', 'edition', 'isbn']
        
        # Add entry-specific fields based on the entry type
        if entry_type == 'article':
            article_fields = ['journal', 'volume', 'number', 'pages', 'month', 'issn']
            simple_fields.extend(article_fields)
            
            # Map CFF journal-specific fields to BibTeX fields
            if 'collection-title' in pref and 'journal' not in pref:
                bibtex_lines.append(f"  journal   = {{{pref['collection-title']}}},")
            if 'volume-title' in pref and 'journal' not in pref and 'collection-title' not in pref:
                bibtex_lines.append(f"  journal   = {{{pref['volume-title']}}},")
        
        elif entry_type in ['inproceedings', 'proceedings']:
            conf_fields = ['booktitle', 'series', 'volume', 'pages', 'month', 'organization']
            simple_fields.extend(conf_fields)
            
            # Map CFF conference-specific fields to BibTeX fields
            if 'conference' in pref and 'booktitle' not in pref:
                conf_name = pref['conference'].get('name', '') if isinstance(pref['conference'], dict) else str(pref['conference'])
                if conf_name:
                    bibtex_lines.append(f"  booktitle = {{{conf_name}}},")
            
            if 'collection-title' in pref and 'booktitle' not in pref:
                bibtex_lines.append(f"  booktitle = {{{pref['collection-title']}}},")
        
        elif entry_type in ['phdthesis', 'mastersthesis']:
            thesis_fields = ['school', 'type', 'month']
            simple_fields.extend(thesis_fields)
            
            # Add institution as school if present
            if 'institution' in pref and 'school' not in pref:
                institution = pref['institution'].get('name', '') if isinstance(pref['institution'], dict) else str(pref['institution'])
                if institution:
                    bibtex_lines.append(f"  school    = {{{institution}}},")
        
        elif entry_type == 'techreport':
            report_fields = ['institution', 'number', 'type']
            simple_fields.extend(report_fields)
            
        elif entry_type == 'incollection':
            # Add fields specific to book chapters
            incollection_fields = ['booktitle', 'editor', 'chapter', 'pages', 'publisher', 'address']
            simple_fields.extend(incollection_fields)
            
            # Map collection-title to booktitle if present
            if 'collection-title' in pref and 'booktitle' not in pref:
                bibtex_lines.append(f"  booktitle = {{{pref['collection-title']}}},")
                
            # Map collection editor if available
            if 'collection-editors' in pref and isinstance(pref['collection-editors'], list):
                try:
                    editor_str = format_authors_for_bibtex(pref['collection-editors'])
                    bibtex_lines.append(f"  editor    = {{{editor_str}}},")
                except Exception as e:
                    logging.warning(f"Error formatting collection editors: {str(e)}")
            
        # Special handling for software, code, data entries
        if cff_type.lower().startswith('software') or cff_type.lower() in ['data', 'database']:
            soft_fields = ['version', 'note']
            simple_fields.extend(soft_fields)
            
            # Add repository info to note field if available
            if 'repository-code' in pref and 'note' not in pref:
                bibtex_lines.append(f"  note      = {{Repository: {pref['repository-code']}}},")
            
            # Add version info
            if 'version' in pref:
                bibtex_lines.append(f"  version   = {{{pref['version']}}},")
                
            # Add software-specific details as howpublished if not present
            if ('howpublished' not in pref) and ('repository-code' in pref or 'url' in pref):
                repo = pref.get('repository-code', pref.get('url', ''))
                bibtex_lines.append(f"  howpublished = {{Available from: {repo}}},")
                
        # Special handling for websites and blogs
        elif cff_type.lower() in ['website', 'blog']:
            # For websites and blogs, ensure the URL is included
            if 'url' in pref:
                bibtex_lines.append(f"  howpublished = {{\\url{{{pref['url']}}}}},")
                
            # Include last accessed date if available
            if 'date-accessed' in pref:
                bibtex_lines.append(f"  note      = {{Accessed: {pref['date-accessed']}}},")

        # Process all simple fields
        for field in simple_fields:
            if field in pref and field not in ['version', 'institution']:  # Skip already handled fields
                # Sanitize field value to avoid BibTeX syntax errors
                field_value = str(pref[field]).replace('{', '').replace('}', '')
                bibtex_lines.append(f"  {field:<9} = {{{field_value}}},")
        
        # Handle list fields like languages
        if 'languages' in pref and pref['languages']:
            try:
                languages_str = ', '.join(pref['languages'])
                bibtex_lines.append(f"  language  = {{{languages_str}}},")
            except Exception as e:
                logging.warning(f"Error processing languages field: {str(e)}")
                
        # Handle keywords field
        if 'keywords' in pref and pref['keywords']:
            try:
                if isinstance(pref['keywords'], list):
                    keywords_str = ', '.join(pref['keywords'])
                    bibtex_lines.append(f"  keywords  = {{{keywords_str}}},")
            except Exception as e:
                logging.warning(f"Error processing keywords field: {str(e)}")
        
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