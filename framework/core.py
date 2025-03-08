"""
CoderAI Core Framework
This module provides the core functionality for the CoderAI agent framework,
enabling natural language creation of tools, agents, and workflows.
"""

# Standard library imports
import copy
import json
from collections import defaultdict
from typing import List, Callable, Union
from datetime import datetime
# Local imports
import os
from .util import function_to_json, debug_print, merge_chunk, pretty_print_messages
from .types import (
    Agent,
    AgentFunction,
    Message,
    ChatCompletionMessageToolCall,
    Function,
    Response,
    Result,
)
from litellm import completion, acompletion
from pathlib import Path
from .logger import CoderAILogger, LoggerManager
from httpx import RemoteProtocolError, ConnectError
from litellm.exceptions import APIError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import AsyncOpenAI
import litellm
import inspect
from .constants import MC_MODE, FN_CALL, API_BASE_URL, NOT_SUPPORT_SENDER, ADD_USER, NON_FN_CALL
from .fn_call_converter import convert_tools_to_description, convert_non_fncall_messages_to_fncall_messages, SYSTEM_PROMPT_SUFFIX_TEMPLATE, convert_fn_messages_to_non_fn_messages, interleave_user_into_messages
from litellm.types.utils import Message as litellmMessage

def should_retry_error(exception):
    if MC_MODE is False: print(f"Caught exception: {type(exception).__name__} - {str(exception)}")
    
    # Match more error types
    if isinstance(exception, (APIError, RemoteProtocolError, ConnectError)):
        return True
    
    # Match through error message
    error_msg = str(exception).lower()
    return any([
        "connection error" in error_msg,
        "server disconnected" in error_msg,
        "eof occurred" in error_msg,
        "timeout" in error_msg, 
        "event loop is closed" in error_msg,
        "anthropicexception" in error_msg,
    ])

__CTX_VARS_NAME__ = "context_variables"
logger = LoggerManager.get_logger()

def adapt_tools_for_gemini(tools):
    """Adapt tool definitions for Gemini model, ensuring all OBJECT type parameters have non-empty properties"""
    if tools is None:
        return None
        
    adapted_tools = []
    for tool in tools:
        adapted_tool = copy.deepcopy(tool)
        
        # Check parameters
        if "parameters" in adapted_tool["function"]:
            params = adapted_tool["function"]["parameters"]
            
            # Handle top-level parameters
            if params.get("type") == "object":
                if "properties" not in params or not params["properties"]:
                    params["properties"] = {
                        "dummy": {
                            "type": "string",
                            "description": "Dummy property for Gemini compatibility"
                        }
                    }
            
            # Handle nested parameters
            if "properties" in params:
                for prop_name, prop in params["properties"].items():
                    if isinstance(prop, dict) and prop.get("type") == "object":
                        if "properties" not in prop or not prop["properties"]:
                            prop["properties"] = {
                                "dummy": {
                                    "type": "string",
                                    "description": "Dummy property for Gemini compatibility"
                                }
                            }
        
        adapted_tools.append(adapted_tool)
    return adapted_tools

