"""
CoderAI Framework Memory Core
This module provides the core functionality for the memory management system.
"""

import os
import json
import pickle
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
import uuid
import numpy as np
from pathlib import Path
from .types import Memory, MemoryGroup, MemorySearchResult
from ..logger import LoggerManager
from ..constants import DEFAULT_MEMORY_SIZE, DEFAULT_MEMORY_K

logger = LoggerManager.get_logger()

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

class MemoryManager:
    """
    Manager for memories.
    """
    def __init__(self, embedding_model: str = None, storage_path: str = None):
        """
        Initialize the memory manager.
        
        Args:
            embedding_model: Model to use for embeddings
            storage_path: Path to store memories
        """
        self.memories = {}
        self.memory_groups = {}
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
                    if logger:
                        logger.warning("OpenAI package not available, embeddings will not be generated")
            elif SENTENCE_TRANSFORMERS_AVAILABLE:
                try:
                    self.model = SentenceTransformer(embedding_model)
                except Exception as e:
                    if logger:
                        logger.error(f"Error loading embedding model: {e}")
            else:
                if logger:
                    logger.warning("Sentence Transformers package not available, embeddings will not be generated")
                    
        # Create storage directory if it doesn't exist
        if storage_path:
            os.makedirs(storage_path, exist_ok=True)
            
            # Load existing memories
            self.load_memories()
    
    def add_memory(self, memory: Memory):
        """
        Add a memory.
        
        Args:
            memory: Memory to add
            
        Returns:
            Added memory
        """
        # Generate embedding if model is available
        if not memory.embedding:
            memory.embedding = self.generate_embedding(memory.content)
            
        # Add memory
        self.memories[memory.id] = memory
        
        # Save memory if storage path is set
        if self.storage_path:
            self.save_memory(memory)
            
        return memory
    
    def update_memory(self, memory: Memory):
        """
        Update a memory.
        
        Args:
            memory: Memory to update
            
        Returns:
            Updated memory
        """
        # Update timestamp
        memory.updated_at = datetime.now()
        
        # Generate embedding if content changed
        if memory.id in self.memories:
            old_memory = self.memories[memory.id]
            if old_memory.content != memory.content:
                memory.embedding = self.generate_embedding(memory.content)
        else:
            memory.embedding = self.generate_embedding(memory.content)
            
        # Update memory
        self.memories[memory.id] = memory
        
        # Save memory if storage path is set
        if self.storage_path:
            self.save_memory(memory)
            
        return memory
    
    def delete_memory(self, memory_id: str):
        """
        Delete a memory.
        
        Args:
            memory_id: ID of the memory to delete
        """
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            
            # Remove from memory groups
            for group in self.memory_groups.values():
                group.memories = [m for m in group.memories if m.id != memory_id]
                
            # Remove from memories
            del self.memories[memory_id]
            
            # Delete file if storage path is set
            if self.storage_path:
                memory_path = os.path.join(self.storage_path, f"{memory_id}.json")
                if os.path.exists(memory_path):
                    os.remove(memory_path)
    
    def add_memory_group(self, memory_group: MemoryGroup):
        """
        Add a memory group.
        
        Args:
            memory_group: Memory group to add
            
        Returns:
            Added memory group
        """
        self.memory_groups[memory_group.id] = memory_group
        
        # Save memory group if storage path is set
        if self.storage_path:
            self.save_memory_group(memory_group)
            
        return memory_group
    
    def update_memory_group(self, memory_group: MemoryGroup):
        """
        Update a memory group.
        
        Args:
            memory_group: Memory group to update
            
        Returns:
            Updated memory group
        """
        # Update timestamp
        memory_group.updated_at = datetime.now()
        
        # Update memory group
        self.memory_groups[memory_group.id] = memory_group
        
        # Save memory group if storage path is set
        if self.storage_path:
            self.save_memory_group(memory_group)
            
        return memory_group
    
    def delete_memory_group(self, group_id: str):
        """
        Delete a memory group.
        
        Args:
            group_id: ID of the memory group to delete
        """
        if group_id in self.memory_groups:
            # Remove from memory groups
            del self.memory_groups[group_id]
            
            # Delete file if storage path is set
            if self.storage_path:
                group_path = os.path.join(self.storage_path, "groups", f"{group_id}.json")
                if os.path.exists(group_path):
                    os.remove(group_path)
    
    def add_memory_to_group(self, memory: Memory, group_id: str):
        """
        Add a memory to a group.
        
        Args:
            memory: Memory to add
            group_id: ID of the group to add to
            
        Returns:
            Updated memory group
        """
        if group_id in self.memory_groups:
            group = self.memory_groups[group_id]
            
            # Add memory to group if not already in it
            if memory.id not in [m.id for m in group.memories]:
                group.memories.append(memory)
                group.updated_at = datetime.now()
                
                # Save memory group if storage path is set
                if self.storage_path:
                    self.save_memory_group(group)
                    
            return group
        return None
    
    def remove_memory_from_group(self, memory_id: str, group_id: str):
        """
        Remove a memory from a group.
        
        Args:
            memory_id: ID of the memory to remove
            group_id: ID of the group to remove from
            
        Returns:
            Updated memory group
        """
        if group_id in self.memory_groups:
            group = self.memory_groups[group_id]
            
            # Remove memory from group
            group.memories = [m for m in group.memories if m.id != memory_id]
            group.updated_at = datetime.now()
            
            # Save memory group if storage path is set
            if self.storage_path:
                self.save_memory_group(group)
                
            return group
        return None
    
    def search_memories(self, query: str, k: int = DEFAULT_MEMORY_K) -> List[MemorySearchResult]:
        """
        Search memories.
        
        Args:
            query: Query to search for
            k: Number of results to return
            
        Returns:
            List of memory search results
        """
        if not self.memories:
            return []
            
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        if query_embedding is None:
            # Fall back to keyword search if embedding is not available
            return self.keyword_search(query, k)
            
        # Calculate similarity scores
        results = []
        for memory in self.memories.values():
            if memory.embedding is not None:
                score = self.calculate_similarity(query_embedding, memory.embedding)
                results.append(MemorySearchResult(memory=memory, score=score))
                
        # Sort by score (highest first)
        results.sort(reverse=True)
        
        # Return top k results
        return results[:k]
    
    def keyword_search(self, query: str, k: int = DEFAULT_MEMORY_K) -> List[MemorySearchResult]:
        """
        Search memories by keywords.
        
        Args:
            query: Query to search for
            k: Number of results to return
            
        Returns:
            List of memory search results
        """
        if not self.memories:
            return []
            
        # Tokenize query
        query_tokens = set(query.lower().split())
        
        # Calculate scores
        results = []
        for memory in self.memories.values():
            memory_tokens = set(memory.content.lower().split())
            
            # Calculate Jaccard similarity
            intersection = len(query_tokens.intersection(memory_tokens))
            union = len(query_tokens.union(memory_tokens))
            
            if union > 0:
                score = intersection / union
            else:
                score = 0
                
            results.append(MemorySearchResult(memory=memory, score=score))
            
        # Sort by score (highest first)
        results.sort(reverse=True)
        
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
            
        if self.client and self.embedding_model_name:
            try:
                response = self.client.embeddings.create(
                    model=self.embedding_model_name,
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                if logger:
                    logger.error(f"Error generating OpenAI embedding: {e}")
                return None
        elif self.model:
            try:
                return self.model.encode(text).tolist()
            except Exception as e:
                if logger:
                    logger.error(f"Error generating sentence transformer embedding: {e}")
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
    
    def save_memory(self, memory: Memory):
        """
        Save a memory to disk.
        
        Args:
            memory: Memory to save
        """
        if not self.storage_path:
            return
            
        # Create memories directory if it doesn't exist
        memories_dir = os.path.join(self.storage_path, "memories")
        os.makedirs(memories_dir, exist_ok=True)
        
        # Save memory
        memory_path = os.path.join(memories_dir, f"{memory.id}.json")
        
        # Convert to dict
        memory_dict = {
            "id": memory.id,
            "content": memory.content,
            "metadata": memory.metadata,
            "created_at": memory.created_at.isoformat(),
            "updated_at": memory.updated_at.isoformat(),
        }
        
        # Save embedding separately
        if memory.embedding:
            embedding_path = os.path.join(memories_dir, f"{memory.id}.embedding")
            with open(embedding_path, "wb") as f:
                pickle.dump(memory.embedding, f)
                
        # Save memory
        with open(memory_path, "w") as f:
            json.dump(memory_dict, f, indent=2)
    
    def save_memory_group(self, memory_group: MemoryGroup):
        """
        Save a memory group to disk.
        
        Args:
            memory_group: Memory group to save
        """
        if not self.storage_path:
            return
            
        # Create groups directory if it doesn't exist
        groups_dir = os.path.join(self.storage_path, "groups")
        os.makedirs(groups_dir, exist_ok=True)
        
        # Save memory group
        group_path = os.path.join(groups_dir, f"{memory_group.id}.json")
        
        # Convert to dict
        group_dict = {
            "id": memory_group.id,
            "name": memory_group.name,
            "metadata": memory_group.metadata,
            "created_at": memory_group.created_at.isoformat(),
            "updated_at": memory_group.updated_at.isoformat(),
            "memory_ids": [m.id for m in memory_group.memories],
        }
        
        # Save memory group
        with open(group_path, "w") as f:
            json.dump(group_dict, f, indent=2)
    
    def load_memories(self):
        """
        Load memories from disk.
        """
        if not self.storage_path:
            return
            
        # Load memories
        memories_dir = os.path.join(self.storage_path, "memories")
        if os.path.exists(memories_dir):
            for filename in os.listdir(memories_dir):
                if filename.endswith(".json"):
                    memory_path = os.path.join(memories_dir, filename)
                    
                    try:
                        with open(memory_path, "r") as f:
                            memory_dict = json.load(f)
                            
                        # Create memory
                        memory = Memory(
                            id=memory_dict["id"],
                            content=memory_dict["content"],
                            metadata=memory_dict["metadata"],
                            created_at=datetime.fromisoformat(memory_dict["created_at"]),
                            updated_at=datetime.fromisoformat(memory_dict["updated_at"]),
                        )
                        
                        # Load embedding
                        embedding_path = os.path.join(memories_dir, f"{memory.id}.embedding")
                        if os.path.exists(embedding_path):
                            with open(embedding_path, "rb") as f:
                                memory.embedding = pickle.load(f)
                                
                        # Add memory
                        self.memories[memory.id] = memory
                    except Exception as e:
                        if logger:
                            logger.error(f"Error loading memory from {memory_path}: {e}")
                            
        # Load memory groups
        groups_dir = os.path.join(self.storage_path, "groups")
        if os.path.exists(groups_dir):
            for filename in os.listdir(groups_dir):
                if filename.endswith(".json"):
                    group_path = os.path.join(groups_dir, filename)
                    
                    try:
                        with open(group_path, "r") as f:
                            group_dict = json.load(f)
                            
                        # Get memories
                        memories = []
                        for memory_id in group_dict["memory_ids"]:
                            if memory_id in self.memories:
                                memories.append(self.memories[memory_id])
                                
                        # Create memory group
                        memory_group = MemoryGroup(
                            id=group_dict["id"],
                            name=group_dict["name"],
                            memories=memories,
                            metadata=group_dict["metadata"],
                            created_at=datetime.fromisoformat(group_dict["created_at"]),
                            updated_at=datetime.fromisoformat(group_dict["updated_at"]),
                        )
                        
                        # Add memory group
                        self.memory_groups[memory_group.id] = memory_group
                    except Exception as e:
                        if logger:
                            logger.error(f"Error loading memory group from {group_path}: {e}")

# Create global memory manager
memory_manager = MemoryManager()
