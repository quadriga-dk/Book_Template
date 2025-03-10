#!/usr/bin/env python3
import yaml
import json
import re
from pathlib import Path

def update_metadata():
    # Load CITATION.cff
    with open('CITATION.cff', 'r') as f:
        citation_data = yaml.safe_load(f)
    
    # Load _toc.yml
    with open('_toc.yml', 'r') as f:
        toc_data = yaml.safe_load(f)
    
    # Load existing metadata.yml
    with open('metadata.yml', 'r') as f:
        metadata = yaml.safe_load(f)
    
    # Update metadata fields based on citation and toc
    if 'title' in citation_data:
        metadata['title'] = citation_data['title']
    
    if 'authors' in citation_data:
        # Convert citation authors format to metadata authors format
        metadata_authors = []
        for author in citation_data['authors']:
            author_entry = {}
            if 'given-names' in author:
                author_entry['given-name'] = author['given-names']
            if 'family-names' in author:
                author_entry['familyname'] = author['family-names']
            if 'orcid' in author:
                author_entry['orcid'] = author['orcid']
            if 'affiliation' in author:
                author_entry['affiliations'] = [author['affiliation']]
            metadata_authors.append(author_entry)
        metadata['authors'] = metadata_authors

    # Save updated metadata.yml
    with open('metadata.yml', 'w') as f:
        f.write("# yaml-language-server: $schema=quadriga-schema.json\n")
        yaml.dump(metadata, f, sort_keys=False, default_flow_style=False)
if __name__ == "__main__":
    update_metadata()