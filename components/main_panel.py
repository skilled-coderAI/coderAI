import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

def render_main_panel():
    """Render the main panel of the application"""
    # Create a header with logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        logo_path = os.path.join(os.getcwd(), "Logo.png")
        st.image(logo_path, width=100)
    with col2:
        st.markdown("<h1 class='main-header'>CoderAI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subheader'>Your AI Integration Platform</p>", unsafe_allow_html=True)
    
    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Active Providers", value=sum(1 for p in st.session_state.providers.values() if p["active"]))
    with col2:
        st.metric(label="Documents Processed", value=len(st.session_state.get("documents", [])))
    with col3:
        st.metric(label="AI Queries", value=len(st.session_state.get("chat_history", [])))
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["Document Processing", "Chat Interface", "Analytics"])
    
    with tab1:
        render_document_processing()
    
    with tab2:
        render_chat_interface()
    
    with tab3:
        render_analytics()

def render_document_processing():
    """Render the document processing section"""
    st.subheader("Document Processing")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a document for processing", 
        type=st.session_state.config.allowed_extensions
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Embedding model selection
        embedding_models = st.session_state.config.provider_configs["huggingface"]["available_embedding_models"]
        selected_embedding_model = st.selectbox(
            "Select Embedding Model",
            embedding_models,
            index=embedding_models.index(st.session_state.config.default_embedding_model)
        )
    
    with col2:
        # Processing options
        st.checkbox("Extract metadata", value=True)
        st.checkbox("Generate summary", value=True)
        st.checkbox("Store in vector database", value=True)
    
    # Process button
    if st.button("Process Document", disabled=uploaded_file is None):
        if uploaded_file is not None:
            with st.spinner("Processing document..."):
                # Simulate processing
                st.success(f"Document '{uploaded_file.name}' processed successfully!")
                
                # In a real implementation, we would:
                # 1. Read the document
                # 2. Generate embeddings using the selected model
                # 3. Store in vector database
                # 4. Extract metadata and generate summary
                
                # Add to session state
                if "documents" not in st.session_state:
                    st.session_state.documents = []
                
                st.session_state.documents.append({
                    "name": uploaded_file.name,
                    "size": uploaded_file.size,
                    "type": uploaded_file.type,
                    "embedding_model": selected_embedding_model,
                    "processed_at": datetime.now().isoformat()
                })
    
    # Display processed documents
    if st.session_state.get("documents"):
        st.subheader("Processed Documents")
        
        for i, doc in enumerate(st.session_state.documents):
            with st.expander(f"{i+1}. {doc['name']}"):
                st.write(f"Size: {doc['size']} bytes")
                st.write(f"Type: {doc['type']}")
                st.write(f"Embedding Model: {doc['embedding_model']}")
                st.write(f"Processed at: {doc['processed_at']}")
                
                # Actions
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"Search Similar Documents #{i}", key=f"search_{i}")
                with col2:
                    st.button(f"Delete Document #{i}", key=f"delete_{i}")

def render_chat_interface():
    """Render the chat interface section"""
    st.subheader("Chat with AI")
    
    # Model selection
    col1, col2 = st.columns(2)
    
    with col1:
        # Provider selection
        active_providers = [p for p, c in st.session_state.providers.items() if c["active"]]
        if not active_providers:
            st.warning("No active providers. Please configure a provider in the settings.")
            return
            
        selected_provider = st.selectbox("Select Provider", active_providers)
    
    with col2:
        # Model selection based on provider
        if selected_provider == "ollama":
            models = st.session_state.config.provider_configs["ollama"]["available_models"]
            default_model = st.session_state.config.default_ollama_model
        elif selected_provider == "openai":
            models = st.session_state.config.provider_configs["openai"]["available_models"]
            default_model = models[0]
        elif selected_provider == "anthropic":
            models = st.session_state.config.provider_configs["anthropic"]["available_models"]
            default_model = models[0]
        else:
            models = ["No models available"]
            default_model = models[0]
            
        selected_model = st.selectbox(
            "Select Model",
            models,
            index=models.index(default_model) if default_model in models else 0
        )
    
    # Store current model and provider in session state
    st.session_state.current_model = selected_model
    st.session_state.current_provider = selected_provider
    
    # Chat history
    st.subheader("Chat History")
    
    for message in st.session_state.get("chat_history", []):
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask something...")
    
    if user_input:
        # Add user message to chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # In a real implementation, we would:
                # 1. Send the query to the selected model via the appropriate provider
                # 2. Get the response and display it
                
                # Simulate AI response
                ai_response = f"This is a simulated response from {selected_model} via {selected_provider}. In a real implementation, this would be generated by the AI model."
                st.write(ai_response)
        
        # Add AI response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_response
        })

def render_analytics():
    """Render the analytics section"""
    st.subheader("Analytics")
    
    # Create sample data for demonstration
    if not st.session_state.get("analytics_data"):
        # Sample data for demonstration
        st.session_state.analytics_data = {
            "model_usage": pd.DataFrame({
                "Model": ["llama2", "mistral", "gpt-3.5-turbo", "claude-3-haiku"],
                "Queries": [45, 30, 20, 15]
            }),
            "daily_usage": pd.DataFrame({
                "Date": pd.date_range(start="2025-03-01", periods=7),
                "Queries": [12, 15, 8, 20, 25, 18, 22]
            }),
            "document_types": pd.DataFrame({
                "Type": ["PDF", "TXT", "DOCX", "MD"],
                "Count": [15, 8, 12, 5]
            })
        }
    
    # Display analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Model usage chart
        st.subheader("Model Usage")
        fig1 = px.bar(
            st.session_state.analytics_data["model_usage"],
            x="Model",
            y="Queries",
            color="Model",
            title="Queries by Model"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Document types chart
        st.subheader("Document Types")
        fig3 = px.pie(
            st.session_state.analytics_data["document_types"],
            values="Count",
            names="Type",
            title="Document Types Processed"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Daily usage chart
        st.subheader("Daily Usage")
        fig2 = px.line(
            st.session_state.analytics_data["daily_usage"],
            x="Date",
            y="Queries",
            title="Daily Queries"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Usage metrics
        st.subheader("Usage Metrics")
        metrics_data = {
            "Total Queries": 110,
            "Avg. Response Time": "1.2s",
            "Success Rate": "98.5%",
            "Token Usage": "125,450"
        }
        
        for metric, value in metrics_data.items():
            st.metric(label=metric, value=value)
