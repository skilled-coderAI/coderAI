#!/usr/bin/env python
"""
CoderAI CLI
Command-line interface for the CoderAI framework.
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table

# Import CoderAI framework
from framework import (
    MetaChain,
    registry,
    CoderAILogger,
    LoggerManager,
    pretty_print_messages,
)

# Initialize console
console = Console()

def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging for the CLI.
    
    Args:
        verbose: Whether to enable verbose logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    LoggerManager.setup(log_level=log_level)
    
def print_header() -> None:
    """
    Print the CoderAI CLI header.
    """
    header = """
    ██████╗ ██████╗ ██████╗ ███████╗██████╗  █████╗ ██╗
   ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██║
   ██║     ██║   ██║██║  ██║█████╗  ██████╔╝███████║██║
   ██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗██╔══██║██║
   ╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║██║  ██║██║
    ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
    """
    console.print(Panel.fit(header, title="CoderAI Framework", border_style="cyan"))
    
def list_agents() -> None:
    """
    List all available agents.
    """
    agents = registry.list_items(type="agent")
    
    if not agents:
        console.print("[yellow]No agents found in the registry.[/yellow]")
        return
        
    # Create table
    table = Table(title="Available Agents")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="green")
    
    # Add rows
    for agent_name, agent_info in agents.items():
        description = agent_info.get("description", "")
        table.add_row(agent_name, description)
        
    # Print table
    console.print(table)
    
def list_tools() -> None:
    """
    List all available tools.
    """
    tools = registry.list_items(type="tool")
    
    if not tools:
        console.print("[yellow]No tools found in the registry.[/yellow]")
        return
        
    # Create table
    table = Table(title="Available Tools")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="green")
    
    # Add rows
    for tool_name, tool_info in tools.items():
        description = tool_info.get("description", "")
        table.add_row(tool_name, description)
        
    # Print table
    console.print(table)
    
def list_workflows() -> None:
    """
    List all available workflows.
    """
    workflows = registry.list_items(type="workflow")
    
    if not workflows:
        console.print("[yellow]No workflows found in the registry.[/yellow]")
        return
        
    # Create table
    table = Table(title="Available Workflows")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="green")
    
    # Add rows
    for workflow_name, workflow_info in workflows.items():
        description = workflow_info.get("description", "")
        table.add_row(workflow_name, description)
        
    # Print table
    console.print(table)
    
def chat_with_agent(agent_name: str, model: str = None) -> None:
    """
    Start an interactive chat with an agent.
    
    Args:
        agent_name: Name of the agent to chat with
        model: Model to use for the agent
    """
    # Check if agent exists
    agent_info = registry.get_item(agent_name, type="agent")
    if not agent_info:
        console.print(f"[red]Agent '{agent_name}' not found in the registry.[/red]")
        return
        
    # Create agent
    agent_class = agent_info["class"]
    agent = agent_class(model=model)
    
    # Create MetaChain
    meta_chain = MetaChain()
    
    # Add agent to MetaChain
    meta_chain.add_agent(agent)
    
    console.print(f"[green]Starting chat with {agent_name}. Type 'exit' to end the conversation.[/green]")
    console.print(f"[cyan]Agent description: {agent.description}[/cyan]")
    
    # Start chat loop
    messages = []
    while True:
        # Get user input
        user_input = console.input("[bold green]You: [/bold green]")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit", "bye"]:
            console.print("[yellow]Ending conversation.[/yellow]")
            break
            
        # Add user message
        messages.append({"role": "user", "content": user_input})
        
        # Get agent response
        response = meta_chain.chat_completion(messages=messages, agent=agent)
        
        # Add agent message
        messages.append({"role": "assistant", "content": response.content})
        
        # Print agent response
        console.print(f"[bold blue]{agent_name}: [/bold blue]{response.content}")
        
def execute_workflow(workflow_name: str, parameters: Dict[str, Any] = None) -> None:
    """
    Execute a workflow with specified parameters.
    
    Args:
        workflow_name: Name of the workflow to execute
        parameters: Parameters for the workflow execution
    """
    # Check if workflow exists
    workflow_info = registry.get_item(workflow_name, type="workflow")
    if not workflow_info:
        console.print(f"[red]Workflow '{workflow_name}' not found in the registry.[/red]")
        return
        
    # Create workflow
    workflow_class = workflow_info["class"]
    workflow = workflow_class()
    
    # Execute workflow
    try:
        console.print(f"[green]Executing workflow '{workflow_name}'...[/green]")
        result = workflow.execute(parameters or {})
        
        # Print result
        console.print("[bold green]Workflow execution completed.[/bold green]")
        console.print(Panel(str(result), title="Workflow Result", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error executing workflow: {str(e)}[/red]")
        
def create_agent_from_description(name: str, description: str, model: str = None) -> None:
    """
    Create a new agent from a natural language description.
    
    Args:
        name: Name for the new agent
        description: Natural language description of the agent
        model: Model to use for the agent
    """
    try:
        # Create MetaChain
        meta_chain = MetaChain()
        
        console.print(f"[green]Creating agent '{name}' from description...[/green]")
        
        # Create agent
        agent = meta_chain.create_agent_from_description(name=name, description=description, model=model)
        
        # Register agent
        registry.register_item(agent, type="agent")
        
        console.print(f"[bold green]Agent '{name}' created and registered successfully.[/bold green]")
        console.print(f"[cyan]Description: {agent.description}[/cyan]")
        
        if agent.functions:
            console.print("[cyan]Functions:[/cyan]")
            for function in agent.functions:
                console.print(f"  - {function.name}: {function.description}")
    except Exception as e:
        console.print(f"[red]Error creating agent: {str(e)}[/red]")
        
def create_workflow_from_description(name: str, description: str) -> None:
    """
    Create a new workflow from a natural language description.
    
    Args:
        name: Name for the new workflow
        description: Natural language description of the workflow
    """
    try:
        # Create MetaChain
        meta_chain = MetaChain()
        
        console.print(f"[green]Creating workflow '{name}' from description...[/green]")
        
        # Create workflow
        workflow = meta_chain.create_workflow_from_description(name=name, description=description)
        
        # Register workflow
        registry.register_item(workflow, type="workflow")
        
        console.print(f"[bold green]Workflow '{name}' created and registered successfully.[/bold green]")
        console.print(f"[cyan]Description: {workflow.description}[/cyan]")
        
        if hasattr(workflow, "steps") and workflow.steps:
            console.print("[cyan]Steps:[/cyan]")
            for i, step in enumerate(workflow.steps):
                console.print(f"  {i+1}. {step.name}: {step.description}")
    except Exception as e:
        console.print(f"[red]Error creating workflow: {str(e)}[/red]")
        
def main() -> None:
    """
    Main entry point for the CoderAI CLI.
    """
    # Create argument parser
    parser = argparse.ArgumentParser(description="CoderAI Command Line Interface")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List agents command
    list_agents_parser = subparsers.add_parser("list-agents", help="List all available agents")
    
    # List tools command
    list_tools_parser = subparsers.add_parser("list-tools", help="List all available tools")
    
    # List workflows command
    list_workflows_parser = subparsers.add_parser("list-workflows", help="List all available workflows")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start an interactive chat with an agent")
    chat_parser.add_argument("agent", help="Name of the agent to chat with")
    chat_parser.add_argument("--model", "-m", help="Model to use for the agent")
    
    # Execute workflow command
    execute_parser = subparsers.add_parser("execute", help="Execute a workflow with specified parameters")
    execute_parser.add_argument("workflow", help="Name of the workflow to execute")
    execute_parser.add_argument("--parameters", "-p", help="Parameters for the workflow execution (JSON string)")
    
    # Create agent command
    create_agent_parser = subparsers.add_parser("create-agent", help="Create a new agent from a natural language description")
    create_agent_parser.add_argument("name", help="Name for the new agent")
    create_agent_parser.add_argument("description", help="Natural language description of the agent")
    create_agent_parser.add_argument("--model", "-m", help="Model to use for the agent")
    
    # Create workflow command
    create_workflow_parser = subparsers.add_parser("create-workflow", help="Create a new workflow from a natural language description")
    create_workflow_parser.add_argument("name", help="Name for the new workflow")
    create_workflow_parser.add_argument("description", help="Natural language description of the workflow")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(verbose=args.verbose)
    
    # Print header
    print_header()
    
    # Execute command
    if args.command == "list-agents":
        list_agents()
    elif args.command == "list-tools":
        list_tools()
    elif args.command == "list-workflows":
        list_workflows()
    elif args.command == "chat":
        chat_with_agent(args.agent, model=args.model)
    elif args.command == "execute":
        parameters = None
        if args.parameters:
            try:
                parameters = json.loads(args.parameters)
            except json.JSONDecodeError:
                console.print("[red]Error: Parameters must be a valid JSON string.[/red]")
                return
        execute_workflow(args.workflow, parameters=parameters)
    elif args.command == "create-agent":
        create_agent_from_description(args.name, args.description, model=args.model)
    elif args.command == "create-workflow":
        create_workflow_from_description(args.name, args.description)
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
