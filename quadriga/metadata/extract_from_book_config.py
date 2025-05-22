"""
This script extracts the title from _config.yml and the first level of the TOC from _toc.yml.
It then uses this information to update metadata.yml.
The titles for the TOC chapters are extracted from the first heading of the corresponding files.
"""

from pathlib import Path  
import logging  
from datetime import datetime
from .utils import (
    get_repo_root,
    get_file_path,
    load_yaml_file,
    save_yaml_file,
    extract_first_heading
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def extract_and_update():
    """
    Extract information from _config.yml and _toc.yml files and update metadata.yml.
    """
    # Get the repository root directory
    repo_root = get_repo_root()
    
    # Define file paths using the get_file_path utility function
    config_path = get_file_path('_config.yml', repo_root)
    toc_path = get_file_path('_toc.yml', repo_root)
    metadata_path = get_file_path('metadata.yml', repo_root)
    
    # Load the files
    config_data = load_yaml_file(config_path)
    toc_data = load_yaml_file(toc_path)
    metadata_data = load_yaml_file(metadata_path)
    
    if not all([config_data, toc_data, metadata_data]):
        logging.error("One or more required files couldn't be loaded. Exiting.")
        return
    
    # Extract information from _config.yml
    title = config_data.get('title', '')
    author = config_data.get('author', '')
    
    # Extract chapters and their titles from _toc.yml
    toc_chapters = []
    if 'chapters' in toc_data:
        for chapter in toc_data['chapters']:
            if 'file' in chapter:
                # Get the file path as a Path object
                file_path_str = chapter['file']
                p = Path(file_path_str)
                
                # Ensure the file has an extension (default to .md if none)
                if p.suffix not in ['.md', '.ipynb']:
                    p = p.with_suffix('.md')
                
                # Create the full path to the file 
                full_path = get_file_path(p, repo_root)
                
                # Extract the chapter title from the file's first heading 
                chapter_title = extract_first_heading(full_path)
                
                # Add to the list of chapters
                toc_chapters.append(chapter_title)
    
    # Format the TOC as a string with proper indentation and single newline between items
    toc_formatted = "- " + "\n- ".join(toc_chapters)
    
    # Update metadata.yml
    if metadata_data:
        # Update the title if it doesn't already have the full title
        if 'title' in metadata_data and not metadata_data['title'].startswith(config_data.get('title', '')):
            metadata_data['title'] = f"{config_data.get('title', '')}. {metadata_data['title']}"
        
        # Update the description table of contents
        if 'description' in metadata_data:
            metadata_data['description']['table-of-contents'] = toc_formatted
        
        # Save the updated metadata 
        save_yaml_file(metadata_path, metadata_data, schema_comment="# yaml-language-server: $schema=quadriga-schema.json")
        logging.info("Metadata updated successfully!")
    else:
        logging.error("Metadata file couldn't be loaded or is empty.")

if __name__ == "__main__":
    extract_and_update()
