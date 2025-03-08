#!/usr/bin/env python
"""
Basic Agent Example
This example demonstrates how to create and interact with a basic agent using the CoderAI framework.
"""

import os
import sys
from rich.console import Console

# Add parent directory to path to import framework
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import CoderAI framework
from framework import MetaChain, Agent, Message, Function, registry

# Initialize console
console = Console()

def main():
    """
    Main function for the basic agent example.
    """
    console.print("[bold green]CoderAI Framework - Basic Agent Example[/bold green]")
    
    # Create MetaChain
    meta_chain = MetaChain()
    
    # Create a custom agent
    agent = Agent(
        name="GreetingAgent",
        description="A simple agent that greets users and provides information about CoderAI.",
        model="gpt-3.5-turbo"  # You can change this to your preferred model
    )
    
    # Define functions for the agent
    agent.functions = [
        Function(
            name="greet_user",
            description="Greet the user with a personalized message",
            parameters={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the user to greet"
                    },
                    "time_of_day": {
                        "type": "string",
                        "enum": ["morning", "afternoon", "evening", "night"],
                        "description": "Time of day for the greeting"
                    }
                },
                "required": ["name"]
            }
        ),
        Function(
            name="provide_info",
            description="Provide information about CoderAI",
            parameters={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to provide information about"
                    },
                    "detail_level": {
                        "type": "string",
                        "enum": ["basic", "intermediate", "advanced"],
                        "description": "Level of detail for the information"
                    }
                },
                "required": ["topic"]
            }
        )
    ]
    
    # Set system message for the agent
    agent.system_message = """
    You are a helpful assistant for the CoderAI framework. Your task is to greet users and provide information about CoderAI.
    
    When greeting users:
    1. Be friendly and personalized
    2. Adjust your greeting based on the time of day
    3. Make the user feel welcome
    
    When providing information about CoderAI:
    1. Focus on the requested topic
    2. Adjust the level of detail based on the requested detail level
    3. Highlight the key features and capabilities
    4. Be accurate and informative
    
    CoderAI is a powerful framework for creating and managing AI agents, workflows, and tools. It includes features like:
    - Agent framework with natural language customization
    - Workflow management system
    - Tool registry and management
    - Memory management
    - RAG capabilities
    - CLI interface
    """
    
    # Add agent to MetaChain
    meta_chain.add_agent(agent)
    
    # Register agent
    registry.register_item(agent, type="agent")
    
    console.print(f"[cyan]Created agent: {agent.name}[/cyan]")
    console.print(f"[cyan]Description: {agent.description}[/cyan]")
    
    # Start conversation
    messages = []
    
    # Add user message
    user_message = "Hi, I'm Jay. Can you tell me about the CoderAI framework?"
    messages.append({"role": "user", "content": user_message})
    
    console.print(f"[bold green]User: [/bold green]{user_message}")
    
    # Get agent response
    response = meta_chain.chat_completion(messages=messages, agent=agent)
    
    # Add agent message
    messages.append({"role": "assistant", "content": response.content})
    
    console.print(f"[bold blue]{agent.name}: [/bold blue]{response.content}")
    
    # Add another user message
    user_message = "What can I do with the workflow management system?"
    messages.append({"role": "user", "content": user_message})
    
    console.print(f"[bold green]User: [/bold green]{user_message}")
    
    # Get agent response
    response = meta_chain.chat_completion(messages=messages, agent=agent)
    
    # Add agent message
    messages.append({"role": "assistant", "content": response.content})
    
    console.print(f"[bold blue]{agent.name}: [/bold blue]{response.content}")
    
    console.print("[bold green]Example completed![/bold green]")

if __name__ == "__main__":
    main()