class MetaChain:
    def __init__(self, log_path: Union[str, None, CoderAILogger] = None):
        """
        log_path: path of log file, None
        """
        if logger:
            self.logger = logger
        elif isinstance(log_path, CoderAILogger):
            self.logger = log_path
        else:
            self.logger = CoderAILogger(log_path=log_path)

    def get_chat_completion(
        self,
        agent: Agent,
        history: List,
        context_variables: dict,
        model_override: str,
        stream: bool,
        debug: bool,
    ) -> Message:
        context_variables = defaultdict(str, context_variables)
        instructions = (
            agent.instructions(context_variables)
            if callable(agent.instructions)
            else agent.instructions
        )
        if agent.examples:
            examples = agent.examples(context_variables) if callable(agent.examples) else agent.examples
            history = examples + history
        
        messages = [{"role": "system", "content": instructions}] + history
        
        tools = [function_to_json(f) for f in agent.functions]
        # hide context_variables from model
        for tool in tools:
            params = tool["function"]["parameters"]
            params["properties"].pop(__CTX_VARS_NAME__, None)
            if __CTX_VARS_NAME__ in params["required"]:
                params["required"].remove(__CTX_VARS_NAME__)
        create_model = model_override or agent.model

        if "gemini" in create_model.lower():
            tools = adapt_tools_for_gemini(tools)
        if FN_CALL:
            assert litellm.supports_function_calling(model = create_model) == True, f"Model {create_model} does not support function calling, please set `FN_CALL=False` to use non-function calling mode"
            create_params = {
                "model": create_model,
                "messages": messages,
                "tools": tools or None,
                "tool_choice": agent.tool_choice,
                "stream": stream,
            }
            NO_SENDER_MODE = False
            for not_sender_model in NOT_SUPPORT_SENDER:
                if not_sender_model in create_model:
                    NO_SENDER_MODE = True
                    break

            if NO_SENDER_MODE:
                messages = create_params["messages"]
                for message in messages:
                    if 'sender' in message:
                        del message['sender']
                create_params["messages"] = messages

            if tools and create_params['model'].startswith("gpt"):
                create_params["parallel_tool_calls"] = agent.parallel_tool_calls
            completion_response = completion(**create_params)
        else: 
            assert agent.tool_choice == "required", f"Non-function calling mode MUST use tool_choice = 'required' rather than {agent.tool_choice}"
            last_content = messages[-1]["content"]
            tools_description = convert_tools_to_description(tools)
            messages[-1]["content"] = last_content + "\n[IMPORTANT] You MUST use the tools provided to complete the task.\n" + SYSTEM_PROMPT_SUFFIX_TEMPLATE.format(description=tools_description)
            NO_SENDER_MODE = False
            for not_sender_model in NOT_SUPPORT_SENDER:
                if not_sender_model in create_model:
                    NO_SENDER_MODE = True
                    break

            if NO_SENDER_MODE:
                for message in messages:
                    if 'sender' in message:
                        del message['sender']
            if NON_FN_CALL:
                messages = convert_fn_messages_to_non_fn_messages(messages)
            if ADD_USER and messages[-1]["role"] != "user":
                messages = interleave_user_into_messages(messages)
            create_params = {
                "model": create_model,
                "messages": messages,
                "stream": stream,
                "base_url": API_BASE_URL,
            }
            completion_response = completion(**create_params)

        if stream:
            return completion_response
        else:
            message = completion_response.choices[0].message
            return message

    def run(
        self,
        agent: Agent,
        messages: List[Message],
        context_variables: dict = None,
        model_override: str = None,
        stream: bool = False,
        debug: bool = False,
    ) -> Result:
        """
        Run the agent with the given messages and context variables.
        
        Args:
            agent: The agent to run
            messages: List of messages to send to the agent
            context_variables: Dictionary of context variables
            model_override: Override the agent's model
            stream: Whether to stream the response
            debug: Whether to print debug information
            
        Returns:
            Result of the agent run
        """
        if context_variables is None:
            context_variables = {}
            
        message = self.get_chat_completion(
            agent=agent,
            history=messages,
            context_variables=context_variables,
            model_override=model_override,
            stream=stream,
            debug=debug,
        )
        
        if stream:
            return message
            
        response = Response(message=message)
        
        if hasattr(message, "tool_calls") and message.tool_calls:
            tool_calls = message.tool_calls
            for tool_call in tool_calls:
                function_call = tool_call.function
                function_name = function_call.name
                function_args = json.loads(function_call.arguments)
                
                # Find the corresponding function
                for function in agent.functions:
                    if function.name == function_name:
                        # Add context variables to function arguments
                        function_args[__CTX_VARS_NAME__] = context_variables
                        
                        # Call the function
                        function_result = function(**function_args)
                        
                        # Add the result to the response
                        response.add_tool_result(
                            tool_call_id=tool_call.id,
                            name=function_name,
                            args=function_args,
                            result=function_result,
                        )
                        break
                else:
                    # Function not found
                    response.add_tool_result(
                        tool_call_id=tool_call.id,
                        name=function_name,
                        args=function_args,
                        result={"error": f"Function {function_name} not found"},
                    )
                    
        return Result(response=response)
