#!/usr/bin/env python3
"""
Common utility functions for metadata management in the Quadriga Book Template.
This module provides reused functionality across different metadata scripts.
"""

import yaml
import re
import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# ---- File Path Handling ----

def get_repo_root() -> Path:
    """
    Get the path to the repository root, assuming this module is in quadriga/metadata/.
    
    Returns:
        Path: Absolute path to the repository root
        
    Raises:
        FileNotFoundError: If the repository structure is not as expected
    """
    try:
        quadriga_metadata_dir = Path(__file__).resolve().parent
        quadriga_dir = quadriga_metadata_dir.parent
        repo_root = quadriga_dir.parent
        
        # Verify the path looks like a repository root
        required_files = ['_config.yml', '_toc.yml']
        found_files = [f for f in required_files if (repo_root / f).exists()]
        
        if len(found_files) < 1:
            raise FileNotFoundError(f"Repository root at {repo_root} doesn't contain expected files (_config.yml or _toc.yml)")
            
        return repo_root
    except Exception as e:
        logging.exception(f"Error resolving repository root: {e}")
        raise

def get_file_path(relative_path: str | Path, repo_root: Path | None = None) -> Path:
    """
    Get the absolute path to a file in the repository.
    
    Args:
        relative_path (str | Path): Relative path from the repository root
        repo_root (Path, optional): Repository root path. If None, it will be determined
    
    Returns:
        Path: Absolute path to the file
    """
    try:
        if repo_root is None:
            repo_root = get_repo_root()
        return repo_root / Path(relative_path)
    except Exception as e:
        logging.error(f"Error resolving file path for '{relative_path}': {e}")
        # Return the relative path as a fallback
        return Path(relative_path)

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
    except FileNotFoundError:
        logging.error(f"File not found: {Path(file_path).name}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"YAML parsing error in {Path(file_path).name}: {e}")
        return None
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
                                        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directories if they don't exist
        directory = Path(file_path).parent
        if not directory.exists():
            directory.mkdir(parents=True)
            logging.info(f"Created directory: {directory}")
        
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, sort_keys=False, default_flow_style=False, allow_unicode=True)
        
        if schema_comment:
            try:
                with open(file_path, 'r+', encoding='utf-8') as file:
                    content = file.read()
                    file.seek(0, 0)
                    file.write(f"{schema_comment}\n" + content)
            except Exception as e:
                logging.warning(f"Failed to add schema comment to {Path(file_path).name}: {e}")
                # Not a critical error, proceed
                
        logging.info(f"Successfully updated {Path(file_path).name}")
        return True
    except yaml.YAMLError as e:
        logging.error(f"YAML encoding error for {Path(file_path).name}: {e}")
        return False
    except PermissionError as e:
        logging.error(f"Permission denied when saving {Path(file_path).name}: {e}")
        return False
    except Exception as e:
        logging.error(f"Error saving to {Path(file_path).name}: {e}")
        return False

# ---- Markdown and Jupyter Content Handling ----

def remove_yaml_frontmatter(text: str) -> str:
    """
    Remove YAML frontmatter from markdown content.
    
    YAML frontmatter is expected to be at the beginning of the file
    and delimited by triple dashes (---) on their own lines.
    
    Args:
        text (str): Markdown content that may contain frontmatter
        
    Returns:
        str: Content with frontmatter removed
    """
    pattern = r'^\s*---\s*\n(.*?)\n\s*---\s*(\n|$)'
    return re.sub(pattern, '', text, count=1, flags=re.DOTALL)

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
            try:
                with open(file_path_obj, 'r', encoding='utf-8') as file:
                    notebook = json.load(file)
                    
                for cell in notebook.get('cells', []):
                    if cell.get('cell_type') == 'markdown':
                        content = ''.join(cell.get('source', []))
                        heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                        if heading_match:
                            return heading_match.group(1).strip()
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in notebook {file_path_obj.name}: {e}")
            except Exception as e:
                logging.error(f"Error reading notebook {file_path_obj.name}: {e}")
                
        elif file_path_obj.suffix == '.md':
            try:
                with open(file_path_obj, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                content = remove_yaml_frontmatter(content)
                heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if heading_match:
                    return heading_match.group(1).strip()
            except Exception as e:
                logging.error(f"Error reading markdown {file_path_obj.name}: {e}")
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
    try:
        if not authors:
            logging.warning("No authors provided to format_authors_for_bibtex")
            return ""
            
        formatted_authors = []
        for i, author in enumerate(authors):
            if not isinstance(author, dict):
                logging.warning(f"Author at index {i} is not a dictionary: {author}")
                continue
                
            family = author.get('family-names', '')
            given = author.get('given-names', '')
            
            if not family and not given:
                logging.warning(f"Author at index {i} is missing both family-names and given-names")
                continue
                
            formatted_authors.append(f"{family}, {given}")
            
        return " and ".join(formatted_authors)
    except Exception as e:
        logging.exception(f"Error formatting authors for BibTeX: {e}")
        return ""

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
    try:
        # Get the first author's family name or use 'Unknown'
        if authors and isinstance(authors, list) and authors[0]:
            first_author = authors[0]
            family_name = first_author.get('family-names', 'Unknown')
        else:
            family_name = 'Unknown'
            logging.warning("No valid authors provided for citation key generation")
        
        # Get the first word of the title or use 'Untitled'
        if title and isinstance(title, str):
            title_words = title.split()
            first_word = title_words[0] if title_words else 'Untitled'
        else:
            first_word = 'Untitled'
            logging.warning("No valid title provided for citation key generation")
        
        # Use the year or empty string
        if not year:
            logging.warning("No year provided for citation key generation")
            year = ""
            
        # Create a citation key with no invalid characters
        raw_key = f"{family_name}_{first_word}_{year}"
        
        # Clean the key - remove special characters
        clean_key = re.sub(r'[^a-zA-Z0-9_]', '', raw_key)
        
        return clean_key or "Unknown_Citation"
    except Exception as e:
        logging.exception(f"Error generating citation key: {e}")
        return "Unknown_Citation_Error"
