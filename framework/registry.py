"""
CoderAI Framework Registry
This module provides a registry for tools, agents, and workflows.
"""

import inspect
import importlib
import os
import glob
from typing import Dict, Any, Callable, List, Literal, Optional, Union
from functools import wraps
from .logger import LoggerManager

logger = LoggerManager.get_logger()

class Registry:
    """
    Registry for tools, agents, and workflows.
    """
    def __init__(self):
        """
        Initialize the registry.
        """
        self.tools = {}
        self.agents = {}
        self.workflows = {}
        self.plugin_tools = {}
        self.plugin_agents = {}
        
    def register(self, type: Literal["tool", "agent", "plugin_tool", "plugin_agent", "workflow"], name: str = None, func_name: str = None):
        """
        Register a tool, agent, or workflow.
        
        Args:
            type: Type of item to register
            name: Name of the item
            func_name: Name of the function
            
        Returns:
            Decorator function
        """
        def decorator(func):
            nonlocal name, func_name
            
            # Get name from function if not provided
            if name is None:
                name = func.__name__
                
            # Get function name from function if not provided
            if func_name is None:
                func_name = func.__name__
                
            # Register item
            if type == "tool":
                self.tools[name] = func
            elif type == "agent":
                self.agents[name] = func
            elif type == "plugin_tool":
                self.plugin_tools[name] = func
            elif type == "plugin_agent":
                self.plugin_agents[name] = func
            elif type == "workflow":
                self.workflows[name] = func
                
            # Log registration
            if logger:
                logger.debug(f"Registered {type} '{name}'")
                
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
                
            return wrapper
            
        return decorator
        
    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get a tool by name.
        
        Args:
            name: Name of the tool
            
        Returns:
            Tool function or None if not found
        """
        return self.tools.get(name) or self.plugin_tools.get(name)
        
    def get_agent(self, name: str) -> Optional[Callable]:
        """
        Get an agent by name.
        
        Args:
            name: Name of the agent
            
        Returns:
            Agent function or None if not found
        """
        return self.agents.get(name) or self.plugin_agents.get(name)
        
    def get_workflow(self, name: str) -> Optional[Callable]:
        """
        Get a workflow by name.
        
        Args:
            name: Name of the workflow
            
        Returns:
            Workflow function or None if not found
        """
        return self.workflows.get(name)
        
    def list_tools(self) -> List[str]:
        """
        List all registered tools.
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys()) + list(self.plugin_tools.keys())
        
    def list_agents(self) -> List[str]:
        """
        List all registered agents.
        
        Returns:
            List of agent names
        """
        return list(self.agents.keys()) + list(self.plugin_agents.keys())
        
    def list_workflows(self) -> List[str]:
        """
        List all registered workflows.
        
        Returns:
            List of workflow names
        """
        return list(self.workflows.keys())
        
    def load_tools_from_directory(self, directory: str):
        """
        Load tools from a directory.
        
        Args:
            directory: Directory to load tools from
        """
        # Get absolute path
        directory = os.path.abspath(directory)
        
        # Check if directory exists
        if not os.path.exists(directory):
            if logger:
                logger.warning(f"Directory '{directory}' does not exist")
            return
            
        # Get all Python files
        python_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
        
        # Import each file
        for file_path in python_files:
            # Skip __init__.py files
            if os.path.basename(file_path) == "__init__.py":
                continue
                
            try:
                # Get module name
                module_path = os.path.relpath(file_path, os.path.dirname(directory))
                module_name = os.path.splitext(module_path.replace(os.path.sep, "."))[0]
                
                # Import module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Log import
                if logger:
                    logger.debug(f"Imported tools from '{file_path}'")
            except Exception as e:
                if logger:
                    logger.error(f"Error importing tools from '{file_path}': {e}")
                    
    def load_agents_from_directory(self, directory: str):
        """
        Load agents from a directory.
        
        Args:
            directory: Directory to load agents from
        """
        # Get absolute path
        directory = os.path.abspath(directory)
        
        # Check if directory exists
        if not os.path.exists(directory):
            if logger:
                logger.warning(f"Directory '{directory}' does not exist")
            return
            
        # Get all Python files
        python_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
        
        # Import each file
        for file_path in python_files:
            # Skip __init__.py files
            if os.path.basename(file_path) == "__init__.py":
                continue
                
            try:
                # Get module name
                module_path = os.path.relpath(file_path, os.path.dirname(directory))
                module_name = os.path.splitext(module_path.replace(os.path.sep, "."))[0]
                
                # Import module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Log import
                if logger:
                    logger.debug(f"Imported agents from '{file_path}'")
            except Exception as e:
                if logger:
                    logger.error(f"Error importing agents from '{file_path}': {e}")
                    
    def load_workflows_from_directory(self, directory: str):
        """
        Load workflows from a directory.
        
        Args:
            directory: Directory to load workflows from
        """
        # Get absolute path
        directory = os.path.abspath(directory)
        
        # Check if directory exists
        if not os.path.exists(directory):
            if logger:
                logger.warning(f"Directory '{directory}' does not exist")
            return
            
        # Get all Python files
        python_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
        
        # Import each file
        for file_path in python_files:
            # Skip __init__.py files
            if os.path.basename(file_path) == "__init__.py":
                continue
                
            try:
                # Get module name
                module_path = os.path.relpath(file_path, os.path.dirname(directory))
                module_name = os.path.splitext(module_path.replace(os.path.sep, "."))[0]
                
                # Import module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Log import
                if logger:
                    logger.debug(f"Imported workflows from '{file_path}'")
            except Exception as e:
                if logger:
                    logger.error(f"Error importing workflows from '{file_path}': {e}")

# Create global registry
registry = Registry()
