"""
CoderAI Framework Agents
This module provides agents for the CoderAI framework.
"""

# Import agent modules
from . import code_agent
from . import research_agent
from . import assistant_agent
from . import workflow_agent

# Import all agents
from .code_agent import *
from .research_agent import *
from .assistant_agent import *
from .workflow_agent import *

__all__ = [
    # Code agents
    "CodeGenerationAgent",
    "CodeReviewAgent",
    "CodeRefactoringAgent",
    "CodeExplanationAgent",
    
    # Research agents
    "ResearchAgent",
    "DocumentationAgent",
    "AnalysisAgent",
    
    # Assistant agents
    "AssistantAgent",
    "QuestionAnsweringAgent",
    "TaskManagementAgent",
    
    # Workflow agents
    "WorkflowAgent",
    "PipelineAgent",
]
