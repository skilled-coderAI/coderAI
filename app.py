import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Workaround for PyTorch-Streamlit interaction issues
import sys
original_import = __import__

def patched_import(name, globals=None, locals=None, fromlist=(), level=0):
    # Skip watching PyTorch modules to avoid file watcher errors
    if name.startswith('torch'):
        if fromlist and '__path__' in fromlist:
            fromlist = tuple(item for item in fromlist if item != '__path__')
    
    return original_import(name, globals, locals, fromlist, level)

sys.__import__ = patched_import

# Set environment variable to handle PyTorch-Streamlit interaction issues
os.environ["STREAMLIT_WATCH_EXCLUDE_MODULES"] = "torch,torchvision,torchaudio"

# Filter out PyTorch-related error messages
class ErrorFilter:
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr

    def write(self, message):
        # Filter out PyTorch errors related to __path__._path
        if "RuntimeError: Tried to instantiate class '__path__._path'" not in message and \
           "Examining the path of torch.classes raised" not in message:
            self.original_stderr.write(message)

    def flush(self):
        self.original_stderr.flush()

# Apply the filter to stderr
sys.stderr = ErrorFilter(sys.stderr)

# Import custom modules
from config import AppConfig
from components.sidebar import render_sidebar
from components.main_panel import render_main_panel
from components.provider_config import render_provider_config
from components.code_review import render_code_review
from components.github_integration import render_github_integration
from components.agent_panel import render_agent_panel
from services.model_service import ModelService
from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
from services.agent_core import CoderAIAgentCore
from components.project_management import ProjectManagement

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="CoderAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'config' not in st.session_state:
        st.session_state.config = AppConfig()
    
    if 'model_service' not in st.session_state:
        st.session_state.model_service = ModelService()
    
    if 'embedding_service' not in st.session_state:
        st.session_state.embedding_service = EmbeddingService()
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = VectorStoreService()
    
    if 'agent_core' not in st.session_state:
        st.session_state.agent_core = CoderAIAgentCore(
            model_service=st.session_state.model_service,
            embedding_service=st.session_state.embedding_service
        )
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    
    if 'providers' not in st.session_state:
        st.session_state.providers = {
            "ollama": {"active": True, "base_url": "http://localhost:11434"},
            "openai": {"active": False, "api_key": os.getenv("OPENAI_API_KEY", "")},
            "anthropic": {"active": False, "api_key": os.getenv("ANTHROPIC_API_KEY", "")},
            "huggingface": {"active": True, "token": os.getenv("HF_TOKEN", "")}
        }

def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4B8BF5;
        margin-bottom: 0.5rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #5F6368;
        margin-bottom: 1.5rem;
    }
    .stButton button {
        background-color: #4B8BF5;
        color: white;
        border-radius: 5px;
    }
    .provider-card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    /* Logo styling */
    img {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    /* Header container styling */
    .stColumn > div:first-child {
        display: flex;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Render main panel based on current page
    if st.session_state.current_page == "Home":
        render_main_panel()
    elif st.session_state.current_page == "Provider Configuration":
        render_provider_config()
    elif st.session_state.current_page == "Code Review":
        render_code_review()
    elif st.session_state.current_page == "GitHub Integration":
        render_github_integration()
    elif st.session_state.current_page == "Agent Framework":
        render_agent_panel()

# Initialize project management
project_mgmt = ProjectManagement()

if __name__ == "__main__":
    main()
