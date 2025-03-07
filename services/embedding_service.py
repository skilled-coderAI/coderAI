import os
from typing import List, Dict, Any, Union
import numpy as np

class EmbeddingService:
    """Service for generating embeddings from text using various models"""
    
    def __init__(self):
        """Initialize the embedding service"""
        self.model = None
        self.model_name = None
    
    def load_model(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Load a sentence transformer model for generating embeddings
        
        Args:
            model_name: Name of the model to load
        """
        try:
            # Import here to avoid loading dependencies unless needed
            from sentence_transformers import SentenceTransformer
            
            # Load the model
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
            
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def generate_embedding(self, text: str) -> Union[List[float], None]:
        """
        Generate embedding for a single text
        
        Args:
            text: The text to generate embedding for
            
        Returns:
            Embedding vector as a list of floats, or None if an error occurs
        """
        if self.model is None:
            if not self.load_model():
                return None
        
        try:
            # Generate embedding
            embedding = self.model.encode(text)
            
            # Convert to list and return
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def generate_embeddings(self, texts: List[str]) -> Union[List[List[float]], None]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of embedding vectors, or None if an error occurs
        """
        if self.model is None:
            if not self.load_model():
                return None
        
        try:
            # Generate embeddings
            embeddings = self.model.encode(texts)
            
            # Convert to list and return
            return embeddings.tolist()
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Compute cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def find_most_similar(self, 
                         query_embedding: List[float], 
                         embeddings: List[List[float]], 
                         top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find the most similar embeddings to a query embedding
        
        Args:
            query_embedding: The query embedding vector
            embeddings: List of embedding vectors to compare against
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries with index and similarity score
        """
        similarities = []
        
        # Compute similarities
        for i, embedding in enumerate(embeddings):
            similarity = self.compute_similarity(query_embedding, embedding)
            similarities.append({"index": i, "score": similarity})
        
        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top-k results
        return similarities[:top_k]
