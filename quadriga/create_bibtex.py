#!/usr/bin/env python3
import yaml
import sys

def create_bibtex_from_cff():
    # Read CITATION.cff
    with open('CITATION.cff', 'r', encoding='utf-8') as f:
        citation_data = yaml.safe_load(f)
    
    # Extract data from preferred-citation
    pref = citation_data.get('preferred-citation', citation_data)
    
    # Create BibTeX entry
    authors = pref.get('authors', [])
    author_str = " and ".join([f"{a.get('family-names', '')}, {a.get('given-names', '')}" for a in authors])
    
    # Choose entry type based on type field
    entry_type = 'book' if pref.get('type') == 'book' else 'misc'
    
    # Generate citation key
    first_author = authors[0] if authors else {'family-names': 'Unknown'}
    year = pref.get('year', '')
    title_words = pref.get('title', '').split()
    citation_key = f"{first_author.get('family-names', 'Unknown')}_{title_words[0] if title_words else 'Untitled'}_{year}"
    
    # Compile BibTeX entry
    bibtex = f"@{entry_type}{{{citation_key},\n"
    
    # Add fields
    if 'title' in pref:
        bibtex += f"  title     = {{{pref['title']}}},\n"
    if author_str:
        bibtex += f"  author    = {{{author_str}}},\n"
    if 'year' in pref:
        bibtex += f"  year      = {{{pref['year']}}},\n"
    if 'doi' in pref:
        bibtex += f"  doi       = {{{pref['doi']}}},\n"
    if 'url' in pref:
        bibtex += f"  url       = {{{pref['url']}}},\n"
    if 'languages' in pref:
        bibtex += f"  language  = {{{', '.join(pref['languages'])}}},\n"
    if 'copyright' in pref:
        bibtex += f"  copyright = {{{pref['copyright']}}},\n"
        
    
    
    # Add additional fields that might be present
    for field in ['publisher', 'address', 'edition', 'isbn', 'language']:
        if field in pref:
            bibtex += f"  {field:<9} = {{{pref[field]}}},\n"
    
    # Close the entry
    bibtex += "}"
    
    # Write to CITATION.bib
    with open('CITATION.bib', 'w', encoding='utf-8') as f:
        f.write(bibtex)
    
    print("BibTeX citation created successfully")

if __name__ == "__main__":
    create_bibtex_from_cff()