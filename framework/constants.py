"""
CoderAI Framework Constants
This module defines constants used throughout the CoderAI framework.
"""

import os

# Framework mode
MC_MODE = os.environ.get("MC_MODE", "False").lower() in ("true", "1", "t")

# Function calling mode
FN_CALL = os.environ.get("FN_CALL", "True").lower() in ("true", "1", "t")
NON_FN_CALL = os.environ.get("NON_FN_CALL", "False").lower() in ("true", "1", "t")

# API configuration
API_BASE_URL = os.environ.get("API_BASE_URL", None)

# Models that don't support sender field
NOT_SUPPORT_SENDER = ["claude", "gemini", "llama", "mistral", "anthropic"]

# User interleaving
ADD_USER = os.environ.get("ADD_USER", "False").lower() in ("true", "1", "t")

# Default models
DEFAULT_MODEL = "gpt-4o"
DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"

# Memory settings
DEFAULT_MEMORY_SIZE = 10
DEFAULT_MEMORY_K = 5

# RAG settings
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

# Tool registry settings
DEFAULT_TOOL_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "tools")

# Agent registry settings
DEFAULT_AGENT_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "agents")

# Workflow settings
DEFAULT_WORKFLOW_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "workflows")

# CLI settings
DEFAULT_CLI_HISTORY_PATH = os.path.join(os.path.expanduser("~"), ".coderAI", "history.json")
DEFAULT_CLI_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".coderAI", "config.json")

# File extensions
CODE_FILE_EXTENSIONS = [
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".hpp",
    ".cs", ".go", ".rb", ".php", ".swift", ".kt", ".rs", ".scala", ".sh",
    ".bash", ".ps1", ".html", ".css", ".scss", ".sass", ".less", ".sql",
    ".r", ".dart", ".lua", ".pl", ".pm", ".groovy", ".yaml", ".yml", ".json",
    ".xml", ".toml", ".ini", ".cfg", ".conf", ".md", ".rst", ".tex"
]

# Documentation settings
DEFAULT_DOCS_OUTPUT_PATH = "docs"
DEFAULT_DOCS_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "docs")

# Visualization settings
DEFAULT_VIZ_OUTPUT_PATH = "visualizations"
DEFAULT_VIZ_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "viz")
