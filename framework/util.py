"""
CoderAI Framework Utilities
This module provides utility functions for the CoderAI framework.
"""

import inspect
import json
import re
from typing import Callable, Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def function_to_json(func: Callable) -> Dict[str, Any]:
    """
    Convert a function to a JSON schema for LLM function calling.
    
    Args:
        func: Function to convert
        
    Returns:
        JSON schema for the function
    """
    # Get function signature
    sig = inspect.signature(func)
    
    # Get function docstring
    doc = inspect.getdoc(func) or ""
    
    # Create parameters schema
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    
    for name, param in sig.parameters.items():
        # Skip context_variables parameter
        if name == "context_variables":
            continue
            
        # Check if parameter has a default value
        has_default = param.default != inspect.Parameter.empty
        
        # Get parameter type hint
        param_type = "string"  # Default type
        if param.annotation != inspect.Parameter.empty:
            if param.annotation == int:
                param_type = "integer"
            elif param.annotation == float:
                param_type = "number"
            elif param.annotation == bool:
                param_type = "boolean"
            elif param.annotation == list or param.annotation == List:
                param_type = "array"
            elif param.annotation == dict or param.annotation == Dict:
                param_type = "object"
                
        # Extract parameter description from docstring
        param_doc = ""
        param_pattern = rf":param {name}:\s*(.*?)(?:$|:param)"
        param_match = re.search(param_pattern, doc, re.DOTALL)
        if param_match:
            param_doc = param_match.group(1).strip()
            
        # Add parameter to schema
        parameters["properties"][name] = {
            "type": param_type,
            "description": param_doc,
        }
        
        # Add to required list if no default value
        if not has_default:
            parameters["required"].append(name)
    
    # Create function schema
    function_schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc.split("\n\n")[0] if doc else "",
            "parameters": parameters,
        }
    }
    
    return function_schema

def debug_print(debug: bool, *args, **kwargs):
    """
    Print debug information if debug is enabled.
    
    Args:
        debug: Whether to print debug information
        *args: Arguments to print
        **kwargs: Keyword arguments to print
    """
    if debug:
        console.print(*args, **kwargs)

def pretty_print_messages(messages: List[Dict[str, Any]], title: Optional[str] = None):
    """
    Pretty print messages.
    
    Args:
        messages: List of messages to print
        title: Optional title for the panel
    """
    for message in messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")
        
        if role == "system":
            console.print(Panel(
                Markdown(content),
                title=f"System Message",
                border_style="blue",
            ))
        elif role == "user":
            console.print(Panel(
                Markdown(content),
                title=f"User Message",
                border_style="green",
            ))
        elif role == "assistant":
            console.print(Panel(
                Markdown(content),
                title=f"Assistant Message",
                border_style="yellow",
            ))
            
            # Print tool calls if any
            if "tool_calls" in message and message["tool_calls"]:
                for tool_call in message["tool_calls"]:
                    function = tool_call.get("function", {})
                    name = function.get("name", "unknown")
                    args = function.get("arguments", "{}")
                    
                    try:
                        args_dict = json.loads(args)
                        args_str = json.dumps(args_dict, indent=2)
                    except:
                        args_str = args
                        
                    console.print(Panel(
                        f"Function: {name}\nArguments:\n{args_str}",
                        title=f"Tool Call",
                        border_style="magenta",
                    ))
        else:
            console.print(Panel(
                Markdown(content),
                title=f"{role.capitalize()} Message",
                border_style="white",
            ))

def merge_chunk(chunk_list):
    """
    Merge chunks of text.
    
    Args:
        chunk_list: List of chunks to merge
        
    Returns:
        Merged text
    """
    if not chunk_list:
        return ""
        
    result = []
    for chunk in chunk_list:
        if chunk:
            result.append(chunk)
            
    return "".join(result)
