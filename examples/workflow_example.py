#!/usr/bin/env python
"""
Workflow Example
This example demonstrates how to create and execute a workflow using the CoderAI framework.
"""

import os
import sys
from rich.console import Console

# Add parent directory to path to import framework
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import CoderAI framework
from framework import MetaChain, registry
from framework.flow.types import Workflow, WorkflowStep, Event, EventType
from framework.agents.code_agent import CodeGenerationAgent, CodeReviewAgent
from framework.tools.file_tools import read_file, write_file

# Initialize console
console = Console()

def main():
    """
    Main function for the workflow example.
    """
    console.print("[bold green]CoderAI Framework - Workflow Example[/bold green]")
    
    # Create MetaChain
    meta_chain = MetaChain()
    
    # Create agents
    code_generation_agent = CodeGenerationAgent()
    code_review_agent = CodeReviewAgent()
    
    # Add agents to MetaChain
    meta_chain.add_agent(code_generation_agent)
    meta_chain.add_agent(code_review_agent)
    
    # Create workflow
    workflow = Workflow(
        name="CodeGenerationWorkflow",
        description="A workflow that generates code based on requirements and then reviews it."
    )
    
    # Create workflow steps
    step1 = WorkflowStep(
        name="GenerateCode",
        description="Generate code based on requirements",
        agent=code_generation_agent,
        function_name="generate_code",
        input_mapping={
            "language": "language",
            "requirements": "requirements",
            "include_comments": "include_comments"
        }
    )
    
    step2 = WorkflowStep(
        name="ReviewCode",
        description="Review the generated code",
        agent=code_review_agent,
        function_name="review_code",
        input_mapping={
            "language": "language",
            "code": "step:GenerateCode.output.code",
            "focus_areas": "focus_areas"
        }
    )
    
    step3 = WorkflowStep(
        name="SaveCode",
        description="Save the generated code to a file",
        tool=write_file,
        input_mapping={
            "file_path": "output_file",
            "content": "step:GenerateCode.output.code",
            "overwrite": True
        }
    )
    
    # Add steps to workflow
    workflow.add_step(step1)
    workflow.add_step(step2)
    workflow.add_step(step3)
    
    # Register workflow
    registry.register_item(workflow, type="workflow")
    
    console.print(f"[cyan]Created workflow: {workflow.name}[/cyan]")
    console.print(f"[cyan]Description: {workflow.description}[/cyan]")
    console.print(f"[cyan]Steps: {', '.join([step.name for step in workflow.steps])}")
    
    # Execute workflow
    console.print("[bold]Executing workflow...[/bold]")
    
    # Define workflow parameters
    parameters = {
        "language": "python",
        "requirements": "Create a function that calculates the Fibonacci sequence up to n terms.",
        "include_comments": True,
        "focus_areas": ["performance", "readability", "best practices"],
        "output_file": "fibonacci.py"
    }
    
    # Execute workflow
    result = workflow.execute(parameters)
    
    # Print result
    console.print("[bold green]Workflow execution completed![/bold green]")
    console.print("[bold]Result:[/bold]")
    
    for step_name, step_result in result.items():
        console.print(f"[bold cyan]Step: {step_name}[/bold cyan]")
        console.print(step_result)
        console.print()
    
    console.print("[bold green]Example completed![/bold green]")

if __name__ == "__main__":
    main()
