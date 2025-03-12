#!/usr/bin/env python3
import yaml
import json
import re
from pathlib import Path

def update_citation():
    """Update CITATION.cff using data from metadata.yml"""
    # Load metadata.yml
    with open('metadata.yml', 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
    
    # Load existing CITATION.cff
    with open('CITATION.cff', 'r', encoding='utf-8') as f:
        citation_data = yaml.safe_load(f)
    
    # Update citation fields based on metadata
    if 'title' in metadata:
        citation_data['title'] = metadata['title']
        # Also update preferred-citation if it exists
        if 'preferred-citation' in citation_data:
            citation_data['preferred-citation']['title'] = metadata['title']
    
    if 'authors' in metadata:
        # Convert metadata authors format to citation authors format
        citation_authors = []
        for author in metadata['authors']:
            new_author_entry = {}
            # Copy existing citation data for authors entry if exists
            for cit_author in citation_data.get('authors', []):
                if ('given-names' in cit_author and 'family-names' in cit_author and 
                    'given-names' in author and 'family-names' in author):
                    if (cit_author['given-names'] == author['given-names'] and 
                        cit_author['family-names'] == author['family-names']):
                        new_author_entry = cit_author
                        break
            
            # Update author entry with metadata
            if 'given-names' in author:
                new_author_entry['given-names'] = author['given-names']
            if 'family-names' in author:
                new_author_entry['family-names'] = author['family-names']
            if 'orcid' in author:
                new_author_entry['orcid'] = author['orcid']
            if 'affiliation' in author:
                new_author_entry['affiliation'] = author['affiliation']
            citation_authors.append(new_author_entry)
        
        citation_data['authors'] = citation_authors
        
        # Also update preferred-citation if it exists
        if 'preferred-citation' in citation_data:
            citation_data['preferred-citation']['authors'] = citation_authors
    
    # Update URL if present in metadata
    if 'url' in metadata:
        citation_data['url'] = metadata['url']
        if 'preferred-citation' in citation_data:
            citation_data['preferred-citation']['url'] = metadata['url']
    
    # Update repository URL if present in metadata
    if 'git' in metadata:
        citation_data['repository-code'] = metadata['git']
        if 'preferred-citation' in citation_data:
            citation_data['preferred-citation']['repository-code'] = metadata['git']
    
    # Update publication date if it exists
    if 'publication-date' in metadata:
        pub_date = metadata['publication-date']
        if isinstance(pub_date, str) and len(pub_date) >= 4:
            year = pub_date[:4]  # Extract year from YYYY-MM-DD
            if 'preferred-citation' in citation_data:
                citation_data['preferred-citation']['year'] = year
    
    # Save updated CITATION.cff
    with open('CITATION.cff', 'w', encoding='utf-8') as f:
        f.write("# yaml-language-server: $schema=https://citation-file-format.github.io/1.2.0/schema.json\n")
        yaml.dump(citation_data, f, encoding='utf-8', default_flow_style=False, 
                 width=100, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    update_citation()