"""
CoderAI Base Tools Module
This module provides the base classes and utilities for creating tools
that can be used by CoderAI agents.
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Union, TypeVar, Generic

class BaseTool:
    """
    Base class for all CoderAI tools.
    Tools are functions that agents can use to interact with the environment.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        required_args: Optional[List[str]] = None,
        optional_args: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new tool.
        
        Args:
            name: Name of the tool
            description: Description of what the tool does
            function: The function to call when the tool is used
            required_args: List of required argument names
            optional_args: Dictionary of optional argument names and their default values
        """
        self.name = name
        self.description = description
        self.function = function
        self.required_args = required_args or []
        self.optional_args = optional_args or {}
        
        # Validate that the function signature matches the provided args
        self._validate_function()
        
        self.logger = logging.getLogger(f"coderAI.tools.{name}")
    
    def _validate_function(self) -> None:
        """
        Validate that the function signature matches the provided args.
        """
        sig = inspect.signature(self.function)
        params = sig.parameters
        
        # Check that all required args are in the function signature
        for arg in self.required_args:
            if arg not in params:
                raise ValueError(f"Required argument '{arg}' not found in function signature")
        
        # Check that all optional args are in the function signature
        for arg in self.optional_args:
            if arg not in params:
                raise ValueError(f"Optional argument '{arg}' not found in function signature")
    
    def __call__(self, **kwargs) -> Any:
        """
        Call the tool function with the provided arguments.
        
        Args:
            **kwargs: Arguments to pass to the function
            
        Returns:
            The result of the function call
        """
        # Check that all required args are provided
        for arg in self.required_args:
            if arg not in kwargs:
                raise ValueError(f"Required argument '{arg}' not provided")
        
        # Add default values for optional args if not provided
        for arg, default in self.optional_args.items():
            if arg not in kwargs:
                kwargs[arg] = default
        
        self.logger.debug(f"Calling tool '{self.name}' with args: {kwargs}")
        
        # Call the function with the provided arguments
        result = self.function(**kwargs)
        
        self.logger.debug(f"Tool '{self.name}' returned: {result}")
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary representation.
        
        Returns:
            Dictionary representation of the tool
        """
        return {
            "name": self.name,
            "description": self.description,
            "required_args": self.required_args,
            "optional_args": self.optional_args
        }

class ToolRegistry:
    """
    Registry for tools that can be used by CoderAI agents.
    """
    
    def __init__(self):
        """Initialize an empty tool registry."""
        self.tools: Dict[str, BaseTool] = {}
        self.logger = logging.getLogger("coderAI.tools.registry")
    
    def register(self, tool: BaseTool) -> None:
        """
        Register a tool with the registry.
        
        Args:
            tool: The tool to register
        """
        if tool.name in self.tools:
            self.logger.warning(f"Tool '{tool.name}' already registered. Overwriting.")
        
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool '{tool.name}'")
    
    def get(self, name: str) -> Optional[BaseTool]:
        """
        Get a tool by name.
        
        Args:
            name: Name of the tool to get
            
        Returns:
            The tool if found, None otherwise
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """
        List all registered tool names.
        
        Returns:
            List of registered tool names
        """
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """
        Get descriptions for all registered tools.
        
        Returns:
            Dictionary mapping tool names to their descriptions
        """
        return {name: tool.description for name, tool in self.tools.items()}
    
    def clear(self) -> None:
        """Clear all registered tools."""
        self.tools.clear()
        self.logger.info("Cleared all registered tools")

# Global tool registry instance
registry = ToolRegistry()

def register_tool(
    name: str,
    description: str,
    function: Callable,
    required_args: Optional[List[str]] = None,
    optional_args: Optional[Dict[str, Any]] = None
) -> BaseTool:
    """
    Register a new tool with the global registry.
    
    Args:
        name: Name of the tool
        description: Description of what the tool does
        function: The function to call when the tool is used
        required_args: List of required argument names
        optional_args: Dictionary of optional argument names and their default values
        
    Returns:
        The registered tool
    """
    tool = BaseTool(
        name=name,
        description=description,
        function=function,
        required_args=required_args,
        optional_args=optional_args
    )
    
    registry.register(tool)
    
    return tool