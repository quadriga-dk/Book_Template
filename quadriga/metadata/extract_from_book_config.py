"""
This script extracts the title from _config.yml and the first level of the TOC from _toc.yml.
It then uses this information to update metadata.yml.
The titles for the TOC chapters are extracted from the first heading of the corresponding files.
"""

import yaml
import os
import re
from datetime import datetime

def load_yaml_file(file_path):
    """Load a YAML file and return its contents as a Python object."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def save_yaml_file(file_path, data):
    """Save Python object as YAML to the specified file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"Successfully updated {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")

def extract_first_heading(file_path):
    """Extract the first heading from a markdown or jupyter notebook file."""
    try:
        # Handle both .md and .ipynb files
        if file_path.endswith('.ipynb'):
            # For Jupyter notebooks, parse the JSON to find the first heading
            import json
            with open(file_path, 'r', encoding='utf-8') as file:
                notebook = json.load(file)
                
            # Look for the first markdown cell with a heading
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    content = ''.join(cell.get('source', []))
                    heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    if heading_match:
                        return heading_match.group(1).strip()
        else:
            # For markdown files
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Skip YAML frontmatter if it exists
            content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            
            # Extract the first heading
            heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if heading_match:
                return heading_match.group(1).strip()
    except Exception as e:
        print(f"Error extracting heading from {file_path}: {e}")
    
    # If we couldn't find a heading, return the filename
    return os.path.splitext(os.path.basename(file_path))[0]

def extract_and_update():
    """
    Extract information from _config.yml and _toc.yml files and update metadata.yml.
    """
    # Get the repository root directory (assuming the script is in a subdirectory of /quadriga)
    quadriga_metadata_dir = os.path.dirname(os.path.abspath(__file__))
    quadriga_dir = os.path.dirname(quadriga_metadata_dir)
    repo_root = os.path.dirname(quadriga_dir)
    
    # Define file paths
    config_path = os.path.join(repo_root, '_config.yml')
    toc_path = os.path.join(repo_root, '_toc.yml')
    metadata_path = os.path.join(repo_root, 'metadata.yml')
    
    # Load the files
    config_data = load_yaml_file(config_path)
    toc_data = load_yaml_file(toc_path)
    metadata_data = load_yaml_file(metadata_path)
    
    if not all([config_data, toc_data, metadata_data]):
        print("One or more required files couldn't be loaded. Exiting.")
        return
    
    # Extract information from _config.yml
    title = config_data.get('title', '')
    author = config_data.get('author', '')
    
    # Extract chapters and their titles from _toc.yml
    toc_chapters = []
    if 'chapters' in toc_data:
        for chapter in toc_data['chapters']:
            if 'file' in chapter:
                # Get the file path
                file_path = chapter['file']
                
                # Ensure the file has an extension (default to .md if none)
                if not file_path.endswith(('.md', '.ipynb')):
                    file_path += '.md'
                
                # Create the full path to the file
                full_path = os.path.join(repo_root, file_path)
                
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
        save_yaml_file(metadata_path, metadata_data)
        # prepend the comment to configure the yaml-lsp to use quadriga-schema.json
        with open(metadata_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0, 0)
            file.write("# yaml-language-server: $schema=quadriga-schema.json\n" + content)
        print("Metadata updated successfully!")
    else:
        print("Metadata file couldn't be loaded or is empty.")

if __name__ == "__main__":
    extract_and_update()
