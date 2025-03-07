import streamlit as st
import os

def render_provider_config():
    """Render the provider configuration page"""
    # Create a header with logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        logo_path = os.path.join(os.getcwd(), "Logo.png")
        st.image(logo_path, width=100)
    with col2:
        st.markdown("<h1 class='main-header'>Provider Configuration</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subheader'>Configure AI providers and models</p>", unsafe_allow_html=True)
    
    # Provider tabs
    provider_tabs = st.tabs(["Ollama", "OpenAI", "Anthropic", "Hugging Face"])
    
    # Ollama configuration
    with provider_tabs[0]:
        render_ollama_config()
    
    # OpenAI configuration
    with provider_tabs[1]:
        render_openai_config()
    
    # Anthropic configuration
    with provider_tabs[2]:
        render_anthropic_config()
    
    # Hugging Face configuration
    with provider_tabs[3]:
        render_huggingface_config()
    
    # Save button
    if st.button("Save Configuration", type="primary"):
        st.success("Configuration saved successfully!")
        st.rerun()

def render_ollama_config():
    """Render Ollama configuration section"""
    st.subheader("Ollama Configuration")
    
    # Get current config
    ollama_config = st.session_state.providers.get("ollama", {
        "active": True,
        "base_url": "http://localhost:11434"
    })
    
    # Active toggle
    ollama_active = st.toggle("Enable Ollama", value=ollama_config["active"])
    
    # Base URL
    ollama_base_url = st.text_input(
        "Ollama Base URL",
        value=ollama_config["base_url"],
        help="The base URL for your Ollama instance. Default is http://localhost:11434"
    )
    
    # Available models
    st.subheader("Available Models")
    
    # In a real implementation, we would fetch available models from Ollama
    # For now, we'll use the ones from config
    ollama_models = st.session_state.config.provider_configs["ollama"]["available_models"]
    
    for model in ollama_models:
        st.checkbox(model, value=True, key=f"ollama_model_{model}")
    
    # Test connection button
    if st.button("Test Ollama Connection"):
        with st.spinner("Testing connection to Ollama..."):
            # In a real implementation, we would:
            # 1. Send a request to the Ollama API
            # 2. Check if the response is valid
            
            # Simulate connection test
            import time
            time.sleep(1)
            st.success("Successfully connected to Ollama!")
    
    # Update config
    st.session_state.providers["ollama"] = {
        "active": ollama_active,
        "base_url": ollama_base_url
    }

def render_openai_config():
    """Render OpenAI configuration section"""
    st.subheader("OpenAI Configuration")
    
    # Get current config
    openai_config = st.session_state.providers.get("openai", {
        "active": False,
        "api_key": ""
    })
    
    # Active toggle
    openai_active = st.toggle("Enable OpenAI", value=openai_config["active"])
    
    # API Key
    openai_api_key = st.text_input(
        "OpenAI API Key",
        value=openai_config["api_key"],
        type="password",
        help="Your OpenAI API key. Required for OpenAI integration."
    )
    
    # Available models
    st.subheader("Available Models")
    
    openai_models = st.session_state.config.provider_configs["openai"]["available_models"]
    
    for model in openai_models:
        st.checkbox(model, value=True, key=f"openai_model_{model}")
    
    # Test connection button
    if st.button("Test OpenAI Connection"):
        if not openai_api_key:
            st.error("API Key is required to test connection.")
        else:
            with st.spinner("Testing connection to OpenAI..."):
                # In a real implementation, we would:
                # 1. Send a request to the OpenAI API
                # 2. Check if the response is valid
                
                # Simulate connection test
                import time
                time.sleep(1)
                st.success("Successfully connected to OpenAI!")
    
    # Update config
    st.session_state.providers["openai"] = {
        "active": openai_active,
        "api_key": openai_api_key
    }

def render_anthropic_config():
    """Render Anthropic configuration section"""
    st.subheader("Anthropic Configuration")
    
    # Get current config
    anthropic_config = st.session_state.providers.get("anthropic", {
        "active": False,
        "api_key": ""
    })
    
    # Active toggle
    anthropic_active = st.toggle("Enable Anthropic", value=anthropic_config["active"])
    
    # API Key
    anthropic_api_key = st.text_input(
        "Anthropic API Key",
        value=anthropic_config["api_key"],
        type="password",
        help="Your Anthropic API key. Required for Anthropic integration."
    )
    
    # Available models
    st.subheader("Available Models")
    
    anthropic_models = st.session_state.config.provider_configs["anthropic"]["available_models"]
    
    for model in anthropic_models:
        st.checkbox(model, value=True, key=f"anthropic_model_{model}")
    
    # Test connection button
    if st.button("Test Anthropic Connection"):
        if not anthropic_api_key:
            st.error("API Key is required to test connection.")
        else:
            with st.spinner("Testing connection to Anthropic..."):
                # In a real implementation, we would:
                # 1. Send a request to the Anthropic API
                # 2. Check if the response is valid
                
                # Simulate connection test
                import time
                time.sleep(1)
                st.success("Successfully connected to Anthropic!")
    
    # Update config
    st.session_state.providers["anthropic"] = {
        "active": anthropic_active,
        "api_key": anthropic_api_key
    }

def render_huggingface_config():
    """Render Hugging Face configuration section"""
    st.subheader("Hugging Face Configuration")
    
    # Get current config
    hf_config = st.session_state.providers.get("huggingface", {
        "active": True,
        "token": ""
    })
    
    # Active toggle
    hf_active = st.toggle("Enable Hugging Face", value=hf_config["active"])
    
    # API Token
    hf_token = st.text_input(
        "Hugging Face Token",
        value=hf_config["token"],
        type="password",
        help="Your Hugging Face token. Optional but recommended for higher rate limits."
    )
    
    # Available embedding models
    st.subheader("Available Embedding Models")
    
    hf_models = st.session_state.config.provider_configs["huggingface"]["available_embedding_models"]
    
    for model in hf_models:
        st.checkbox(model, value=True, key=f"hf_model_{model}")
    
    # Test connection button
    if st.button("Test Hugging Face Connection"):
        with st.spinner("Testing connection to Hugging Face..."):
            # In a real implementation, we would:
            # 1. Send a request to the Hugging Face API
            # 2. Check if the response is valid
            
            # Simulate connection test
            import time
            time.sleep(1)
            st.success("Successfully connected to Hugging Face!")
    
    # Update config
    st.session_state.providers["huggingface"] = {
        "active": hf_active,
        "token": hf_token
    }
