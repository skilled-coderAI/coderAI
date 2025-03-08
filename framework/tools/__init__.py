"""
CoderAI Framework Tools
This module provides tools for the CoderAI framework.
"""

# Import tool modules
from . import file_tools
from . import web_tools
from . import terminal_tools
from . import rag_tools

# Import all tools
from .file_tools import *
from .web_tools import *
from .terminal_tools import *
from .rag_tools import *

__all__ = [
    # File tools
    "read_file",
    "write_file",
    "append_file",
    "delete_file",
    "list_files",
    "search_files",
    
    # Web tools
    "search_web",
    "read_url",
    "download_file",
    
    # Terminal tools
    "run_command",
    "run_python",
    "run_script",
    
    # RAG tools
    "add_document",
    "search_documents",
    "delete_document",
]
