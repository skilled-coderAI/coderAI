# CoderAI - AI Integration Platform

![GitHub repo size](https://img.shields.io/github/repo-size/codeaashu/CoderAI)
![GitHub stars](https://img.shields.io/github/stars/codeaashu/CoderAI?style=social)
![GitHub forks](https://img.shields.io/github/forks/codeaashu/CoderAI?style=social)

CoderAI is a powerful SaaS platform that enables seamless integration with various AI solution providers and development tools. This application allows users to:

- Connect to local Ollama models or external AI providers
- Process and analyze documents using state-of-the-art AI models
- Generate embeddings using Hugging Face models
- Create and manage vector databases for semantic search
- Build custom AI workflows with a user-friendly interface
- Integrate with GitHub for automated code reviews and project management

## Features

- **Multi-Provider Integration**: Connect to Ollama, OpenAI, Anthropic, and other AI providers
- **Document Processing**: Upload and analyze documents with AI assistance
- **Vector Database**: Store and search through document embeddings
- **Custom Workflows**: Create tailored AI workflows for specific use cases
- **Analytics Dashboard**: Monitor usage and performance metrics
- **GitHub Integration**: Automated code reviews, pull request analysis, and issue tracking
- **Project Management**: Built-in tools for managing development workflows and tasks
- **Code Review**: AI-powered code analysis and improvement suggestions

## Technologies Used

![Python](https://img.shields.io/badge/python-%2314354C.svg?style=plastic&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-%23FF4B4B.svg?style=plastic&logo=streamlit&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=plastic&logo=react&logoColor=%2361DAFB)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=plastic&logo=tailwind-css&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=plastic&logo=github&logoColor=white)

## Getting Started

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key_here (optional)
   ANTHROPIC_API_KEY=your_anthropic_key_here (optional)
   HF_TOKEN=your_huggingface_token_here (optional)
   GITHUB_TOKEN=your_github_token_here (required for GitHub integration)
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## Requirements

- Python 3.9+
- Ollama installed locally (for local model integration)
- Internet connection (for external API access)

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
- `data/`: Data storage directory

## GitHub Integration

To use the GitHub integration features:

1. Generate a GitHub Personal Access Token with the following permissions:
   - repo (full access)
   - workflow
   - read:org

2. Add your GitHub token to the `.env` file

3. Configure your GitHub repositories in the application settings

## Code Review Features

- Automated code quality analysis
- Pull request review suggestions
- Security vulnerability scanning
- Best practices recommendations
- Performance optimization tips

## Contributing

If you want to contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a clear description of your changes

Please make sure to follow the existing code style and guidelines.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
