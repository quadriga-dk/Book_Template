#!/usr/bin/env python3
"""
Common utility functions for metadata management in the Quadriga Book Template.
This module provides reused functionality across different metadata scripts.
"""

import yaml
import re
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# ---- File Path Handling ----

def get_repo_root() -> Path:
    """
    Get the path to the repository root, assuming this module is in quadriga/metadata/.
    
    Returns:
        Path: Absolute path to the repository root
    """
    quadriga_metadata_dir = Path(__file__).resolve().parent
    quadriga_dir = quadriga_metadata_dir.parent
    repo_root = quadriga_dir.parent
    return repo_root

def get_file_path(relative_path: str | Path, repo_root: Path | None = None) -> Path:
    """
    Get the absolute path to a file in the repository.
    
    Args:
        relative_path (str | Path): Relative path from the repository root
        repo_root (Path, optional): Repository root path. If None, it will be determined
    
    Returns:
        Path: Absolute path to the file
    """
    if repo_root is None:
        repo_root = get_repo_root()
    return repo_root / Path(relative_path)

# ---- YAML Handling ----

def load_yaml_file(file_path: str | Path):
    """
    Load a YAML file and return its contents as a Python object.
    
    Args:
        file_path (str | Path): Path to the YAML file
        
    Returns:
        dict/list: Contents of the YAML file, or None if an error occurs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading {Path(file_path).name}: {e}")
        return None

def save_yaml_file(file_path: str | Path, data, schema_comment: str | None = None):
    """
    Save Python object as YAML to the specified file.
    
    Args:
        file_path (str | Path): Path where the YAML file should be saved
        data (dict/list): Data to save
        schema_comment (str, optional): Schema comment to add at the start of the file
                                           e.g. "# yaml-language-server: $schema=quadriga-schema.json"
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, sort_keys=False, default_flow_style=False, allow_unicode=True)
        
        if schema_comment:
            with open(file_path, 'r+', encoding='utf-8') as file:
                content = file.read()
                file.seek(0, 0)
                file.write(f"{schema_comment}\n" + content)
                
        logging.info(f"Successfully updated {Path(file_path).name}")
    except Exception as e:
        logging.error(f"Error saving to {Path(file_path).name}: {e}")

# ---- Markdown and Jupyter Content Handling ----

def extract_first_heading(file_path: str | Path) -> str:
    """
    Extract the first heading from a markdown or jupyter notebook file.
    
    Args:
        file_path (str | Path): Path to the file
        
    Returns:
        str: The content of the first heading or filename if no heading found
    """
    file_path_obj = Path(file_path)
    try:
        if file_path_obj.suffix == '.ipynb':
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                notebook = json.load(file)
                
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    content = ''.join(cell.get('source', []))
                    heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    if heading_match:
                        return heading_match.group(1).strip()
        elif file_path_obj.suffix == '.md':
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                content = file.read()
            
            content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if heading_match:
                return heading_match.group(1).strip()
        else:
            logging.warning(f"Unsupported file type for heading extraction: {file_path_obj.name}")
            return file_path_obj.stem

    except FileNotFoundError:
        logging.error(f"File not found: {file_path_obj.name}")
    except Exception as e:
        logging.error(f"Error processing {file_path_obj.name}: {e}")
    
    return file_path_obj.stem

# ---- Citation Handling ----

def format_authors_for_bibtex(authors):
    """
    Format a list of authors in the proper BibTeX format.
    
    Args:
        authors (list): List of author dictionaries with 'given-names' and 'family-names'
        
    Returns:
        str: Authors formatted for BibTeX
    """
    return " and ".join([f"{a.get('family-names', '')}, {a.get('given-names', '')}" for a in authors])

def generate_citation_key(authors, title, year):
    """
    Generate a citation key for BibTeX.
    
    Args:
        authors (list): List of author dictionaries
        title (str): Title of the work
        year (str): Year of publication
        
    Returns:
        str: Citation key
    """
    first_author = authors[0] if authors else {'family-names': 'Unknown'}
    title_words = title.split()
    return f"{first_author.get('family-names', 'Unknown')}_{title_words[0] if title_words else 'Untitled'}_{year}"
