# CoderAI - AI PaaS solution

![GitHub repo size](https://img.shields.io/github/repo-size/skilled-coderAI/coderAI)
![GitHub stars](https://img.shields.io/github/stars/skilled-coderAI/coderAI?style=social)
![GitHub forks](https://img.shields.io/github/forks/skilled-coderAI/coderAI?style=social)

CoderAI is a powerful SaaS platform that enables seamless integration with various AI solution providers and development tools. This application allows users to:

- Connect to local Ollama models or external AI providers
- Process and analyze documents using state-of-the-art AI models
- Generate embeddings using Hugging Face models
- Create and manage vector databases for semantic search
- Build custom AI workflows with a user-friendly interface
- Integrate with GitHub for automated code reviews and project management
- Real-time code collaboration with multiple developers
- Automated testing and continuous integration
- Create and customize AI agents using natural language
- Build complex workflows with multiple agents and tools
- Leverage advanced memory management for context-aware AI

## Features

- **Multi-Provider Integration**: Connect to Ollama, OpenAI, Anthropic, and other AI providers
- **Document Processing**: Upload and analyze documents with AI assistance
- **Vector Database**: Store and search through document embeddings
- **Custom Workflows**: Create tailored AI workflows for specific use cases
- **Analytics Dashboard**: Monitor usage and performance metrics
- **GitHub Integration**: Automated code reviews, pull request analysis, and issue tracking
- **Project Management**: Built-in tools for managing development workflows and tasks
- **Code Review**: AI-powered code analysis and improvement suggestions
- **Real-time Collaboration**: Multi-user code editing and pair programming
- **Automated Testing**: Integrated test discovery, execution, and reporting
- **Test History**: Track and analyze test results over time
- **Session Management**: Monitor active collaboration sessions and participants
- **Agent Framework**: Create, customize, and deploy AI agents using natural language
- **Workflow Management**: Build and execute complex workflows with multiple steps and agents
- **Tool Registry**: Register and manage custom tools for agents to use
- **Memory Management**: Store and retrieve context for more effective AI interactions
- **RAG Capabilities**: Implement Retrieval-Augmented Generation for knowledge-intensive tasks
- **CLI Interface**: Access all framework features through a powerful command-line interface

## Project Structure

- `app.py`: Main Streamlit application
- `config.py`: Configuration settings
- `cli.py`: Command-line interface for the CoderAI framework
- `models/`: Model integration modules
- `utils/`: Utility functions
- `components/`: Streamlit UI components
  - `code_review.py`: Code review interface and logic
  - `github_integration.py`: GitHub API integration
  - `project_management.py`: Project management features
- `services/`: Core services
  - `embedding_service.py`: Text embedding generation
  - `vector_store_service.py`: Vector database management
  - `github_service.py`: GitHub API service
  - `code_analysis_service.py`: Code analysis and review
  - `collaboration_service.py`: Real-time code collaboration
  - `testing_service.py`: Automated testing integration
- `data/`: Data storage directory
- `framework/`: CoderAI Framework components
  - `core.py`: Core framework functionality
  - `types.py`: Data structure definitions
  - `registry.py`: Tool and agent registry
  - `util.py`: Utility functions
  - `logger.py`: Logging system
  - `constants.py`: Framework constants
  - `fn_call_converter.py`: Function call conversion utilities
  - `agents/`: Agent implementations
    - `code_agent.py`: Code-related agents
    - `research_agent.py`: Research-related agents
    - `assistant_agent.py`: Assistant-related agents
    - `workflow_agent.py`: Workflow-related agents
  - `tools/`: Tool implementations
    - `file_tools.py`: File operation tools
    - `web_tools.py`: Web operation tools
    - `terminal_tools.py`: Terminal operation tools
    - `rag_tools.py`: RAG-related tools
  - `flow/`: Workflow management
    - `core.py`: Workflow execution engine
    - `types.py`: Workflow data structures
  - `memory/`: Memory management
    - `core.py`: Memory storage and retrieval
    - `types.py`: Memory data structures

## CoderAI Framework

The CoderAI Framework is a powerful agent-based system that allows you to:

### Agent Framework
- Create custom AI agents using natural language descriptions
- Customize agent behavior with specific functions and system messages
- Deploy agents for various tasks like code generation, research, and assistance
- Combine multiple agents to solve complex problems

### Workflow Management
- Create workflows that coordinate multiple agents and tools
- Define complex multi-step processes with dependencies
- Handle events and triggers for automated execution
- Monitor and manage workflow execution

### Tool Registry
- Register custom tools for agents to use
- Manage tool availability and permissions
- Discover available tools through the registry
- Create new tools using natural language descriptions

### Memory Management
- Store and retrieve context for more effective AI interactions
- Implement short-term and long-term memory for agents
- Search through memories using semantic similarity
- Group related memories for better organization

### RAG Capabilities
- Implement Retrieval-Augmented Generation for knowledge-intensive tasks
- Index and search through documents and knowledge bases
- Generate responses grounded in specific knowledge sources
- Customize chunking and embedding strategies

### CLI Interface
- Access all framework features through a powerful command-line interface
- Create and chat with agents
- Execute workflows with custom parameters
- List available agents, tools, and workflows

## Code Review Features

- Automated code quality analysis
- Pull request review suggestions
- Security vulnerability scanning
- Best practices recommendations
- Performance optimization tips
- Real-time collaborative review sessions

## Using the CLI

```bash
# List all available agents
python cli.py list-agents

# List all available tools
python cli.py list-tools

# List all available workflows
python cli.py list-workflows

# Chat with an agent
python cli.py chat CodeGenerationAgent

# Execute a workflow
python cli.py execute CodeReviewWorkflow --parameters '{"repo_url": "https://github.com/user/repo", "branch": "main"}'

# Create a new agent from description
python cli.py create-agent CustomAgent "An agent that helps with database schema design and optimization"

# Create a new workflow from description
python cli.py create-workflow DataProcessingWorkflow "A workflow that processes CSV data, cleans it, and generates insights"
```

## Contributing

If you want to contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a clear description of your changes

Please make sure to follow the existing code style and guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
