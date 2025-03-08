"""
CoderAI Framework File Tools
This module provides file operation tools for the CoderAI framework.
"""

import os
import glob
import shutil
from typing import List, Optional, Dict, Any
from pathlib import Path
from ..registry import registry

@registry.register(type="tool")
def read_file(file_path: str, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Dictionary containing the file contents and metadata
    """
    try:
        # Expand user directory if needed
        file_path = os.path.expanduser(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File '{file_path}' does not exist",
            }
            
        # Check if path is a file
        if not os.path.isfile(file_path):
            return {
                "success": False,
                "error": f"Path '{file_path}' is not a file",
            }
            
        # Read file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Get file metadata
        stat = os.stat(file_path)
        
        return {
            "success": True,
            "content": content,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def write_file(file_path: str, content: str, overwrite: bool = False, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        overwrite: Whether to overwrite the file if it exists
        
    Returns:
        Dictionary indicating success or failure
    """
    try:
        # Expand user directory if needed
        file_path = os.path.expanduser(file_path)
        
        # Check if file exists
        if os.path.exists(file_path) and not overwrite:
            return {
                "success": False,
                "error": f"File '{file_path}' already exists and overwrite is False",
            }
            
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Write file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return {
            "success": True,
            "path": file_path,
            "size": len(content),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def append_file(file_path: str, content: str, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Append content to a file.
    
    Args:
        file_path: Path to the file to append to
        content: Content to append to the file
        
    Returns:
        Dictionary indicating success or failure
    """
    try:
        # Expand user directory if needed
        file_path = os.path.expanduser(file_path)
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Append to file
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
            
        return {
            "success": True,
            "path": file_path,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def delete_file(file_path: str, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Delete a file.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        Dictionary indicating success or failure
    """
    try:
        # Expand user directory if needed
        file_path = os.path.expanduser(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File '{file_path}' does not exist",
            }
            
        # Check if path is a file
        if not os.path.isfile(file_path):
            return {
                "success": False,
                "error": f"Path '{file_path}' is not a file",
            }
            
        # Delete file
        os.remove(file_path)
        
        return {
            "success": True,
            "path": file_path,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def list_files(directory: str, pattern: str = "*", recursive: bool = False, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    List files in a directory.
    
    Args:
        directory: Directory to list files in
        pattern: Pattern to match files against
        recursive: Whether to list files recursively
        
    Returns:
        Dictionary containing the list of files
    """
    try:
        # Expand user directory if needed
        directory = os.path.expanduser(directory)
        
        # Check if directory exists
        if not os.path.exists(directory):
            return {
                "success": False,
                "error": f"Directory '{directory}' does not exist",
            }
            
        # Check if path is a directory
        if not os.path.isdir(directory):
            return {
                "success": False,
                "error": f"Path '{directory}' is not a directory",
            }
            
        # List files
        if recursive:
            files = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
        else:
            files = glob.glob(os.path.join(directory, pattern))
            
        # Get file metadata
        file_info = []
        for file_path in files:
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                file_info.append({
                    "path": file_path,
                    "name": os.path.basename(file_path),
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "created": stat.st_ctime,
                })
                
        return {
            "success": True,
            "files": file_info,
            "count": len(file_info),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def search_files(directory: str, content: str, pattern: str = "*", recursive: bool = True, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Search for files containing specific content.
    
    Args:
        directory: Directory to search in
        content: Content to search for
        pattern: Pattern to match files against
        recursive: Whether to search recursively
        
    Returns:
        Dictionary containing the list of matching files
    """
    try:
        # Expand user directory if needed
        directory = os.path.expanduser(directory)
        
        # Check if directory exists
        if not os.path.exists(directory):
            return {
                "success": False,
                "error": f"Directory '{directory}' does not exist",
            }
            
        # Check if path is a directory
        if not os.path.isdir(directory):
            return {
                "success": False,
                "error": f"Path '{directory}' is not a directory",
            }
            
        # List files
        if recursive:
            files = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
        else:
            files = glob.glob(os.path.join(directory, pattern))
            
        # Search for content
        matches = []
        for file_path in files:
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        
                    if content in file_content:
                        stat = os.stat(file_path)
                        matches.append({
                            "path": file_path,
                            "name": os.path.basename(file_path),
                            "size": stat.st_size,
                            "modified": stat.st_mtime,
                            "created": stat.st_ctime,
                        })
                except:
                    # Skip files that can't be read as text
                    pass
                    
        return {
            "success": True,
            "matches": matches,
            "count": len(matches),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
