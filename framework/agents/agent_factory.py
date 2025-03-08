"""
CoderAI Agent Factory Module
This module provides a factory for creating different types of agents
based on the specified configuration.
"""

import logging
from typing import Dict, List, Any, Optional, Union, Type

from framework.tools.base_tools import BaseTool
from framework.memory.memory_manager import MemoryManager
from framework.flow.workflow import Workflow

# Import agent implementations
from .assistant_agent import AssistantAgent
from .code_agent import CodeGenerationAgent, CodeReviewAgent, CodeRefactoringAgent, CodeExplanationAgent
from .research_agent import ResearchAgent
from .workflow_agent import WorkflowAgent

class AgentFactory:
    """
    Factory for creating CoderAI agents.
    
    This factory provides methods for creating different types of agents
    with the specified configuration.
    """
    
    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        """
        Initialize the agent factory.
        
        Args:
            memory_manager: Memory manager to use for agents
        """
        self.logger = logging.getLogger(__name__)
        self.memory_manager = memory_manager or MemoryManager()
        
        # Register available agent types
        self.agent_types = {
            "assistant": AssistantAgent,
            "code_generation": CodeGenerationAgent,
            "code_review": CodeReviewAgent,
            "code_refactoring": CodeRefactoringAgent,
            "code_explanation": CodeExplanationAgent,
            "research": ResearchAgent,
            "workflow": WorkflowAgent
        }
        
        self.logger.info(f"Agent factory initialized with {len(self.agent_types)} agent types")
    
    def create_agent(
        self,
        agent_type: str,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create
            agent_id: ID for the agent (optional, will be generated if not provided)
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created agent
            
        Raises:
            ValueError: If the specified agent type is not supported
        """
        if agent_type not in self.agent_types:
            supported_types = ", ".join(self.agent_types.keys())
            raise ValueError(f"Unsupported agent type: {agent_type}. Supported types: {supported_types}")
        
        agent_class = self.agent_types[agent_type]
        
        self.logger.info(f"Creating agent of type {agent_type}")
        
        # Create the agent with the specified configuration
        agent = agent_class(
            agent_id=agent_id,
            name=name or f"{agent_type.capitalize()} Agent",
            description=description or f"A CoderAI {agent_type} agent",
            memory_manager=self.memory_manager,
            tools=tools or [],
            config=config or {}
        )
        
        return agent
    
    def create_assistant_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> AssistantAgent:
        """
        Create an assistant agent.
        
        Args:
            agent_id: ID for the agent
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created assistant agent
        """
        return self.create_agent(
            agent_type="assistant",
            agent_id=agent_id,
            name=name,
            description=description,
            tools=tools,
            config=config
        )
    
    def create_code_generation_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> CodeGenerationAgent:
        """
        Create a code generation agent.
        
        Args:
            agent_id: ID for the agent
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created code generation agent
        """
        return self.create_agent(
            agent_type="code_generation",
            agent_id=agent_id,
            name=name,
            description=description,
            tools=tools,
            config=config
        )
    
    def create_code_review_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> CodeReviewAgent:
        """
        Create a code review agent.
        
        Args:
            agent_id: ID for the agent
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created code review agent
        """
        return self.create_agent(
            agent_type="code_review",
            agent_id=agent_id,
            name=name,
            description=description,
            tools=tools,
            config=config
        )
    
    def create_code_refactoring_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> CodeRefactoringAgent:
        """
        Create a code refactoring agent.
        
        Args:
            agent_id: ID for the agent
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created code refactoring agent
        """
        return self.create_agent(
            agent_type="code_refactoring",
            agent_id=agent_id,
            name=name,
            description=description,
            tools=tools,
            config=config
        )
    
    def create_code_explanation_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> CodeExplanationAgent:
        """
        Create a code explanation agent.
        
        Args:
            agent_id: ID for the agent
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created code explanation agent
        """
        return self.create_agent(
            agent_type="code_explanation",
            agent_id=agent_id,
            name=name,
            description=description,
            tools=tools,
            config=config
        )
    
    def create_research_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> ResearchAgent:
        """
        Create a research agent.
        
        Args:
            agent_id: ID for the agent
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created research agent
        """
        return self.create_agent(
            agent_type="research",
            agent_id=agent_id,
            name=name,
            description=description,
            tools=tools,
            config=config
        )
    
    def create_workflow_agent(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        workflows: Optional[List[Workflow]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> WorkflowAgent:
        """
        Create a workflow agent.
        
        Args:
            agent_id: ID for the agent
            name: Name for the agent
            description: Description of the agent
            tools: Tools to provide to the agent
            workflows: Workflows to provide to the agent
            config: Additional configuration for the agent
            
        Returns:
            Created workflow agent
        """
        # Add workflows to the configuration
        full_config = config or {}
        if workflows:
            full_config["workflows"] = workflows
        
        return self.create_agent(
            agent_type="workflow",
            agent_id=agent_id,
            name=name,
            description=description,
            tools=tools,
            config=full_config
        )
    
    def register_agent_type(self, agent_type: str, agent_class: Type) -> None:
        """
        Register a new agent type.
        
        Args:
            agent_type: Type name for the agent
            agent_class: Class for the agent
        """
        self.agent_types[agent_type] = agent_class
        self.logger.info(f"Registered new agent type: {agent_type}")
    
    def get_available_agent_types(self) -> List[str]:
        """
        Get a list of available agent types.
        
        Returns:
            List of available agent types
        """
        return list(self.agent_types.keys())