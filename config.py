from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class AppConfig(BaseModel):
    """Application configuration settings"""
    # Default models
    default_ollama_model: str = "llama3.2:1b"
    default_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # UI settings
    theme: str = "light"
    max_chat_history: int = 500
    
    # File handling
    allowed_extensions: List[str] = ["pdf", "txt", "docx", "md"]
    max_file_size_mb: int = 100
    
    # Vector database settings
    vector_db_path: str = "./data/vector_db"
    embedding_dimension: int = 384  # Default for all-MiniLM-L6-v2
    
    # API settings
    api_timeout: int = 30
    max_retries: int = 3
    
    # Model provider settings
    provider_configs: Dict[str, Dict[str, Any]] = {
        "ollama": {
            "base_url": "http://localhost:11434",
            "available_models": [
                "llama3.2:1b", "mistral", "gemma", "phi", "codellama"
            ]
        },
        "openai": {
            "available_models": [
                "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"
            ]
        },
        "anthropic": {
            "available_models": [
                "claude-3-haiku-20240307 1", "claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022", "claude-3-5-sonnet-20241022", "claude-3-7-sonnet-20250219"
            ]
        },
        "huggingface": {
            "available_embedding_models": [
                "sentence-transformers/all-MiniLM-L6-v2",
                "sentence-transformers/all-mpnet-base-v2",
                "sentence-transformers/multi-qa-mpnet-base-dot-v1"
            ]
        }
    }
