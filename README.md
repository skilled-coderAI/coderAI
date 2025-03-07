# CoderAI - AI Integration Platform

CoderAI is a powerful SaaS platform that enables seamless integration with various AI solution providers. This application allows users to:

- Connect to local Ollama models or external AI providers
- Process and analyze documents using state-of-the-art AI models
- Generate embeddings using Hugging Face models
- Create and manage vector databases for semantic search
- Build custom AI workflows with a user-friendly interface

## Features

- **Multi-Provider Integration**: Connect to Ollama, OpenAI, Anthropic, and other AI providers
- **Document Processing**: Upload and analyze documents with AI assistance
- **Vector Database**: Store and search through document embeddings
- **Custom Workflows**: Create tailored AI workflows for specific use cases
- **Analytics Dashboard**: Monitor usage and performance metrics

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
- `services/`: Core services (embedding, vector store, etc.)
- `data/`: Data storage directory
