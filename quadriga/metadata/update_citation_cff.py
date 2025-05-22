#!/usr/bin/env python3
"""
Updates the CITATION.cff file with metadata from metadata.yml.

This script reads metadata from 'metadata.yml' and updates the corresponding
fields in 'CITATION.cff'. It handles fields like title, authors, URL, 
repository URL, and publication date. It also ensures that the 
'preferred-citation' section, if present, is updated consistently.
"""
import logging
from .utils import load_yaml_file, save_yaml_file, get_file_path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def update_citation():
    """
    Updates the CITATION.cff file using data from the metadata.yml file.

    The function performs the following steps:
    1.  Constructs absolute paths to 'metadata.yml' and 'CITATION.cff'.
    2.  Loads data from both YAML files.
    3.  Updates 'CITATION.cff' fields (title, authors, URL, repository-code, 
        and publication year in preferred-citation) based on 'metadata.yml'.
    4.  For authors, it attempts to preserve existing author details in 
        'CITATION.cff' if a matching author (by given and family names) is found.
    5.  Saves the updated data back to 'CITATION.cff', including a schema comment.
    
    If 'metadata.yml' or 'CITATION.cff' cannot be loaded, an error message is
    printed, and the function returns without making changes.
    """
    # Define file paths 
    repo_root = get_file_path('')  # Get repo root by providing empty relative path
    metadata_path = get_file_path('metadata.yml', repo_root)
    citation_cff_path = get_file_path('CITATION.cff', repo_root)

    # Load metadata.yml
    metadata = load_yaml_file(metadata_path)
    
    # Load existing CITATION.cff
    citation_data = load_yaml_file(citation_cff_path)

    if not metadata or not citation_data:
        logging.error("Could not load metadata.yml or CITATION.cff. Exiting.")
        return
    
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
    save_yaml_file(citation_cff_path, citation_data, schema_comment="# yaml-language-server: $schema=https://citation-file-format.github.io/1.2.0/schema.json")

if __name__ == "__main__":
    update_citation()