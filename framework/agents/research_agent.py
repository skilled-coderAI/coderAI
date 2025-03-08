"""
CoderAI Framework Research Agents
This module provides research-related agents for the CoderAI framework.
"""

from typing import Dict, Any, List, Optional
from ..registry import registry
from ..types import Agent, Message, Function

@registry.register(type="agent")
class ResearchAgent(Agent):
    """
    Agent for conducting research on various topics.
    """
    
    def __init__(self, name: str = "ResearchAgent", description: str = None, model: str = None):
        """
        Initialize the research agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Conducts research on various topics and provides comprehensive information."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="research_topic",
                description="Research a topic and provide information",
                parameters={
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic to research"
                        },
                        "depth": {
                            "type": "string",
                            "enum": ["basic", "intermediate", "advanced"],
                            "description": "Depth of research"
                        },
                        "focus_areas": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Specific areas to focus on during research"
                        }
                    },
                    "required": ["topic"]
                }
            ),
            Function(
                name="compare_topics",
                description="Compare multiple topics",
                parameters={
                    "type": "object",
                    "properties": {
                        "topics": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Topics to compare"
                        },
                        "comparison_criteria": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Criteria to use for comparison"
                        }
                    },
                    "required": ["topics"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a thorough research agent. Your task is to conduct comprehensive research on various topics and provide accurate, well-organized information.
        
        When researching topics:
        1. Gather information from reliable sources
        2. Organize information in a clear, logical structure
        3. Provide context and background information
        4. Include relevant examples, statistics, or case studies
        5. Address different perspectives or viewpoints
        6. Cite sources when providing specific facts or claims
        7. Adjust the depth and complexity based on the requested depth level
        
        When comparing topics, identify key similarities and differences based on the specified criteria, and present the information in a structured, easy-to-understand format.
        """

@registry.register(type="agent")
class DocumentationAgent(Agent):
    """
    Agent for creating and managing documentation.
    """
    
    def __init__(self, name: str = "DocumentationAgent", description: str = None, model: str = None):
        """
        Initialize the documentation agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Creates and manages documentation for projects, code, and processes."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="create_documentation",
                description="Create documentation for a project or component",
                parameters={
                    "type": "object",
                    "properties": {
                        "project_name": {
                            "type": "string",
                            "description": "Name of the project or component"
                        },
                        "documentation_type": {
                            "type": "string",
                            "enum": ["user_guide", "api_reference", "technical_specification", "readme"],
                            "description": "Type of documentation to create"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content or information to include in the documentation"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "html", "text", "docstring"],
                            "description": "Format for the documentation"
                        }
                    },
                    "required": ["project_name", "documentation_type", "content"]
                }
            ),
            Function(
                name="update_documentation",
                description="Update existing documentation",
                parameters={
                    "type": "object",
                    "properties": {
                        "existing_documentation": {
                            "type": "string",
                            "description": "Existing documentation content"
                        },
                        "updates": {
                            "type": "string",
                            "description": "Updates to apply to the documentation"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "html", "text", "docstring"],
                            "description": "Format of the documentation"
                        }
                    },
                    "required": ["existing_documentation", "updates"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a skilled documentation agent. Your task is to create and manage clear, comprehensive documentation for projects, code, and processes.
        
        When creating documentation:
        1. Use a clear, concise writing style
        2. Organize information logically with appropriate headings and sections
        3. Include examples, diagrams, or screenshots when helpful
        4. Tailor the content to the intended audience
        5. Follow best practices for the specified documentation type and format
        6. Ensure completeness and accuracy of information
        
        When updating documentation, integrate new information seamlessly with existing content while maintaining consistency in style and structure.
        """

@registry.register(type="agent")
class AnalysisAgent(Agent):
    """
    Agent for analyzing data and information.
    """
    
    def __init__(self, name: str = "AnalysisAgent", description: str = None, model: str = None):
        """
        Initialize the analysis agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Analyzes data and information to extract insights and patterns."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="analyze_data",
                description="Analyze data to extract insights",
                parameters={
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "Data to analyze (can be text, numbers, or structured data in JSON format)"
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["statistical", "trend", "pattern", "sentiment", "comparative"],
                            "description": "Type of analysis to perform"
                        },
                        "specific_questions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Specific questions to answer through the analysis"
                        }
                    },
                    "required": ["data"]
                }
            ),
            Function(
                name="summarize_information",
                description="Summarize complex information",
                parameters={
                    "type": "object",
                    "properties": {
                        "information": {
                            "type": "string",
                            "description": "Information to summarize"
                        },
                        "length": {
                            "type": "string",
                            "enum": ["brief", "moderate", "comprehensive"],
                            "description": "Desired length of the summary"
                        },
                        "focus": {
                            "type": "string",
                            "description": "Specific aspect to focus on in the summary"
                        }
                    },
                    "required": ["information"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are an insightful analysis agent. Your task is to analyze data and information to extract meaningful insights, patterns, and conclusions.
        
        When analyzing data:
        1. Identify key patterns, trends, or anomalies
        2. Apply appropriate analytical techniques based on the data type and analysis goals
        3. Draw evidence-based conclusions
        4. Highlight limitations or uncertainties in the analysis
        5. Present findings in a clear, structured format
        6. Use visualizations or examples to illustrate key points when helpful
        
        When summarizing information, capture the essential points and main ideas while maintaining accuracy and context, adjusting the level of detail based on the requested length.
        """
