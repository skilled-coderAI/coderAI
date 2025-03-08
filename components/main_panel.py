import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from components.helpmate_bridge import init_helpmate_bridge

def render_main_panel():
    """Render the main panel of the CoderAI application"""
    
    # Initialize Helpmate-AI bridge if not already initialized
    if "helpmate_initialized" not in st.session_state:
        st.session_state.helpmate_initialized = False
        
    if not st.session_state.helpmate_initialized:
        try:
            st.session_state.helpmate_thread = init_helpmate_bridge()
            st.session_state.helpmate_initialized = True
        except Exception as e:
            st.error(f"Failed to initialize Helpmate-AI integration: {str(e)}")
    
    # Main panel tabs
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Chat", "Analytics"])
    
    with tab1:
        render_dashboard()
    
    with tab2:
        render_chat_interface()
    
    with tab3:
        render_analytics()
    
    """ with tab4:
        render_settings() """

def render_dashboard():
    """Render the dashboard section"""
    # Create a header with logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        logo_path = os.path.join(os.getcwd(), "Logo.png")
        st.image(logo_path, width=100)
    with col2:
        st.markdown("<h1 class='main-header'>CoderAI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subheader'>Your AI Platform</p>", unsafe_allow_html=True)
    
    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Active Providers", value=sum(1 for p in st.session_state.providers.values() if p.get("active", False)))
    with col2:
        st.metric(label="Documents Processed", value=len(st.session_state.get("documents", [])))
    with col3:
        st.metric(label="AI Queries", value=len(st.session_state.get("chat_history", [])))
    
    # Initialize chatbot state if not already initialized
    if "chatbot_open" not in st.session_state:
        st.session_state.chatbot_open = False
    
    # Create a button that will toggle the chatbot state
    chatbot_col1, chatbot_col2 = st.columns([6, 1])
    with chatbot_col2:
        if st.button("Chat 💬", key="dashboard_chat_button"):
            st.session_state.chatbot_open = not st.session_state.chatbot_open
    
    # Display the chatbot if it's open
    if st.session_state.chatbot_open:
        st.markdown("""
        <div style="position: fixed; bottom: 80px; right: 20px; width: 350px; height: 500px; 
                    background-color: white; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
                    z-index: 9999; overflow: hidden;">
            <div style="width: 100%; height: 30px; background-color: #4B8BF5; display: flex; justify-content: space-between; align-items: center; padding: 0 10px;">
                <span style="color: white; font-weight: bold;">Helpmate AI</span>
                <button style="background: none; border: none; color: white; cursor: pointer; font-size: 16px;" 
                        onclick="window.location.href = window.location.href;">✕</button>
            </div>
            <iframe src="http://localhost:5173" width="100%" height="470px" frameborder="0"></iframe>
        </div>
        """, unsafe_allow_html=True)
    
    # Main dashboard content
    st.subheader("Recent Activity")
    
    # Sample data for recent activity
    activity_data = {
        "Timestamp": ["2025-03-08 19:45", "2025-03-08 18:30", "2025-03-08 17:15", "2025-03-08 16:00"],
        "Activity": ["Code Review", "AI Query", "Document Processing", "GitHub Integration"],
        "Details": ["Reviewed login.py", "Generated API documentation", "Processed requirements.txt", "Synced with repository"]
    }
    
    activity_df = pd.DataFrame(activity_data)
    st.dataframe(activity_df, use_container_width=True)

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
    st.subheader("Chat Interface")
    
    # Initialize chatbot state if not already initialized
    if "chatbot_open" not in st.session_state:
        st.session_state.chatbot_open = False
    
    # Add a button to open the chatbot
    if st.button("Open Helpmate AI Assistant", key="chat_tab_button"):
        st.session_state.chatbot_open = not st.session_state.chatbot_open
    
    # Display the chatbot if it's open
    if st.session_state.chatbot_open:
        st.markdown("""
        <div style="position: fixed; bottom: 80px; right: 20px; width: 350px; height: 500px; 
                    background-color: white; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
                    z-index: 9999; overflow: hidden;">
            <div style="width: 100%; height: 30px; background-color: #4B8BF5; display: flex; justify-content: space-between; align-items: center; padding: 0 10px;">
                <span style="color: white; font-weight: bold;">Helpmate AI</span>
                <button style="background: none; border: none; color: white; cursor: pointer; font-size: 16px;" 
                        onclick="window.location.href = window.location.href;">✕</button>
            </div>
            <iframe src="http://localhost:5173" width="100%" height="470px" frameborder="0"></iframe>
        </div>
        """, unsafe_allow_html=True)
    
    # Native chat interface
    st.subheader("Native Chat Interface")
    
    # Message input
    with st.form("chat_form"):
        user_input = st.text_area("Your message:", height=100)
        
        col1, col2 = st.columns([4, 1])
        with col2:
            submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input:
            # Add user message to chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate AI response
            try:
                model_service = st.session_state.model_service
                
                # Find active provider
                active_provider = None
                active_model = None
                
                if st.session_state.providers.get("ollama", {}).get("active", False):
                    active_provider = "ollama"
                    active_model = "llama2"
                elif st.session_state.providers.get("openai", {}).get("active", False):
                    active_provider = "openai"
                    active_model = "gpt-3.5-turbo"
                elif st.session_state.providers.get("anthropic", {}).get("active", False):
                    active_provider = "anthropic"
                    active_model = "claude-3-haiku"
                
                if active_provider:
                    with st.spinner("Generating response..."):
                        response = model_service.query_model(
                            prompt=user_input,
                            provider=active_provider,
                            model=active_model
                        )
                        
                        ai_response = response.get("text", "Sorry, I couldn't generate a response.")
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                else:
                    st.error("No active AI providers found. Please configure a provider in the settings.")
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
    
    # Display chat history
    if "chat_history" in st.session_state and st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="background-color: #e6f7ff; padding: 10px; border-radius: 10px; margin-bottom: 10px; text-align: right;">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    <strong>AI:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)

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

def render_settings():
    """Render the settings section"""
    st.subheader("Settings")
    # Add settings UI here
