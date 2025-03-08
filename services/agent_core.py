"""
CoderAI Advanced Agent Framework
This module provides the core agent framework for CoderAI,
allowing natural language creation of tools, agents, and workflows.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Add CoderAI Agent Framework to the Python path
FRAMEWORK_PATH = Path(__file__).parent.parent / "framework"
sys.path.append(str(FRAMEWORK_PATH))

# Import CoderAI Agent Framework components
try:
    # Import core CoderAI Agent Framework components directly
    from framework.core import MetaChain
    from framework.types import Agent, AgentFunction, Message, Function, Response, Result
    from framework.util import function_to_json, debug_print
    from framework.logger import LoggerManager
    from framework.registry import Registry
    from framework.tools.base_tools import BaseTool
    from framework.memory.memory_manager import MemoryManager
    from framework.flow.workflow import Workflow, WorkflowStep
    from framework.agents.agent_factory import AgentFactory
except ImportError as e:
    logging.error(f"Failed to import CoderAI Agent Framework components: {e}")
    raise ImportError(
        "CoderAI Agent Framework components could not be imported. "
        "Please ensure the framework directory is present in the project root."
    )

class CoderAIAgentCore:
    """
    Core integration class for CoderAI Agent Framework.
    Provides direct access to advanced agent capabilities as an inbuilt power.
    """
    
    def __init__(self, model_service=None, embedding_service=None):
        """
        Initialize the CoderAI Agent Framework integration.
        
        Args:
            model_service: CoderAI's model service for LLM interactions
            embedding_service: CoderAI's embedding service for vector operations
        """
        self.logger = logging.getLogger(__name__)
        self.model_service = model_service
        self.embedding_service = embedding_service
        
        # Initialize CoderAI Agent Framework core components directly
        self.meta_chain = MetaChain()
        self.registry = Registry()
        self.memory_manager = MemoryManager()
        self.agent_factory = AgentFactory()
        
        # Register CoderAI-specific tools and capabilities
        self._register_coderAI_tools()
        self._register_coderAI_agents()
        
        self.logger.info("CoderAI Agent Framework initialized successfully as an inbuilt power")
    
    def _register_coderAI_tools(self):
        """Register CoderAI-specific tools with the registry"""
        # Register code analysis tools
        self.registry.register_tool(
            name="code_analysis",
            description="Analyze code structure and quality",
            function=self._code_analysis_tool
        )
        
        # Register documentation tools
        self.registry.register_tool(
            name="generate_documentation",
            description="Generate documentation for code",
            function=self._documentation_tool
        )
        
        # Register visualization tools
        self.registry.register_tool(
            name="visualize_code",
            description="Create visual representations of code structure",
            function=self._visualization_tool
        )
        
        # Register code generation tools
        self.registry.register_tool(
            name="generate_code",
            description="Generate code based on requirements",
            function=self._code_generation_tool
        )
        
        # Register code refactoring tools
        self.registry.register_tool(
            name="refactor_code",
            description="Refactor code to improve quality",
            function=self._code_refactoring_tool
        )
        
        # Register testing tools
        self.registry.register_tool(
            name="generate_tests",
            description="Generate test cases for code",
            function=self._test_generation_tool
        )
        
        # Register file operations tools
        self.registry.register_tool(
            name="file_operations",
            description="Perform file operations like read, write, and search",
            function=self._file_operations_tool
        )
        
        # Register web tools
        self.registry.register_tool(
            name="web_search",
            description="Search the web for information",
            function=self._web_search_tool
        )
        
        # Register terminal tools
        self.registry.register_tool(
            name="terminal_command",
            description="Execute terminal commands",
            function=self._terminal_command_tool
        )
        
        # Register RAG tools
        self.registry.register_tool(
            name="rag_search",
            description="Search through knowledge base using RAG",
            function=self._rag_search_tool
        )
        
        self.logger.info("CoderAI tools registered with the registry")
    
    def _register_coderAI_agents(self):
        """Register CoderAI-specific agent types"""
        # Register code assistant agent
        self.agent_factory.register_agent_type(
            "code_assistant",
            {
                "description": "Assists with code-related tasks",
                "default_tools": ["code_analysis", "generate_documentation", "generate_code"]
            }
        )
        
        # Register code evolution agent
        self.agent_factory.register_agent_type(
            "code_evolution",
            {
                "description": "Evolves and improves existing code",
                "default_tools": ["code_analysis", "refactor_code", "generate_tests"]
            }
        )
        
        # Register NLP interface agent
        self.agent_factory.register_agent_type(
            "nlp_interface",
            {
                "description": "Translates natural language to code",
                "default_tools": ["generate_code", "code_analysis"]
            }
        )
        
        # Register synthetic data agent
        self.agent_factory.register_agent_type(
            "synthetic_data",
            {
                "description": "Generates synthetic data for testing",
                "default_tools": ["generate_code", "generate_tests"]
            }
        )
        
        # Register research agent
        self.agent_factory.register_agent_type(
            "research_agent",
            {
                "description": "Conducts research on programming topics",
                "default_tools": ["web_search", "rag_search"]
            }
        )
        
        # Register file manager agent
        self.agent_factory.register_agent_type(
            "file_manager",
            {
                "description": "Manages file operations",
                "default_tools": ["file_operations"]
            }
        )
        
        # Register terminal agent
        self.agent_factory.register_agent_type(
            "terminal_agent",
            {
                "description": "Executes terminal commands",
                "default_tools": ["terminal_command"]
            }
        )
        
        self.logger.info("CoderAI agent types registered with the agent factory")
    
    # Tool implementations
    def _code_analysis_tool(self, code: str, language: str = None) -> Dict[str, Any]:
        """
        Analyze code structure and quality.
        
        Args:
            code: Code to analyze
            language: Programming language of the code
            
        Returns:
            Analysis results
        """
        # Use the model service to analyze code
        prompt = f"Analyze the following {language} code for structure, quality, and potential improvements:\n\n{code}"
        
        response = self.model_service.generate_text(prompt)
        
        return {
            "analysis": response,
            "language": language,
            "code_length": len(code)
        }
    
    def _documentation_tool(self, code: str, language: str = None, style: str = "standard") -> Dict[str, Any]:
        """
        Generate documentation for code.
        
        Args:
            code: Code to document
            language: Programming language of the code
            style: Documentation style (standard, detailed, minimal)
            
        Returns:
            Generated documentation
        """
        # Use the model service to generate documentation
        prompt = f"Generate {style} documentation for the following {language} code:\n\n{code}"
        
        response = self.model_service.generate_text(prompt)
        
        return {
            "documentation": response,
            "language": language,
            "style": style
        }
    
    def _visualization_tool(self, code: str, language: str = None, format: str = "mermaid") -> Dict[str, Any]:
        """
        Create visual representations of code structure.
        
        Args:
            code: Code to visualize
            language: Programming language of the code
            format: Visualization format (mermaid, plantuml, ascii)
            
        Returns:
            Visualization data
        """
        # Use the model service to generate visualization
        prompt = f"Create a {format} diagram representing the structure of the following {language} code:\n\n{code}"
        
        response = self.model_service.generate_text(prompt)
        
        return {
            "visualization": response,
            "format": format,
            "language": language
        }
    
    def _code_generation_tool(self, requirements: str, language: str = "python", comments: bool = True) -> Dict[str, Any]:
        """
        Generate code based on requirements.
        
        Args:
            requirements: Requirements for the code
            language: Programming language to generate
            comments: Whether to include comments
            
        Returns:
            Generated code
        """
        # Use the model service to generate code
        prompt = f"Generate {language} code that meets these requirements:\n\n{requirements}\n\n"
        prompt += "Include detailed comments and explanations." if comments else "Minimize comments."
        
        response = self.model_service.generate_text(prompt)
        
        return {
            "code": response,
            "language": language,
            "requirements": requirements
        }
    
    def _code_refactoring_tool(self, code: str, language: str = None, goals: List[str] = None) -> Dict[str, Any]:
        """
        Refactor code to improve quality.
        
        Args:
            code: Code to refactor
            language: Programming language of the code
            goals: Refactoring goals (performance, readability, maintainability)
            
        Returns:
            Refactored code
        """
        goals_str = ", ".join(goals) if goals else "general improvement"
        
        # Use the model service to refactor code
        prompt = f"Refactor the following {language} code for {goals_str}:\n\n{code}"
        
        response = self.model_service.generate_text(prompt)
        
        return {
            "refactored_code": response,
            "original_code": code,
            "language": language,
            "goals": goals
        }
    
    def _test_generation_tool(self, code: str, language: str = None, framework: str = None) -> Dict[str, Any]:
        """
        Generate test cases for code.
        
        Args:
            code: Code to test
            language: Programming language of the code
            framework: Testing framework to use
            
        Returns:
            Generated tests
        """
        framework_str = f" using the {framework} framework" if framework else ""
        
        # Use the model service to generate tests
        prompt = f"Generate tests{framework_str} for the following {language} code:\n\n{code}"
        
        response = self.model_service.generate_text(prompt)
        
        return {
            "tests": response,
            "language": language,
            "framework": framework
        }
    
    def _file_operations_tool(self, operation: str, path: str, content: str = None) -> Dict[str, Any]:
        """
        Perform file operations.
        
        Args:
            operation: Operation to perform (read, write, append, delete, search)
            path: File path
            content: Content for write/append operations
            
        Returns:
            Operation result
        """
        result = {
            "operation": operation,
            "path": path,
            "success": False
        }
        
        try:
            if operation == "read":
                with open(path, "r") as f:
                    result["content"] = f.read()
                    result["success"] = True
            elif operation == "write":
                with open(path, "w") as f:
                    f.write(content)
                    result["success"] = True
            elif operation == "append":
                with open(path, "a") as f:
                    f.write(content)
                    result["success"] = True
            elif operation == "delete":
                os.remove(path)
                result["success"] = True
            elif operation == "search":
                if os.path.isfile(path):
                    with open(path, "r") as f:
                        file_content = f.read()
                        result["matches"] = content in file_content
                        result["success"] = True
                else:
                    result["error"] = "File not found"
            else:
                result["error"] = f"Unsupported operation: {operation}"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _web_search_tool(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Search results
        """
        # This is a placeholder. In a real implementation, you would use a web search API
        return {
            "query": query,
            "results": [
                {"title": "Example Result 1", "url": "https://example.com/1", "snippet": "This is an example search result."},
                {"title": "Example Result 2", "url": "https://example.com/2", "snippet": "This is another example search result."}
            ],
            "num_results": 2
        }
    
    def _terminal_command_tool(self, command: str, cwd: str = None) -> Dict[str, Any]:
        """
        Execute terminal commands.
        
        Args:
            command: Command to execute
            cwd: Working directory
            
        Returns:
            Command execution result
        """
        import subprocess
        
        result = {
            "command": command,
            "success": False
        }
        
        try:
            process = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True
            )
            
            result["returncode"] = process.returncode
            result["stdout"] = process.stdout
            result["stderr"] = process.stderr
            result["success"] = process.returncode == 0
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _rag_search_tool(self, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Search through knowledge base using RAG.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Search results
        """
        # This is a placeholder. In a real implementation, you would use the embedding service
        # to search through a vector database
        return {
            "query": query,
            "results": [
                {"content": "Example content 1", "score": 0.95},
                {"content": "Example content 2", "score": 0.85},
                {"content": "Example content 3", "score": 0.75}
            ],
            "count": 3
        }
    
    # Public methods
    def create_agent(self, agent_type: str, config: Dict[str, Any] = None) -> Agent:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create
            config: Agent configuration
            
        Returns:
            Created agent
        """
        return self.agent_factory.create_agent(agent_type, config or {})
    
    def execute_agent_task(self, agent: Agent, task: str) -> Dict[str, Any]:
        """
        Execute a task using the specified agent.
        
        Args:
            agent: Agent to use
            task: Task description
            
        Returns:
            Task execution result
        """
        # Create messages
        messages = [
            {"role": "system", "content": agent.system_message},
            {"role": "user", "content": task}
        ]
        
        # Execute agent
        response = self.meta_chain.chat_completion(messages=messages, agent=agent)
        
        # Process response
        result = {
            "content": response.content,
            "task": task,
            "agent_type": agent.name
        }
        
        # Extract code if present
        import re
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response.content, re.DOTALL)
        if code_blocks:
            result["code"] = code_blocks[0]
        
        # Extract explanation if present
        explanation_match = re.search(r"(?:Explanation|Here's how it works):(.*?)(?:```|$)", response.content, re.DOTALL)
        if explanation_match:
            result["explanation"] = explanation_match.group(1).strip()
        
        return result
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get a list of available tools.
        
        Returns:
            List of available tools
        """
        tools = self.registry.list_items(type="tool")
        
        # Format tools for UI
        formatted_tools = []
        for name, tool_info in tools.items():
            formatted_tools.append({
                "name": name,
                "description": tool_info.get("description", ""),
                "category": tool_info.get("category", "other"),
                "parameters": tool_info.get("parameters", {})
            })
        
        return formatted_tools
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with the specified parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters
            
        Returns:
            Tool execution result
        """
        tool_info = self.registry.get_item(tool_name, type="tool")
        if not tool_info:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool_function = tool_info["function"]
        
        # Execute tool
        result = tool_function(**parameters)
        
        return result
    
    def save_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a workflow configuration.
        
        Args:
            workflow_config: Workflow configuration
            
        Returns:
            Save result
        """
        try:
            # Create workflow
            workflow = Workflow(
                name=workflow_config["name"],
                description=workflow_config.get("description", "")
            )
            
            # Add steps
            for step_config in workflow_config["steps"]:
                # Create step
                step = WorkflowStep(
                    name=step_config["description"],
                    description=step_config["description"],
                    config=step_config["config"]
                )
                
                # Add step to workflow
                workflow.add_step(step)
            
            # Register workflow
            self.registry.register_item(workflow, type="workflow")
            
            return {
                "success": True,
                "workflow_name": workflow_config["name"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
