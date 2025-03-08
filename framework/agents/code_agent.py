"""
CoderAI Framework Code Agents
This module provides code-related agents for the CoderAI framework.
"""

from typing import Dict, Any, List, Optional
from ..registry import registry
from ..types import Agent, Message, Function

@registry.register(type="agent")
class CodeGenerationAgent(Agent):
    """
    Agent for generating code based on requirements.
    """
    
    def __init__(self, name: str = "CodeGenerationAgent", description: str = None, model: str = None):
        """
        Initialize the code generation agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Generates code based on requirements and specifications."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="generate_code",
                description="Generate code based on requirements",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language to generate code in"
                        },
                        "requirements": {
                            "type": "string",
                            "description": "Requirements for the code to generate"
                        },
                        "include_comments": {
                            "type": "boolean",
                            "description": "Whether to include comments in the generated code"
                        }
                    },
                    "required": ["language", "requirements"]
                }
            ),
            Function(
                name="complete_code",
                description="Complete partial code",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language of the code"
                        },
                        "partial_code": {
                            "type": "string",
                            "description": "Partial code to complete"
                        },
                        "requirements": {
                            "type": "string",
                            "description": "Requirements for the code completion"
                        }
                    },
                    "required": ["language", "partial_code"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a skilled code generation agent. Your task is to generate high-quality, efficient, and well-documented code based on requirements.
        
        Follow these guidelines:
        1. Write clean, readable, and maintainable code
        2. Follow best practices for the specified programming language
        3. Include appropriate error handling
        4. Add helpful comments if requested
        5. Optimize for performance and efficiency
        6. Ensure the code meets all specified requirements
        
        When completing partial code, ensure that your additions integrate seamlessly with the existing code and maintain the same style and conventions.
        """

@registry.register(type="agent")
class CodeReviewAgent(Agent):
    """
    Agent for reviewing code.
    """
    
    def __init__(self, name: str = "CodeReviewAgent", description: str = None, model: str = None):
        """
        Initialize the code review agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Reviews code for issues, bugs, and improvement opportunities."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="review_code",
                description="Review code for issues and improvements",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language of the code"
                        },
                        "code": {
                            "type": "string",
                            "description": "Code to review"
                        },
                        "focus_areas": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Areas to focus on during review (e.g., performance, security, readability)"
                        }
                    },
                    "required": ["language", "code"]
                }
            ),
            Function(
                name="suggest_improvements",
                description="Suggest improvements for code",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language of the code"
                        },
                        "code": {
                            "type": "string",
                            "description": "Code to improve"
                        },
                        "improvement_type": {
                            "type": "string",
                            "description": "Type of improvement to suggest (e.g., performance, readability, security)"
                        }
                    },
                    "required": ["language", "code"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a thorough code review agent. Your task is to review code for issues, bugs, and improvement opportunities.
        
        Focus on these aspects:
        1. Code correctness and potential bugs
        2. Performance issues and optimizations
        3. Security vulnerabilities
        4. Code readability and maintainability
        5. Adherence to best practices and coding standards
        6. Potential edge cases and error handling
        
        Provide specific, actionable feedback with examples of how to improve the code when possible.
        """

@registry.register(type="agent")
class CodeRefactoringAgent(Agent):
    """
    Agent for refactoring code.
    """
    
    def __init__(self, name: str = "CodeRefactoringAgent", description: str = None, model: str = None):
        """
        Initialize the code refactoring agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Refactors code to improve quality, readability, and performance."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="refactor_code",
                description="Refactor code to improve quality",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language of the code"
                        },
                        "code": {
                            "type": "string",
                            "description": "Code to refactor"
                        },
                        "refactoring_goals": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Goals for the refactoring (e.g., improve performance, reduce complexity, enhance readability)"
                        }
                    },
                    "required": ["language", "code"]
                }
            ),
            Function(
                name="optimize_code",
                description="Optimize code for performance",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language of the code"
                        },
                        "code": {
                            "type": "string",
                            "description": "Code to optimize"
                        },
                        "optimization_target": {
                            "type": "string",
                            "description": "Target for optimization (e.g., speed, memory, readability)"
                        }
                    },
                    "required": ["language", "code"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are an expert code refactoring agent. Your task is to refactor code to improve its quality, readability, and performance.
        
        Apply these refactoring techniques as appropriate:
        1. Extract methods/functions to improve readability and reusability
        2. Rename variables and functions for clarity
        3. Simplify complex conditionals and loops
        4. Remove code duplication
        5. Apply design patterns where appropriate
        6. Optimize algorithms and data structures for performance
        7. Improve error handling and edge case management
        
        Ensure that the refactored code maintains the same functionality as the original code.
        """

@registry.register(type="agent")
class CodeExplanationAgent(Agent):
    """
    Agent for explaining code.
    """
    
    def __init__(self, name: str = "CodeExplanationAgent", description: str = None, model: str = None):
        """
        Initialize the code explanation agent.
        
        Args:
            name: Agent name
            description: Agent description
            model: Model to use for the agent
        """
        description = description or "Explains code functionality and implementation details."
        super().__init__(name=name, description=description, model=model)
        
        # Define functions
        self.functions = [
            Function(
                name="explain_code",
                description="Explain code functionality",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language of the code"
                        },
                        "code": {
                            "type": "string",
                            "description": "Code to explain"
                        },
                        "detail_level": {
                            "type": "string",
                            "enum": ["basic", "intermediate", "advanced"],
                            "description": "Level of detail for the explanation"
                        }
                    },
                    "required": ["language", "code"]
                }
            ),
            Function(
                name="document_code",
                description="Generate documentation for code",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language of the code"
                        },
                        "code": {
                            "type": "string",
                            "description": "Code to document"
                        },
                        "documentation_format": {
                            "type": "string",
                            "enum": ["inline", "docstring", "markdown"],
                            "description": "Format for the documentation"
                        }
                    },
                    "required": ["language", "code"]
                }
            )
        ]
        
        # Set system message
        self.system_message = """
        You are a clear and thorough code explanation agent. Your task is to explain code functionality and implementation details in an accessible way.
        
        When explaining code:
        1. Start with a high-level overview of what the code does
        2. Break down complex sections into simpler parts
        3. Explain the purpose of key variables, functions, and algorithms
        4. Highlight any notable patterns, optimizations, or techniques used
        5. Adjust the level of detail based on the requested detail level
        6. Use analogies or examples to clarify complex concepts
        
        When documenting code, follow the appropriate documentation standards for the specified language and format.
        """
