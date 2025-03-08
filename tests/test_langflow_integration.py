import pytest
import streamlit as st
from components.langflow_integration import LangflowIntegration
from langflow.schema.message import Message

@pytest.fixture
def langflow_integration():
    return LangflowIntegration()

@pytest.mark.asyncio
async def test_chat_interface(langflow_integration, monkeypatch):
    # Mock streamlit session state
    session_state = {}
    monkeypatch.setattr(st, 'session_state', session_state)
    
    # Mock text_area and button
    def mock_text_area(*args, **kwargs):
        return "Test message"
    monkeypatch.setattr(st, 'text_area', mock_text_area)
    
    def mock_button(*args, **kwargs):
        return True
    monkeypatch.setattr(st, 'button', mock_button)
    
    # Test chat interface setup
    await langflow_integration.setup_chat_interface()
    
    # Verify chat history was created
    assert 'langflow_chat' in st.session_state
    assert len(st.session_state['langflow_chat']) == 2  # User message and response
    
    # Verify message format
    assert st.session_state['langflow_chat'][0]['role'] == 'user'
    assert st.session_state['langflow_chat'][0]['content'] == 'Test message'
    assert st.session_state['langflow_chat'][1]['role'] == 'assistant'

def test_vector_store_setup(langflow_integration):
    # Test with valid inputs
    name = "Test Store"
    description = "Test vector store description"
    mock_vector_store = object()  # Mock vector store instance
    
    vector_store_info = langflow_integration.setup_vector_store(
        name=name,
        description=description,
        vector_store=mock_vector_store
    )
    
    assert vector_store_info is not None
    assert vector_store_info.name == name
    assert vector_store_info.description == description
    assert vector_store_info.vectorstore == mock_vector_store

def test_vector_store_setup_validation(langflow_integration):
    # Test with invalid inputs
    with pytest.raises(ValueError, match="Vector store name and description are required"):
        langflow_integration.setup_vector_store(
            name="",
            description="",
            vector_store=object()
        )
    
    with pytest.raises(ValueError, match="Vector store instance is required"):
        langflow_integration.setup_vector_store(
            name="Test",
            description="Test",
            vector_store=None
        )

def test_render_chat_history(langflow_integration, monkeypatch):
    # Mock streamlit session state
    session_state = {
        'langflow_chat': [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
    }
    monkeypatch.setattr(st, 'session_state', session_state)
    
    # Mock container and text_area
    def mock_container():
        class Container:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return Container()
    monkeypatch.setattr(st, 'container', mock_container)
    
    text_areas = []
    def mock_text_area(*args, **kwargs):
        text_areas.append((args, kwargs))
        return ""
    monkeypatch.setattr(st, 'text_area', mock_text_area)
    
    # Test rendering chat history
    langflow_integration.render_chat_history()
    
    # Verify text areas were created for each message
    assert len(text_areas) == 2
    assert text_areas[0][1]['value'] == "Hello"  # User message
    assert text_areas[1][1]['value'] == "Hi there!"  # Assistant message