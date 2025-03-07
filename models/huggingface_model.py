from typing import Dict, List, Any, Optional, Union
from .base_model import BaseModel

class HuggingFaceModel(BaseModel):
    """Integration with Hugging Face models"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the Hugging Face model
        
        Args:
            token: Hugging Face API token (optional)
        """
        self.token = token
        self.embedding_model = None
        self.embedding_model_name = None
    
    def query(self, 
             prompt: str, 
             model: str = "google/flan-t5-base",
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Query a Hugging Face model
        
        Args:
            prompt: The user prompt
            model: The model name
            system_prompt: Optional system prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response from the model
        """
        try:
            # Import here to avoid loading dependencies unless needed
            from transformers import pipeline
            
            # Combine system prompt and user prompt if provided
            input_text = prompt
            if system_prompt:
                input_text = f"{system_prompt}\n\n{prompt}"
            
            # Create pipeline
            generator = pipeline(
                "text-generation", 
                model=model,
                token=self.token if self.token else None
            )
            
            # Generate text
            result = generator(
                input_text,
                max_length=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0
            )
            
            # Extract generated text
            generated_text = result[0]["generated_text"]
            
            # Remove the input prompt from the generated text
            if generated_text.startswith(input_text):
                generated_text = generated_text[len(input_text):].strip()
            
            return {
                "text": generated_text,
                "model": model,
                "provider": self.provider_name
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "model": model,
                "provider": self.provider_name
            }
    
    def get_embedding(self, text: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> Union[List[float], None]:
        """
        Generate embedding for a text
        
        Args:
            text: The text to generate embedding for
            model_name: Name of the embedding model
            
        Returns:
            Embedding vector as a list of floats, or None if an error occurs
        """
        try:
            # Import here to avoid loading dependencies unless needed
            from sentence_transformers import SentenceTransformer
            
            # Load model if not loaded or if model name changed
            if self.embedding_model is None or self.embedding_model_name != model_name:
                self.embedding_model = SentenceTransformer(model_name)
                self.embedding_model_name = model_name
            
            # Generate embedding
            embedding = self.embedding_model.encode(text)
            
            # Convert to list and return
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def get_embeddings(self, texts: List[str], model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> Union[List[List[float]], None]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to generate embeddings for
            model_name: Name of the embedding model
            
        Returns:
            List of embedding vectors, or None if an error occurs
        """
        try:
            # Import here to avoid loading dependencies unless needed
            from sentence_transformers import SentenceTransformer
            
            # Load model if not loaded or if model name changed
            if self.embedding_model is None or self.embedding_model_name != model_name:
                self.embedding_model = SentenceTransformer(model_name)
                self.embedding_model_name = model_name
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(texts)
            
            # Convert to list and return
            return embeddings.tolist()
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None
    
    def get_available_models(self) -> List[str]:
        """
        Get a list of recommended models
        
        Returns:
            List of model names
        """
        # Return a list of recommended models
        # In a real implementation, we might query the Hugging Face API
        return [
            "google/flan-t5-base",
            "google/flan-t5-large",
            "facebook/bart-large-cnn",
            "gpt2",
            "EleutherAI/gpt-neo-1.3B"
        ]
    
    def get_available_embedding_models(self) -> List[str]:
        """
        Get a list of recommended embedding models
        
        Returns:
            List of model names
        """
        # Return a list of recommended embedding models
        return [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2",
            "sentence-transformers/multi-qa-mpnet-base-dot-v1",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        ]
    
    @property
    def provider_name(self) -> str:
        """
        Get the provider name
        
        Returns:
            Provider name
        """
        return "huggingface"
