"""
CoderAI Framework Function Call Converter
This module provides utilities for converting between function calling and non-function calling formats.
"""

import json
import re
from typing import List, Dict, Any, Optional

# Template for system prompt suffix in non-function calling mode
SYSTEM_PROMPT_SUFFIX_TEMPLATE = """
Available tools:
{description}

To use a tool, respond with the following format:
```tool
{{"name": "tool_name", "arguments": {{"arg1": "value1", "arg2": "value2", ...}}}}
```

You MUST use one of the provided tools to respond to the user. Do not respond in any other format.
"""

def convert_tools_to_description(tools: List[Dict[str, Any]]) -> str:
    """
    Convert tools to a description format for non-function calling models.
    
    Args:
        tools: List of tools to convert
        
    Returns:
        Description of tools
    """
    if not tools:
        return ""
        
    description = ""
    for tool in tools:
        function = tool["function"]
        name = function["name"]
        tool_description = function["description"]
        parameters = function["parameters"]
        
        description += f"- {name}: {tool_description}\n"
        description += "  Parameters:\n"
        
        required_params = parameters.get("required", [])
        properties = parameters.get("properties", {})
        
        for param_name, param_info in properties.items():
            param_type = param_info.get("type", "string")
            param_description = param_info.get("description", "")
            required = "required" if param_name in required_params else "optional"
            
            description += f"  - {param_name} ({param_type}, {required}): {param_description}\n"
            
        description += "\n"
        
    return description

def extract_tool_calls_from_content(content: str) -> List[Dict[str, Any]]:
    """
    Extract tool calls from content.
    
    Args:
        content: Content to extract tool calls from
        
    Returns:
        List of tool calls
    """
    tool_calls = []
    
    # Find all tool call blocks
    tool_blocks = re.findall(r"```tool\s*(.*?)```", content, re.DOTALL)
    
    for block in tool_blocks:
        try:
            # Parse JSON
            tool_call = json.loads(block.strip())
            
            # Validate tool call format
            if "name" in tool_call and "arguments" in tool_call:
                tool_calls.append({
                    "type": "function",
                    "function": {
                        "name": tool_call["name"],
                        "arguments": json.dumps(tool_call["arguments"]),
                    }
                })
        except:
            # Skip invalid tool calls
            pass
            
    return tool_calls

def convert_non_fncall_messages_to_fncall_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert non-function calling messages to function calling messages.
    
    Args:
        messages: List of messages to convert
        
    Returns:
        Converted messages
    """
    converted_messages = []
    
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        
        if role == "assistant":
            # Extract tool calls from content
            tool_calls = extract_tool_calls_from_content(content)
            
            if tool_calls:
                # Create new message with tool calls
                converted_message = {
                    "role": role,
                    "content": None,
                    "tool_calls": tool_calls,
                }
            else:
                # Keep original message
                converted_message = message
        else:
            # Keep original message
            converted_message = message
            
        converted_messages.append(converted_message)
        
    return converted_messages

def convert_fn_messages_to_non_fn_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert function calling messages to non-function calling messages.
    
    Args:
        messages: List of messages to convert
        
    Returns:
        Converted messages
    """
    converted_messages = []
    
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        tool_calls = message.get("tool_calls", [])
        
        if role == "assistant" and tool_calls:
            # Convert tool calls to content
            tool_call_content = ""
            
            for tool_call in tool_calls:
                if tool_call.get("type") == "function":
                    function = tool_call.get("function", {})
                    name = function.get("name", "")
                    arguments = function.get("arguments", "{}")
                    
                    try:
                        args_dict = json.loads(arguments)
                        args_str = json.dumps(args_dict, indent=2)
                    except:
                        args_str = arguments
                        
                    tool_call_content += f"```tool\n{{\n  \"name\": \"{name}\",\n  \"arguments\": {args_str}\n}}\n```\n\n"
            
            # Create new message with content
            converted_message = {
                "role": role,
                "content": (content or "") + "\n\n" + tool_call_content.strip(),
            }
        else:
            # Keep original message
            converted_message = message
            
        converted_messages.append(converted_message)
        
    return converted_messages

def interleave_user_into_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Interleave user messages between assistant messages.
    
    Args:
        messages: List of messages to interleave
        
    Returns:
        Interleaved messages
    """
    interleaved_messages = []
    
    for i, message in enumerate(messages):
        interleaved_messages.append(message)
        
        if i < len(messages) - 1:
            next_message = messages[i + 1]
            
            if message.get("role") == "assistant" and next_message.get("role") == "assistant":
                # Insert user message
                interleaved_messages.append({
                    "role": "user",
                    "content": "Please continue.",
                })
                
    return interleaved_messages
