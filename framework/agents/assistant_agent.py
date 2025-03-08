"""
CoderAI Framework Assistant Agents
This module provides assistant-related agents for the CoderAI framework.
"""

from typing import Dict, Any, List, Optional
from ..registry import registry
from ..types import Agent, Message, Function

@registry.register(type="agent")
class AssistantAgent(Agent):
    """
    General-purpose assistant agent for various tasks.
    """
    
    def __init__(self, name: str = "AssistantAgent", description: str = None, model: str = None):
        """
        Initialize the assistant agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "General-purpose assistant for answering questions and providing assistance."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="answer_question",
                description="Answer a question with detailed information",
                parameters={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Question to answer"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context or information related to the question"
                        },
                        "detail_level": {
                            "type": "string",
                            "enum": ["brief", "moderate", "detailed"],
                            "description": "Level of detail for the answer"
                        }
                    },
                    "required": ["question"]
                }
            ),
            Function(
                name="provide_assistance",
                description="Provide assistance with a task or problem",
                parameters={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Task or problem to assist with"
                        },
                        "user_level": {
                            "type": "string",
                            "enum": ["beginner", "intermediate", "advanced"],
                            "description": "User's knowledge or experience level"
                        },
                        "preferred_approach": {
                            "type": "string",
                            "description": "User's preferred approach or method"
                        }
                    },
                    "required": ["task"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a helpful assistant agent. Your task is to provide accurate, useful information and assistance to users.
        
        When answering questions:
        1. Provide clear, concise, and accurate information
        2. Use examples or analogies to clarify complex concepts
        3. Cite sources or references when appropriate
        4. Adjust the level of detail based on the requested detail level
        5. Acknowledge limitations or uncertainties in your knowledge
        
        When providing assistance:
        1. Break down complex tasks into manageable steps
        2. Tailor your guidance to the user's knowledge level
        3. Offer multiple approaches or solutions when applicable
        4. Anticipate potential challenges or issues
        5. Provide resources for further learning or assistance
        
        Always maintain a helpful, supportive tone and focus on addressing the user's needs effectively.
        """

@registry.register(type="agent")
class QuestionAnsweringAgent(Agent):
    """
    Agent specialized in answering questions.
    """
    
    def __init__(self, name: str = "QuestionAnsweringAgent", description: str = None, model: str = None):
        """
        Initialize the question answering agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Specialized in answering questions with accurate and comprehensive information."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="answer_factual_question",
                description="Answer a factual question with accurate information",
                parameters={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Factual question to answer"
                        },
                        "domain": {
                            "type": "string",
                            "description": "Knowledge domain of the question (e.g., science, history, technology)"
                        },
                        "include_sources": {
                            "type": "boolean",
                            "description": "Whether to include sources or references"
                        }
                    },
                    "required": ["question"]
                }
            ),
            Function(
                name="answer_conceptual_question",
                description="Answer a conceptual or theoretical question",
                parameters={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Conceptual question to answer"
                        },
                        "complexity": {
                            "type": "string",
                            "enum": ["basic", "intermediate", "advanced"],
                            "description": "Complexity level of the answer"
                        },
                        "include_examples": {
                            "type": "boolean",
                            "description": "Whether to include examples or illustrations"
                        }
                    },
                    "required": ["question"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a knowledgeable question answering agent. Your task is to provide accurate, informative answers to various types of questions.
        
        When answering factual questions:
        1. Provide accurate, verifiable information
        2. Present facts clearly and concisely
        3. Include relevant context or background
        4. Cite sources or references when requested
        5. Acknowledge when information is uncertain or contested
        
        When answering conceptual questions:
        1. Explain concepts clearly and thoroughly
        2. Use analogies, examples, or illustrations to enhance understanding
        3. Present different perspectives or interpretations when relevant
        4. Adjust the complexity of your explanation based on the requested level
        5. Connect the concept to related ideas or applications
        
        Always strive for accuracy, clarity, and helpfulness in your answers.
        """

@registry.register(type="agent")
class TaskManagementAgent(Agent):
    """
    Agent for managing tasks and workflows.
    """
    
    def __init__(self, name: str = "TaskManagementAgent", description: str = None, model: str = None):
        """
        Initialize the task management agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Helps manage tasks, projects, and workflows efficiently."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="create_task_plan",
                description="Create a plan for completing a task or project",
                parameters={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Task or project to plan"
                        },
                        "deadline": {
                            "type": "string",
                            "description": "Deadline or timeframe for the task"
                        },
                        "resources": {
                            "type": "string",
                            "description": "Available resources or constraints"
                        },
                        "detail_level": {
                            "type": "string",
                            "enum": ["high-level", "detailed", "comprehensive"],
                            "description": "Level of detail for the plan"
                        }
                    },
                    "required": ["task"]
                }
            ),
            Function(
                name="optimize_workflow",
                description="Optimize a workflow or process for efficiency",
                parameters={
                    "type": "object",
                    "properties": {
                        "current_workflow": {
                            "type": "string",
                            "description": "Current workflow or process"
                        },
                        "optimization_goals": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Goals for optimization (e.g., time saving, resource efficiency, quality improvement)"
                        },
                        "constraints": {
                            "type": "string",
                            "description": "Constraints or limitations to consider"
                        }
                    },
                    "required": ["current_workflow"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are an efficient task management agent. Your task is to help users plan, organize, and optimize their tasks, projects, and workflows.
        
        When creating task plans:
        1. Break down complex tasks into manageable steps or subtasks
        2. Establish clear priorities and dependencies
        3. Allocate appropriate time and resources to each step
        4. Identify potential risks or challenges
        5. Suggest milestones or checkpoints for tracking progress
        6. Adjust the level of detail based on the requested detail level
        
        When optimizing workflows:
        1. Identify inefficiencies or bottlenecks in the current process
        2. Suggest specific improvements or alternatives
        3. Consider trade-offs between different optimization goals
        4. Provide implementation guidance for recommended changes
        5. Suggest metrics or methods for evaluating the optimized workflow
        
        Focus on practical, actionable recommendations that help users achieve their goals efficiently and effectively.
        """
