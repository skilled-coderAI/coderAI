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

## Requirements

- Python 3.9+
- Ollama installed locally (for local model integration)
- Internet connection (for external API access)
- pytest (for automated testing)
- WebSocket support (for real-time collaboration)

## Project Structure

- `app.py`: Main Streamlit application
- `config.py`: Configuration settings
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

## Code Review Features

- Automated code quality analysis
- Pull request review suggestions
- Security vulnerability scanning
- Best practices recommendations
- Performance optimization tips
- Real-time collaborative review sessions

## Contributing

If you want to contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a clear description of your changes

Please make sure to follow the existing code style and guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
