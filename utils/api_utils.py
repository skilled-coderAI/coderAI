import requests
import json
import time
from typing import Dict, List, Any, Optional, Union

class APIUtils:
    """Utility for making API requests to various providers"""
    
    @staticmethod
    def make_request(
        url: str, 
        method: str = "GET", 
        headers: Optional[Dict[str, str]] = None, 
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1
    ) -> Dict[str, Any]:
        """
        Make an API request with retry logic
        
        Args:
            url: URL to make request to
            method: HTTP method (GET, POST, PUT, DELETE)
            headers: Request headers
            data: Form data
            json_data: JSON data
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds
            
        Returns:
            Response data
        """
        method = method.upper()
        headers = headers or {}
        
        for attempt in range(max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                    json=json_data,
                    timeout=timeout
                )
                
                # Check if request was successful
                response.raise_for_status()
                
                # Parse response
                if response.content:
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        return {"text": response.text}
                else:
                    return {"status": "success"}
                
            except requests.exceptions.RequestException as e:
                # Last attempt, raise exception
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                
                # Retry after delay
                time.sleep(retry_delay)
    
    @staticmethod
    def register_provider(
        provider_name: str,
        api_key: str,
        base_url: str,
        provider_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Register an external provider
        
        Args:
            provider_name: Name of the provider
            api_key: API key for the provider
            base_url: Base URL for the provider's API
            provider_config: Additional configuration for the provider
            
        Returns:
            Provider configuration
        """
        # In a real implementation, this would:
        # 1. Validate the API key
        # 2. Test the connection
        # 3. Save the provider configuration
        
        # For demonstration purposes, we'll return a simulated response
        return {
            "name": provider_name,
            "status": "registered",
            "api_key": api_key[:4] + "..." + api_key[-4:] if api_key else "",
            "base_url": base_url,
            "config": provider_config
        }
    
    @staticmethod
    def validate_api_key(provider: str, api_key: str) -> bool:
        """
        Validate an API key for a provider
        
        Args:
            provider: Provider name
            api_key: API key to validate
            
        Returns:
            True if valid, False otherwise
        """
        # In a real implementation, this would:
        # 1. Make a request to the provider's API
        # 2. Check if the response indicates a valid API key
        
        # For demonstration purposes, we'll return True if the API key is not empty
        return bool(api_key)
