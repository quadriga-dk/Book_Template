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
            new_author_entry = {}
            # Copy existing metadata for authors entry
            for meta_author in metadata['authors']:
                if 'given-names' in meta_author and 'family-names' in meta_author:
                    if meta_author['given-names'] == author['given-names'] and meta_author['family-names'] == author['family-names']:
                        new_author_entry = meta_author
                        break
            # Update author entry with citation data
            if 'given-names' in author:
                new_author_entry['given-names'] = author['given-names']
            if 'family-names' in author:
                new_author_entry['family-names'] = author['family-names']
            if 'orcid' in author:
                new_author_entry['orcid'] = author['orcid']
            if 'affiliation' in author:
                new_author_entry['affiliation'] = author['affiliation']
            metadata_authors.append(new_author_entry)
        metadata['authors'] = metadata_authors

    # Save updated metadata.yml
    with open('metadata.yml', 'w') as f:
        f.write("# yaml-language-server: $schema=quadriga-schema.json\n")
        yaml.dump(metadata, f, encoding="utf-8", default_flow_style=False, width=1000, allow_unicode=True)
if __name__ == "__main__":
    update_metadata()