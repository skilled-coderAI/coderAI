import requests
import json
from typing import Dict, List, Any, Optional
from .base_model import BaseModel

class OllamaModel(BaseModel):
    """Integration with Ollama models"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama model
        
        Args:
            base_url: Base URL for the Ollama API
        """
        self.base_url = base_url
    
    def query(self, 
             prompt: str, 
             model: str = "llama2",
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Query an Ollama model
        
        Args:
            prompt: The user prompt
            model: The model name
            system_prompt: Optional system prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response from the model
        """
        # Prepare request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            # Make request to Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            return {
                "text": result.get("response", ""),
                "model": model,
                "provider": self.provider_name,
                "tokens_used": result.get("eval_count", 0)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "model": model,
                "provider": self.provider_name
            }
    
    def get_available_models(self) -> List[str]:
        """
        Get a list of available models from Ollama
        
        Returns:
            List of model names
        """
        try:
            # Make request to Ollama API
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            # Extract model names
            models = [model["name"] for model in result.get("models", [])]
            
            return models
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting available models: {e}")
            return []
    
    @property
    def provider_name(self) -> str:
        """
        Get the provider name
        
        Returns:
            Provider name
        """
        return "ollama"
