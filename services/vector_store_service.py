import os
import json
import numpy as np
from typing import List, Dict, Any, Optional, Union
import faiss
import pickle

class VectorStoreService:
    """Service for managing vector storage and retrieval"""
    
    def __init__(self, vector_db_path: str = "./data/vector_db"):
        """
        Initialize the vector store service
        
        Args:
            vector_db_path: Path to store vector database files
        """
        self.vector_db_path = vector_db_path
        self.index = None
        self.metadata = []
        self.dimension = None
        
        # Create directory if it doesn't exist
        os.makedirs(vector_db_path, exist_ok=True)
    
    def create_index(self, dimension: int = 384):
        """
        Create a new FAISS index
        
        Args:
            dimension: Dimension of the embedding vectors
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
    
    def add_vectors(self, vectors: List[List[float]], metadata_list: List[Dict[str, Any]]) -> bool:
        """
        Add vectors to the index
        
        Args:
            vectors: List of embedding vectors
            metadata_list: List of metadata dictionaries for each vector
            
        Returns:
            True if successful, False otherwise
        """
        if self.index is None:
            if self.dimension is None and vectors:
                # Auto-detect dimension from first vector
                self.dimension = len(vectors[0])
                self.create_index(self.dimension)
            else:
                return False
        
        try:
            # Convert to numpy array
            vectors_np = np.array(vectors).astype('float32')
            
            # Add vectors to index
            self.index.add(vectors_np)
            
            # Add metadata
            self.metadata.extend(metadata_list)
            
            return True
        except Exception as e:
            print(f"Error adding vectors: {e}")
            return False
    
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries with metadata and similarity score
        """
        if self.index is None or not self.metadata:
            return []
        
        try:
            # Convert to numpy array
            query_np = np.array([query_vector]).astype('float32')
            
            # Search index
            distances, indices = self.index.search(query_np, top_k)
            
            # Prepare results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata) and idx != -1:
                    result = {
                        "score": float(1 / (1 + distances[0][i])),  # Convert distance to similarity score
                        **self.metadata[idx]
                    }
                    results.append(result)
            
            return results
        except Exception as e:
            print(f"Error searching vectors: {e}")
            return []
    
    def save(self, name: str = "default") -> bool:
        """
        Save the index and metadata to disk
        
        Args:
            name: Name of the index
            
        Returns:
            True if successful, False otherwise
        """
        if self.index is None:
            return False
        
        try:
            # Create index directory
            index_dir = os.path.join(self.vector_db_path, name)
            os.makedirs(index_dir, exist_ok=True)
            
            # Save index
            index_path = os.path.join(index_dir, "index.faiss")
            faiss.write_index(self.index, index_path)
            
            # Save metadata
            metadata_path = os.path.join(index_dir, "metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(self.metadata, f)
            
            # Save dimension
            config_path = os.path.join(index_dir, "config.pkl")
            with open(config_path, 'wb') as f:
                pickle.dump({"dimension": self.dimension}, f)
            
            return True
        except Exception as e:
            print(f"Error saving index: {e}")
            return False
    
    def load(self, name: str = "default") -> bool:
        """
        Load the index and metadata from disk
        
        Args:
            name: Name of the index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if index directory exists
            index_dir = os.path.join(self.vector_db_path, name)
            if not os.path.exists(index_dir):
                return False
            
            # Load index
            index_path = os.path.join(index_dir, "index.faiss")
            self.index = faiss.read_index(index_path)
            
            # Load metadata
            metadata_path = os.path.join(index_dir, "metadata.json")
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            
            # Load dimension
            config_path = os.path.join(index_dir, "config.pkl")
            with open(config_path, 'rb') as f:
                config = pickle.load(f)
                self.dimension = config.get("dimension")
            
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def list_indexes(self) -> List[str]:
        """
        List available indexes
        
        Returns:
            List of index names
        """
        try:
            # Get subdirectories in vector_db_path
            return [d for d in os.listdir(self.vector_db_path) 
                   if os.path.isdir(os.path.join(self.vector_db_path, d))]
        except Exception as e:
            print(f"Error listing indexes: {e}")
            return []
    
    def delete_index(self, name: str) -> bool:
        """
        Delete an index
        
        Args:
            name: Name of the index
            
        Returns:
            True if successful, False otherwise
        """
        import shutil
        
        try:
            # Check if index directory exists
            index_dir = os.path.join(self.vector_db_path, name)
            if not os.path.exists(index_dir):
                return False
            
            # Delete directory
            shutil.rmtree(index_dir)
            
            # Reset if current index was deleted
            if self.index is not None:
                self.index = None
                self.metadata = []
                self.dimension = None
            
            return True
        except Exception as e:
            print(f"Error deleting index: {e}")
            return False
