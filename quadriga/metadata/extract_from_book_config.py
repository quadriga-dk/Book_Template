"""
This script extracts the title from _config.yml and the first level of the TOC from _toc.yml.
It then uses this information to update metadata.yml.
The titles for the TOC chapters are extracted from the first heading of the corresponding files.
"""

from pathlib import Path  
import logging
import sys
from datetime import datetime
from .utils import (
    get_repo_root,
    get_file_path,
    load_yaml_file,
    save_yaml_file,
    extract_first_heading
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def extract_and_update():
    """
    Extract information from _config.yml and _toc.yml files and update metadata.yml.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Get the repository root directory
        try:
            repo_root = get_repo_root()
        except Exception as e:
            logging.error(f"Failed to get repository root: {e}")
            return False
        
        # Define file paths using the get_file_path utility function
        config_path = get_file_path('_config.yml', repo_root)
        toc_path = get_file_path('_toc.yml', repo_root)
        metadata_path = get_file_path('metadata.yml', repo_root)
        
        # Verify files exist before loading
        for path, name in [(config_path, "_config.yml"), (toc_path, "_toc.yml"), (metadata_path, "metadata.yml")]:
            if not path.exists():
                logging.error(f"Required file {name} not found at {path}")
                return False
        
        # Load the files
        config_data = load_yaml_file(config_path)
        toc_data = load_yaml_file(toc_path)
        metadata_data = load_yaml_file(metadata_path)
        
        if not all([config_data, toc_data, metadata_data]):
            logging.error("One or more required files couldn't be loaded. Exiting.")
            return False
        
        # Extract information from _config.yml
        title = config_data.get('title', '')
        author = config_data.get('author', '')
        
        if not title:
            logging.warning("No title found in _config.yml")
        
        # Extract chapters and their titles from _toc.yml
        toc_chapters = []
        missing_files = []
        
        if 'chapters' not in toc_data:
            logging.warning("No 'chapters' section found in _toc.yml")
        else:
            for chapter in toc_data['chapters']:
                if 'file' not in chapter:
                    logging.warning("Found chapter entry without 'file' attribute in _toc.yml")
                    continue
                
                try:
                    # Get the file path as a Path object
                    file_path_str = chapter['file']
                    p = Path(file_path_str)
                    
                    # Ensure the file has an extension (default to .md if none)
                    if p.suffix not in ['.md', '.ipynb']:
                        p = p.with_suffix('.md')
                    
                    # Create the full path to the file 
                    full_path = get_file_path(p, repo_root)
                    
                    # Check if file exists
                    if not full_path.exists():
                        missing_files.append(str(full_path))
                        logging.warning(f"Chapter file not found: {full_path}")
                        # Use filename as fallback title
                        toc_chapters.append(f"[Missing: {p.stem}]")
                        continue
                    
                    # Extract the chapter title from the file's first heading 
                    chapter_title = extract_first_heading(full_path)
                    
                    # Add to the list of chapters
                    toc_chapters.append(chapter_title)
                except Exception as e:
                    logging.error(f"Error processing chapter {chapter.get('file', 'unknown')}: {e}")
                    # Add a placeholder with the filename if possible
                    try:
                        toc_chapters.append(f"[Error: {p.stem}]")
                    except:
                        toc_chapters.append("[Error: unknown chapter]")
        
        if missing_files:
            logging.warning(f"Missing {len(missing_files)} chapter files")
        
        if not toc_chapters:
            logging.warning("No chapter titles were extracted")
        
        # Format the TOC as a string with proper indentation and single newline between items
        toc_formatted = "- " + "\n- ".join(toc_chapters)
        
        # Update metadata.yml
        if metadata_data:
            try:
                # Update the title if it doesn't already have the full title
                if 'title' in metadata_data and title and not metadata_data['title'].startswith(title):
                    metadata_data['title'] = f"{title}. {metadata_data['title']}"
                
                # Update the description table of contents
                if 'description' in metadata_data:
                    if isinstance(metadata_data['description'], dict):
                        metadata_data['description']['table-of-contents'] = toc_formatted
                    else:
                        logging.error("'description' in metadata.yml is not a dictionary")
                        return False
                else:
                    logging.warning("No 'description' field found in metadata.yml")
                
                # Save the updated metadata 
                if save_yaml_file(metadata_path, metadata_data, schema_comment="# yaml-language-server: $schema=quadriga-schema.json"):
                    logging.info("Metadata updated successfully!")
                    return True
                else:
                    logging.error("Failed to save metadata.yml")
                    return False
            except Exception as e:
                logging.exception(f"Error updating metadata.yml: {e}")
                return False
        else:
            logging.error("Metadata file couldn't be loaded or is empty.")
            return False
            
    except Exception as e:
        logging.exception(f"Unexpected error in extract_and_update: {e}")
        return False

if __name__ == "__main__":
    success = extract_and_update()
    sys.exit(0 if success else 1)
