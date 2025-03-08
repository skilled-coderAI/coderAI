"""
CoderAI Framework Web Tools
This module provides web operation tools for the CoderAI framework.
"""

import os
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from ..registry import registry

@registry.register(type="tool")
def search_web(query: str, num_results: int = 5, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Search the web for information.
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        Dictionary containing search results
    """
    try:
        # Check if API key is available
        api_key = os.environ.get("SERP_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "SERP API key not found. Please set the SERP_API_KEY environment variable.",
            }
            
        # Prepare request
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": api_key,
            "num": num_results,
        }
        
        # Send request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Extract organic results
        results = []
        if "organic_results" in data:
            for result in data["organic_results"][:num_results]:
                results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                })
                
        return {
            "success": True,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def read_url(url: str, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Read content from a URL.
    
    Args:
        url: URL to read content from
        
    Returns:
        Dictionary containing the URL content
    """
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return {
                "success": False,
                "error": f"Invalid URL: {url}",
            }
            
        # Send request
        headers = {
            "User-Agent": "CoderAI/1.0",
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Get content type
        content_type = response.headers.get("Content-Type", "")
        
        # Check if content is text
        if "text" in content_type or "json" in content_type or "xml" in content_type:
            content = response.text
        else:
            content = f"Binary content (Content-Type: {content_type})"
            
        return {
            "success": True,
            "content": content,
            "content_type": content_type,
            "status_code": response.status_code,
            "url": response.url,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def download_file(url: str, output_path: str, overwrite: bool = False, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Download a file from a URL.
    
    Args:
        url: URL to download file from
        output_path: Path to save the file to
        overwrite: Whether to overwrite the file if it exists
        
    Returns:
        Dictionary indicating success or failure
    """
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return {
                "success": False,
                "error": f"Invalid URL: {url}",
            }
            
        # Expand user directory if needed
        output_path = os.path.expanduser(output_path)
        
        # Check if file exists
        if os.path.exists(output_path) and not overwrite:
            return {
                "success": False,
                "error": f"File '{output_path}' already exists and overwrite is False",
            }
            
        # Create directory if it doesn't exist
        directory = os.path.dirname(output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Send request
        headers = {
            "User-Agent": "CoderAI/1.0",
        }
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        # Get content length
        content_length = int(response.headers.get("Content-Length", 0))
        
        # Download file
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Get file size
        file_size = os.path.getsize(output_path)
        
        return {
            "success": True,
            "path": output_path,
            "size": file_size,
            "content_type": response.headers.get("Content-Type", ""),
            "url": response.url,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
