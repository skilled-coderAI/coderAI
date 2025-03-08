"""
CoderAI Framework RAG Tools
This module provides Retrieval-Augmented Generation (RAG) tools for the CoderAI framework.
"""

import os
import json
import uuid
import pickle
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import numpy as np
from ..registry import registry
from ..constants import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class Document:
    """
    Document class for RAG.
    """
    def __init__(self, id: str, content: str, metadata: Dict[str, Any] = None, embedding: List[float] = None):
        """
        Initialize a document.
        
        Args:
            id: Document ID
            content: Document content
            metadata: Document metadata
            embedding: Document embedding
        """
        self.id = id
        self.content = content
        self.metadata = metadata or {}
        self.embedding = embedding
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert document to dictionary.
        
        Returns:
            Dictionary representation of the document
        """
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """
        Create document from dictionary.
        
        Args:
            data: Dictionary to create document from
            
        Returns:
            Created document
        """
        return cls(
            id=data["id"],
            content=data["content"],
            metadata=data.get("metadata", {}),
        )

class RAGStore:
    """
    Store for RAG documents.
    """
    def __init__(self, embedding_model: str = None, storage_path: str = None):
        """
        Initialize the RAG store.
        
        Args:
            embedding_model: Model to use for embeddings
            storage_path: Path to store documents
        """
        self.documents = {}
        self.embedding_model = embedding_model
        self.storage_path = storage_path
        
        # Initialize embedding model
        self.model = None
        self.client = None
        
        if embedding_model:
            if embedding_model.startswith("openai:"):
                if OPENAI_AVAILABLE:
                    self.client = OpenAI()
                    self.embedding_model_name = embedding_model[7:]
                else:
                    print("OpenAI package not available, embeddings will not be generated")
            elif SENTENCE_TRANSFORMERS_AVAILABLE:
                try:
                    self.model = SentenceTransformer(embedding_model)
                except Exception as e:
                    print(f"Error loading embedding model: {e}")
            else:
                print("Sentence Transformers package not available, embeddings will not be generated")
                
        # Create storage directory if it doesn't exist
        if storage_path:
            os.makedirs(storage_path, exist_ok=True)
            
            # Load existing documents
            self.load_documents()
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None) -> Document:
        """
        Add a document.
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            Added document
        """
        # Generate ID
        doc_id = str(uuid.uuid4())
        
        # Create document
        document = Document(
            id=doc_id,
            content=content,
            metadata=metadata or {},
        )
        
        # Generate embedding
        document.embedding = self.generate_embedding(content)
        
        # Add document
        self.documents[doc_id] = document
        
        # Save document if storage path is set
        if self.storage_path:
            self.save_document(document)
            
        return document
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """
        Get a document.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document or None if not found
        """
        return self.documents.get(doc_id)
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document.
        
        Args:
            doc_id: Document ID
            
        Returns:
            True if document was deleted, False otherwise
        """
        if doc_id in self.documents:
            # Remove document
            del self.documents[doc_id]
            
            # Delete files if storage path is set
            if self.storage_path:
                doc_path = os.path.join(self.storage_path, "documents", f"{doc_id}.json")
                if os.path.exists(doc_path):
                    os.remove(doc_path)
                    
                embedding_path = os.path.join(self.storage_path, "embeddings", f"{doc_id}.pickle")
                if os.path.exists(embedding_path):
                    os.remove(embedding_path)
                    
            return True
        return False
    
    def search_documents(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search documents.
        
        Args:
            query: Query to search for
            k: Number of results to return
            
        Returns:
            List of search results
        """
        if not self.documents:
            return []
            
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        if query_embedding is None:
            # Fall back to keyword search if embedding is not available
            return self.keyword_search(query, k)
            
        # Calculate similarity scores
        results = []
        for doc_id, document in self.documents.items():
            if document.embedding is not None:
                score = self.calculate_similarity(query_embedding, document.embedding)
                results.append({
                    "id": doc_id,
                    "content": document.content,
                    "metadata": document.metadata,
                    "score": score,
                })
                
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top k results
        return results[:k]
    
    def keyword_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search documents by keywords.
        
        Args:
            query: Query to search for
            k: Number of results to return
            
        Returns:
            List of search results
        """
        if not self.documents:
            return []
            
        # Tokenize query
        query_tokens = set(query.lower().split())
        
        # Calculate scores
        results = []
        for doc_id, document in self.documents.items():
            doc_tokens = set(document.content.lower().split())
            
            # Calculate Jaccard similarity
            intersection = len(query_tokens.intersection(doc_tokens))
            union = len(query_tokens.union(doc_tokens))
            
            if union > 0:
                score = intersection / union
            else:
                score = 0
                
            results.append({
                "id": doc_id,
                "content": document.content,
                "metadata": document.metadata,
                "score": score,
            })
            
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top k results
        return results[:k]
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate an embedding for text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            Embedding or None if not available
        """
        if not text:
            return None
            
        if self.client and hasattr(self, "embedding_model_name"):
            try:
                response = self.client.embeddings.create(
                    model=self.embedding_model_name,
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"Error generating OpenAI embedding: {e}")
                return None
        elif self.model:
            try:
                return self.model.encode(text).tolist()
            except Exception as e:
                print(f"Error generating sentence transformer embedding: {e}")
                return None
        else:
            return None
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between embeddings.
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Cosine similarity
        """
        if embedding1 is None or embedding2 is None:
            return 0
            
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
            
        return dot_product / (norm1 * norm2)
    
    def save_document(self, document: Document):
        """
        Save a document to disk.
        
        Args:
            document: Document to save
        """
        if not self.storage_path:
            return
            
        # Create documents directory if it doesn't exist
        documents_dir = os.path.join(self.storage_path, "documents")
        os.makedirs(documents_dir, exist_ok=True)
        
        # Save document
        doc_path = os.path.join(documents_dir, f"{document.id}.json")
        with open(doc_path, "w") as f:
            json.dump(document.to_dict(), f, indent=2)
            
        # Save embedding if available
        if document.embedding:
            # Create embeddings directory if it doesn't exist
            embeddings_dir = os.path.join(self.storage_path, "embeddings")
            os.makedirs(embeddings_dir, exist_ok=True)
            
            # Save embedding
            embedding_path = os.path.join(embeddings_dir, f"{document.id}.pickle")
            with open(embedding_path, "wb") as f:
                pickle.dump(document.embedding, f)
    
    def load_documents(self):
        """
        Load documents from disk.
        """
        if not self.storage_path:
            return
            
        # Load documents
        documents_dir = os.path.join(self.storage_path, "documents")
        if os.path.exists(documents_dir):
            for filename in os.listdir(documents_dir):
                if filename.endswith(".json"):
                    doc_path = os.path.join(documents_dir, filename)
                    
                    try:
                        with open(doc_path, "r") as f:
                            doc_data = json.load(f)
                            
                        # Create document
                        document = Document.from_dict(doc_data)
                        
                        # Load embedding if available
                        embedding_path = os.path.join(self.storage_path, "embeddings", f"{document.id}.pickle")
                        if os.path.exists(embedding_path):
                            with open(embedding_path, "rb") as f:
                                document.embedding = pickle.load(f)
                                
                        # Add document
                        self.documents[document.id] = document
                    except Exception as e:
                        print(f"Error loading document from {doc_path}: {e}")
    
    def chunk_text(self, text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
        """
        Chunk text into smaller pieces.
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of chunks
        """
        if LANGCHAIN_AVAILABLE:
            # Use LangChain text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            return text_splitter.split_text(text)
        else:
            # Simple chunking
            chunks = []
            start = 0
            
            while start < len(text):
                # Get chunk
                end = start + chunk_size
                chunk = text[start:end]
                
                # Add chunk
                chunks.append(chunk)
                
                # Move to next chunk
                start = end - chunk_overlap
                
            return chunks

# Create global RAG store
rag_store = RAGStore()

@registry.register(type="tool")
def add_document(content: str, metadata: Dict[str, Any] = None, chunk: bool = False, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Add a document to the RAG store.
    
    Args:
        content: Document content
        metadata: Document metadata
        chunk: Whether to chunk the document
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        Dictionary containing the document ID
    """
    try:
        if chunk:
            # Chunk document
            chunks = rag_store.chunk_text(content, chunk_size, chunk_overlap)
            
            # Add chunks
            doc_ids = []
            for i, chunk_content in enumerate(chunks):
                # Create metadata for chunk
                chunk_metadata = metadata.copy() if metadata else {}
                chunk_metadata["chunk_index"] = i
                chunk_metadata["chunk_count"] = len(chunks)
                
                # Add chunk
                document = rag_store.add_document(chunk_content, chunk_metadata)
                doc_ids.append(document.id)
                
            return {
                "success": True,
                "doc_ids": doc_ids,
                "chunk_count": len(chunks),
            }
        else:
            # Add document
            document = rag_store.add_document(content, metadata)
            
            return {
                "success": True,
                "doc_id": document.id,
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def search_documents(query: str, k: int = 5, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Search documents in the RAG store.
    
    Args:
        query: Query to search for
        k: Number of results to return
        
    Returns:
        Dictionary containing search results
    """
    try:
        # Search documents
        results = rag_store.search_documents(query, k)
        
        return {
            "success": True,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@registry.register(type="tool")
def delete_document(doc_id: str, context_variables: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Delete a document from the RAG store.
    
    Args:
        doc_id: Document ID
        
    Returns:
        Dictionary indicating success or failure
    """
    try:
        # Delete document
        success = rag_store.delete_document(doc_id)
        
        if success:
            return {
                "success": True,
                "doc_id": doc_id,
            }
        else:
            return {
                "success": False,
                "error": f"Document '{doc_id}' not found",
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
