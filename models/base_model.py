from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseModel(ABC):
    """Base class for all model integrations"""
    
    @abstractmethod
    def query(self, 
             prompt: str, 
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Query the model with a prompt
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response from the model
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get a list of available models
        
        Returns:
            List of model names
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Get the provider name
        
        Returns:
            Provider name
        """
        pass
