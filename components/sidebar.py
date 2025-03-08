import streamlit as st
import os

def render_sidebar():
    """Render the sidebar navigation and settings"""
    with st.sidebar:
        # Use the local Logo.png file instead of placeholder
        logo_path = os.path.join(os.getcwd(), "Logo.png")
        st.image(logo_path, width=150)
        st.title("CoderAI")
        st.subheader("AI Integration Platform")
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
            
        if st.button("⚙️ Provider Configuration", use_container_width=True):
            st.session_state.current_page = "Provider Configuration"
            st.rerun()
            
        if st.button("🔍 Code Review", use_container_width=True):
            st.session_state.current_page = "Code Review"
            st.rerun()
            
        if st.button("🐙 GitHub Integration", use_container_width=True):
            st.session_state.current_page = "GitHub Integration"
            st.rerun()
            
        if st.button("🤖 Agent Framework", use_container_width=True):
            st.session_state.current_page = "Agent Framework"
            st.rerun()
        
        st.divider()
        
        # Active Providers
        st.subheader("Active Providers")
        providers = st.session_state.providers
        
        for provider, config in providers.items():
            if config["active"]:
                st.success(f"✅ {provider.capitalize()}")
            else:
                st.error(f"❌ {provider.capitalize()}")
        
        st.divider()
        
        # Current Model
        st.subheader("Current Model")
        if "current_model" in st.session_state:
            st.info(f"Model: {st.session_state.current_model}")
            st.info(f"Provider: {st.session_state.current_provider}")
        else:
            st.info("No model selected")
        
        st.divider()
        
        # App Info
        st.caption("CoderAI v1.0.0")
        st.caption(" 2025 CoderAI Team")
