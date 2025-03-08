import requests
import json
import os
from typing import Dict, List, Any, Optional

class ModelService:
    """Service for interacting with various AI model providers"""
    
    def __init__(self):
        """Initialize the model service"""
        self.providers = {}
    
    def set_provider_config(self, provider_configs: Dict[str, Dict[str, Any]]):
        """Set the provider configurations"""
        self.providers = provider_configs
    
    def query_ollama(self, 
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
        if not self.providers.get("ollama", {}).get("active", False):
            raise ValueError("Ollama provider is not active")
        
        base_url = self.providers.get("ollama", {}).get("base_url", "http://localhost:11434")
        
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
                f"{base_url}/api/generate",
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
                "provider": "ollama",
                "tokens_used": result.get("eval_count", 0)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "model": model,
                "provider": "ollama"
            }
    
    def query_openai(self, 
                    prompt: str, 
                    model: str = "gpt-3.5-turbo", 
                    system_prompt: Optional[str] = None,
                    temperature: float = 0.7,
                    max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Query an OpenAI model
        
        Args:
            prompt: The user prompt
            model: The model name
            system_prompt: Optional system prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response from the model
        """
        if not self.providers.get("openai", {}).get("active", False):
            raise ValueError("OpenAI provider is not active")
        
        api_key = self.providers.get("openai", {}).get("api_key")
        
        if not api_key:
            raise ValueError("OpenAI API key is not set")
        
        # In a real implementation, we would:
        # 1. Import the OpenAI client
        # 2. Set up the client with the API key
        # 3. Make a request to the OpenAI API
        # 4. Parse and return the response
        
        # For demonstration purposes, we'll return a simulated response
        return {
            "text": f"This is a simulated response from OpenAI's {model}.",
            "model": model,
            "provider": "openai",
            "tokens_used": 50
        }
    
    def query_anthropic(self, 
                      prompt: str, 
                      model: str = "claude-3-haiku", 
                      system_prompt: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Query an Anthropic model
        
        Args:
            prompt: The user prompt
            model: The model name
            system_prompt: Optional system prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response from the model
        """
        if not self.providers.get("anthropic", {}).get("active", False):
            raise ValueError("Anthropic provider is not active")
        
        api_key = self.providers.get("anthropic", {}).get("api_key")
        
        if not api_key:
            raise ValueError("Anthropic API key is not set")
        
        # In a real implementation, we would:
        # 1. Import the Anthropic client
        # 2. Set up the client with the API key
        # 3. Make a request to the Anthropic API
        # 4. Parse and return the response
        
        # For demonstration purposes, we'll return a simulated response
        return {
            "text": f"This is a simulated response from Anthropic's {model}.",
            "model": model,
            "provider": "anthropic",
            "tokens_used": 50
        }
    
    def query_model(self, 
                  prompt: str, 
                  provider: str,
                  model: str,
                  system_prompt: Optional[str] = None,
                  temperature: float = 0.7,
                  max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Query a model from the specified provider
        
        Args:
            prompt: The user prompt
            provider: The provider name
            model: The model name
            system_prompt: Optional system prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response from the model
        """
        if provider == "ollama":
            return self.query_ollama(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif provider == "openai":
            return self.query_openai(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif provider == "anthropic":
            return self.query_anthropic(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate_response(self, question: str) -> str:
        """
        Generate a response to a question from Helpmate-AI
        
        Args:
            question: The question from Helpmate-AI
            
        Returns:
            A response string
        """
        try:
            # Find the first active provider
            active_provider = None
            active_model = None
            
            if self.providers.get("ollama", {}).get("active", False):
                active_provider = "ollama"
                active_model = "llama2"  # Default model for Ollama
            elif self.providers.get("openai", {}).get("active", False):
                active_provider = "openai"
                active_model = "gpt-3.5-turbo"  # Default model for OpenAI
            elif self.providers.get("anthropic", {}).get("active", False):
                active_provider = "anthropic"
                active_model = "claude-3-haiku"  # Default model for Anthropic
            
            if not active_provider:
                return "No active AI providers found. Please configure a provider in the CoderAI settings."
            
            # Generate response using the active provider
            system_prompt = "You are a helpful AI assistant integrated with CoderAI. Answer the user's question concisely and accurately."
            
            response = self.query_model(
                prompt=question,
                provider=active_provider,
                model=active_model,
                system_prompt=system_prompt
            )
            
            return response.get("text", "Sorry, I couldn't generate a response.")
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
