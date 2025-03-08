"""
CoderAI Framework
This module provides the core functionality for the CoderAI framework,
enabling natural language creation of tools, agents, and workflows.
"""

from .core import MetaChain
from .types import Agent, AgentFunction, Message, Function, Response, Result
from .registry import Registry, registry
from .logger import CoderAILogger, LoggerManager
from .util import function_to_json, debug_print, pretty_print_messages
from .constants import (
    DEFAULT_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_MEMORY_SIZE,
    DEFAULT_MEMORY_K,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_TOOL_REGISTRY_PATH,
    DEFAULT_AGENT_REGISTRY_PATH,
    DEFAULT_WORKFLOW_REGISTRY_PATH,
)

__all__ = [
    "MetaChain",
    "Agent",
    "AgentFunction",
    "Message",
    "Function",
    "Response",
    "Result",
    "Registry",
    "registry",
    "CoderAILogger",
    "LoggerManager",
    "function_to_json",
    "debug_print",
    "pretty_print_messages",
    "DEFAULT_MODEL",
    "DEFAULT_EMBEDDING_MODEL",
    "DEFAULT_MEMORY_SIZE",
    "DEFAULT_MEMORY_K",
    "DEFAULT_CHUNK_SIZE",
    "DEFAULT_CHUNK_OVERLAP",
    "DEFAULT_TOOL_REGISTRY_PATH",
    "DEFAULT_AGENT_REGISTRY_PATH",
    "DEFAULT_WORKFLOW_REGISTRY_PATH",
]
