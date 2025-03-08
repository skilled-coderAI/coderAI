#!/usr/bin/env python
"""
RAG Example
This example demonstrates how to use the Retrieval-Augmented Generation (RAG) capabilities
of the CoderAI framework to create a knowledge-based agent.
"""

import os
import sys
from rich.console import Console

# Add parent directory to path to import framework
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import CoderAI framework
from framework import MetaChain, Agent, Message, Function, registry
from framework.tools.rag_tools import add_document, search_documents, rag_store

# Initialize console
console = Console()

def main():
    """
    Main function for the RAG example.
    """
    console.print("[bold green]CoderAI Framework - RAG Example[/bold green]")
    
    # Create MetaChain
    meta_chain = MetaChain()
    
    # Create a knowledge base with some documents
    console.print("[bold]Creating knowledge base...[/bold]")
    
    # Add documents to the RAG store
    python_doc = """
    # Python Programming Language
    
    Python is a high-level, interpreted programming language known for its readability and versatility.
    
    ## Key Features
    
    - Easy to learn and use
    - Extensive standard library
    - Dynamic typing and memory management
    - Support for multiple programming paradigms (procedural, object-oriented, functional)
    - Large and active community
    
    ## Common Use Cases
    
    - Web development
    - Data analysis and visualization
    - Machine learning and AI
    - Automation and scripting
    - Scientific computing
    
    ## Basic Syntax
    
    ```python
    # Hello World
    print("Hello, World!")
    
    # Variables
    x = 10
    name = "Python"
    
    # Conditional statements
    if x > 5:
        print("x is greater than 5")
    else:
        print("x is not greater than 5")
    
    # Loops
    for i in range(5):
        print(i)
    
    # Functions
    def greet(name):
        return f"Hello, {name}!"
    ```
    """
    
    javascript_doc = """
    # JavaScript Programming Language
    
    JavaScript is a high-level, interpreted programming language primarily used for web development.
    
    ## Key Features
    
    - Client-side scripting for web browsers
    - Event-driven programming
    - Prototype-based object-oriented programming
    - First-class functions
    - Dynamic typing
    
    ## Common Use Cases
    
    - Web development (front-end and back-end with Node.js)
    - Mobile app development (React Native, Ionic)
    - Desktop applications (Electron)
    - Game development
    - Server-side programming (Node.js)
    
    ## Basic Syntax
    
    ```javascript
    // Hello World
    console.log("Hello, World!");
    
    // Variables
    let x = 10;
    const name = "JavaScript";
    
    // Conditional statements
    if (x > 5) {
        console.log("x is greater than 5");
    } else {
        console.log("x is not greater than 5");
    }
    
    // Loops
    for (let i = 0; i < 5; i++) {
        console.log(i);
    }
    
    // Functions
    function greet(name) {
        return `Hello, ${name}!`;
    }
    ```
    """
    
    machine_learning_doc = """
    # Machine Learning Basics
    
    Machine learning is a subset of artificial intelligence that focuses on developing systems that can learn from data.
    
    ## Key Concepts
    
    - Supervised learning
    - Unsupervised learning
    - Reinforcement learning
    - Feature engineering
    - Model evaluation and validation
    
    ## Common Algorithms
    
    - Linear regression
    - Logistic regression
    - Decision trees
    - Random forests
    - Support vector machines
    - Neural networks
    - K-means clustering
    
    ## Popular Libraries
    
    - scikit-learn (Python)
    - TensorFlow (Python, C++, JavaScript)
    - PyTorch (Python)
    - Keras (Python)
    - XGBoost (multiple languages)
    
    ## Basic Workflow
    
    1. Data collection and preparation
    2. Feature selection and engineering
    3. Model selection and training
    4. Model evaluation and tuning
    5. Deployment and monitoring
    """
    
    # Add documents to the RAG store
    add_document(content=python_doc, metadata={"topic": "programming", "language": "Python"})
    add_document(content=javascript_doc, metadata={"topic": "programming", "language": "JavaScript"})
    add_document(content=machine_learning_doc, metadata={"topic": "machine learning"})
    
    console.print("[green]Added 3 documents to the knowledge base[/green]")
    
    # Create a RAG-powered agent
    agent = Agent(
        name="KnowledgeAgent",
        description="An agent that answers questions using a knowledge base of programming and machine learning information.",
        model="gpt-3.5-turbo"  # You can change this to your preferred model
    )
    
    # Define functions for the agent
    agent.functions = [
        Function(
            name="answer_question",
            description="Answer a question using the knowledge base",
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
                    }
                },
                "required": ["question"]
            }
        ),
        Function(
            name="search_knowledge_base",
            description="Search the knowledge base for relevant information",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return"
                    }
                },
                "required": ["query"]
            }
        )
    ]
    
    # Set system message for the agent
    agent.system_message = """
    You are a knowledgeable assistant powered by a RAG (Retrieval-Augmented Generation) system.
    Your task is to answer questions using the information from your knowledge base.
    
    When answering questions:
    1. Search the knowledge base for relevant information
    2. Use the retrieved information to formulate your answer
    3. Be accurate and informative
    4. Acknowledge when information is not available in your knowledge base
    5. Provide code examples when appropriate
    
    Your knowledge base contains information about programming languages (Python, JavaScript)
    and machine learning concepts.
    """
    
    # Add agent to MetaChain
    meta_chain.add_agent(agent)
    
    # Register agent
    registry.register_item(agent, type="agent")
    
    console.print(f"[cyan]Created agent: {agent.name}[/cyan]")
    console.print(f"[cyan]Description: {agent.description}[/cyan]")
    
    # Define a function to search the knowledge base and augment the agent's context
    def rag_augmented_chat(question):
        # Search the knowledge base
        search_results = search_documents(query=question, k=2)
        
        if search_results["success"] and search_results["count"] > 0:
            # Extract relevant information from search results
            context = "\n\n".join([result["content"] for result in search_results["results"]])
            
            # Create messages with context
            messages = [
                {"role": "system", "content": agent.system_message},
                {"role": "user", "content": f"Question: {question}\n\nRelevant information from knowledge base:\n{context}"}
            ]
        else:
            # Create messages without context
            messages = [
                {"role": "system", "content": agent.system_message},
                {"role": "user", "content": f"Question: {question}"}
            ]
        
        # Get agent response
        response = meta_chain.chat_completion(messages=messages, agent=agent)
        
        return response.content
    
    # Example questions
    questions = [
        "What are the key features of Python?",
        "How do you write a for loop in JavaScript?",
        "What are some common machine learning algorithms?",
        "Compare Python and JavaScript syntax for defining functions."
    ]
    
    # Answer questions using RAG
    for question in questions:
        console.print(f"\n[bold green]Question: [/bold green]{question}")
        
        answer = rag_augmented_chat(question)
        
        console.print(f"[bold blue]Answer: [/bold blue]{answer}")
    
    console.print("\n[bold green]Example completed![/bold green]")

if __name__ == "__main__":
    main()
