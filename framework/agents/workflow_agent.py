"""
CoderAI Framework Workflow Agents
This module provides workflow-related agents for the CoderAI framework.
"""

from typing import Dict, Any, List, Optional
from ..registry import registry
from ..types import Agent, Message, Function

@registry.register(type="agent")
class WorkflowAgent(Agent):
    """
    Agent for managing and executing workflows.
    """
    
    def __init__(self, name: str = "WorkflowAgent", description: str = None, model: str = None):
        """
        Initialize the workflow agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Manages and executes workflows composed of multiple steps and agents."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="create_workflow",
                description="Create a workflow from a description",
                parameters={
                    "type": "object",
                    "properties": {
                        "workflow_name": {
                            "type": "string",
                            "description": "Name of the workflow"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of what the workflow should do"
                        },
                        "input_parameters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Parameter name"
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "Parameter description"
                                    },
                                    "required": {
                                        "type": "boolean",
                                        "description": "Whether the parameter is required"
                                    }
                                }
                            },
                            "description": "Input parameters for the workflow"
                        }
                    },
                    "required": ["workflow_name", "description"]
                }
            ),
            Function(
                name="execute_workflow",
                description="Execute a workflow with specified parameters",
                parameters={
                    "type": "object",
                    "properties": {
                        "workflow_name": {
                            "type": "string",
                            "description": "Name of the workflow to execute"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "Parameters for the workflow execution"
                        },
                        "execution_options": {
                            "type": "object",
                            "properties": {
                                "async": {
                                    "type": "boolean",
                                    "description": "Whether to execute the workflow asynchronously"
                                },
                                "timeout": {
                                    "type": "integer",
                                    "description": "Timeout in seconds for the workflow execution"
                                }
                            },
                            "description": "Options for the workflow execution"
                        }
                    },
                    "required": ["workflow_name"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a sophisticated workflow agent. Your task is to create, manage, and execute workflows that coordinate multiple steps and agents to accomplish complex tasks.
        
        When creating workflows:
        1. Break down the overall task into logical steps or stages
        2. Identify appropriate agents or tools for each step
        3. Define clear inputs and outputs for each step
        4. Establish dependencies and flow between steps
        5. Include error handling and fallback mechanisms
        6. Design the workflow to be flexible and adaptable
        
        When executing workflows:
        1. Validate input parameters for completeness and correctness
        2. Monitor the execution of each step
        3. Handle errors or exceptions appropriately
        4. Provide status updates on workflow progress
        5. Ensure proper data flow between workflow steps
        6. Return comprehensive results upon completion
        
        Focus on creating workflows that are reliable, efficient, and effective at accomplishing their intended purpose.
        """

@registry.register(type="agent")
class PipelineAgent(Agent):
    """
    Agent for creating and managing data processing pipelines.
    """
    
    def __init__(self, name: str = "PipelineAgent", description: str = None, model: str = None):
        """
        Initialize the pipeline agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Creates and manages data processing pipelines for efficient data transformation and analysis."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="create_pipeline",
                description="Create a data processing pipeline",
                parameters={
                    "type": "object",
                    "properties": {
                        "pipeline_name": {
                            "type": "string",
                            "description": "Name of the pipeline"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of what the pipeline should do"
                        },
                        "input_data_format": {
                            "type": "string",
                            "description": "Format of the input data"
                        },
                        "output_data_format": {
                            "type": "string",
                            "description": "Format of the output data"
                        },
                        "processing_steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Step name"
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "Step description"
                                    },
                                    "type": {
                                        "type": "string",
                                        "description": "Type of processing step"
                                    }
                                }
                            },
                            "description": "Steps in the data processing pipeline"
                        }
                    },
                    "required": ["pipeline_name", "description", "input_data_format", "output_data_format"]
                }
            ),
            Function(
                name="execute_pipeline",
                description="Execute a data processing pipeline",
                parameters={
                    "type": "object",
                    "properties": {
                        "pipeline_name": {
                            "type": "string",
                            "description": "Name of the pipeline to execute"
                        },
                        "input_data": {
                            "type": "string",
                            "description": "Input data for the pipeline"
                        },
                        "execution_options": {
                            "type": "object",
                            "properties": {
                                "parallel": {
                                    "type": "boolean",
                                    "description": "Whether to execute steps in parallel when possible"
                                },
                                "cache_results": {
                                    "type": "boolean",
                                    "description": "Whether to cache intermediate results"
                                }
                            },
                            "description": "Options for the pipeline execution"
                        }
                    },
                    "required": ["pipeline_name", "input_data"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a specialized pipeline agent. Your task is to create and manage data processing pipelines that efficiently transform, analyze, and extract value from data.
        
        When creating pipelines:
        1. Design a logical sequence of processing steps based on the desired transformation
        2. Select appropriate processing methods for each step
        3. Ensure compatibility between input and output formats of adjacent steps
        4. Consider efficiency, scalability, and resource requirements
        5. Include validation and error handling mechanisms
        6. Document the purpose and functionality of each step
        
        When executing pipelines:
        1. Validate input data for format and quality
        2. Monitor the execution of each processing step
        3. Handle errors or exceptions appropriately
        4. Optimize resource usage based on execution options
        5. Provide progress updates and performance metrics
        6. Deliver processed data in the specified output format
        
        Focus on creating pipelines that are robust, efficient, and effective at transforming data to meet the user's needs.
        """
