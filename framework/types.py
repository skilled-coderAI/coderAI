"""
CoderAI Framework Types
This module defines the data types used throughout the CoderAI framework.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional, Union, Literal

class Agent:
    """
    Agent class representing an AI agent with specific instructions and functions.
    """
    def __init__(
        self,
        instructions: Union[str, Callable[[Dict[str, Any]], str]],
        functions: List[Callable] = None,
        model: str = "gpt-4o",
        examples: Union[List[Dict[str, Any]], Callable[[Dict[str, Any]], List[Dict[str, Any]]]] = None,
        tool_choice: Union[str, Dict[str, Any]] = "auto",
        parallel_tool_calls: bool = True,
    ):
        """
        Initialize an agent.
        
        Args:
            instructions: Instructions for the agent, either a string or a function that takes context variables and returns a string
            functions: List of functions available to the agent
            model: Model to use for the agent
            examples: Examples to provide to the agent
            tool_choice: Tool choice strategy
            parallel_tool_calls: Whether to allow parallel tool calls
        """
        self.instructions = instructions
        self.functions = functions or []
        self.model = model
        self.examples = examples
        self.tool_choice = tool_choice
        self.parallel_tool_calls = parallel_tool_calls

@dataclass
class AgentFunction:
    """
    Function available to an agent.
    """
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable

@dataclass
class Message:
    """
    Message in a conversation.
    """
    role: str
    content: str
    tool_calls: List[Any] = field(default_factory=list)

@dataclass
class ChatCompletionMessageToolCall:
    """
    Tool call in a chat completion message.
    """
    id: str
    type: str
    function: Any

@dataclass
class Function:
    """
    Function definition.
    """
    name: str
    description: str
    parameters: Dict[str, Any]

@dataclass
class ToolResult:
    """
    Result of a tool call.
    """
    tool_call_id: str
    name: str
    args: Dict[str, Any]
    result: Any

@dataclass
class Response:
    """
    Response from an agent.
    """
    message: Message
    tool_results: List[ToolResult] = field(default_factory=list)
    
    def add_tool_result(self, tool_call_id: str, name: str, args: Dict[str, Any], result: Any):
        """
        Add a tool result to the response.
        
        Args:
            tool_call_id: ID of the tool call
            name: Name of the tool
            args: Arguments passed to the tool
            result: Result of the tool call
        """
        self.tool_results.append(ToolResult(
            tool_call_id=tool_call_id,
            name=name,
            args=args,
            result=result,
        ))

@dataclass
class Result:
    """
    Result of an agent run.
    """
    response: Response
