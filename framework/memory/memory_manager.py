"""
CoderAI Memory Manager Module
This module provides memory management capabilities for CoderAI agents,
allowing them to store and retrieve information across conversations.
"""

import os
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

from .types import Memory, MemoryType, MemoryQuery

class MemoryManager:
    """
    Manages agent memories, providing storage and retrieval capabilities.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the memory manager.
        
        Args:
            storage_path: Path to store memories. If None, uses a default path.
        """
        self.logger = logging.getLogger(__name__)
        
        if storage_path is None:
            # Default to a directory in the user's home directory
            home_dir = Path.home()
            self.storage_path = home_dir / ".coderAI" / "memories"
        else:
            self.storage_path = Path(storage_path)
        
        # Create the storage directory if it doesn't exist
        os.makedirs(self.storage_path, exist_ok=True)
        
        self.memories: Dict[str, Memory] = {}
        self.load_memories()
        
        self.logger.info(f"Memory manager initialized with storage path: {self.storage_path}")
    
    def load_memories(self) -> None:
        """
        Load memories from storage.
        """
        memory_files = list(self.storage_path.glob("*.json"))
        self.logger.info(f"Loading {len(memory_files)} memories from storage")
        
        for memory_file in memory_files:
            try:
                with open(memory_file, "r") as f:
                    memory_data = json.load(f)
                
                memory = Memory(
                    id=memory_data["id"],
                    content=memory_data["content"],
                    type=MemoryType(memory_data["type"]),
                    created_at=datetime.datetime.fromisoformat(memory_data["created_at"]),
                    last_accessed=datetime.datetime.fromisoformat(memory_data["last_accessed"]) if "last_accessed" in memory_data else None,
                    metadata=memory_data.get("metadata", {})
                )
                
                self.memories[memory.id] = memory
            except Exception as e:
                self.logger.error(f"Error loading memory from {memory_file}: {e}")
    
    def save_memory(self, memory: Memory) -> None:
        """
        Save a memory to storage.
        
        Args:
            memory: The memory to save
        """
        memory_path = self.storage_path / f"{memory.id}.json"
        
        memory_data = {
            "id": memory.id,
            "content": memory.content,
            "type": memory.type.value,
            "created_at": memory.created_at.isoformat(),
            "last_accessed": memory.last_accessed.isoformat() if memory.last_accessed else None,
            "metadata": memory.metadata
        }
        
        with open(memory_path, "w") as f:
            json.dump(memory_data, f, indent=2)
        
        self.logger.debug(f"Saved memory {memory.id} to {memory_path}")
    
    def create_memory(
        self,
        content: str,
        memory_type: MemoryType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """
        Create a new memory.
        
        Args:
            content: The content of the memory
            memory_type: The type of memory
            metadata: Additional metadata for the memory
            
        Returns:
            The created memory
        """
        from uuid import uuid4
        
        memory_id = str(uuid4())
        now = datetime.datetime.now()
        
        memory = Memory(
            id=memory_id,
            content=content,
            type=memory_type,
            created_at=now,
            last_accessed=None,
            metadata=metadata or {}
        )
        
        self.memories[memory_id] = memory
        self.save_memory(memory)
        
        self.logger.info(f"Created new memory with ID {memory_id}")
        
        return memory
    
    def get_memory(self, memory_id: str) -> Optional[Memory]:
        """
        Get a memory by ID.
        
        Args:
            memory_id: ID of the memory to get
            
        Returns:
            The memory if found, None otherwise
        """
        memory = self.memories.get(memory_id)
        
        if memory:
            # Update last accessed time
            memory.last_accessed = datetime.datetime.now()
            self.save_memory(memory)
        
        return memory
    
    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Memory]:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of the memory to update
            content: New content for the memory, if None, keeps existing content
            metadata: New metadata for the memory, if None, keeps existing metadata
            
        Returns:
            The updated memory if found, None otherwise
        """
        memory = self.memories.get(memory_id)
        
        if not memory:
            self.logger.warning(f"Memory {memory_id} not found for update")
            return None
        
        if content is not None:
            memory.content = content
        
        if metadata is not None:
            memory.metadata = metadata
        
        memory.last_accessed = datetime.datetime.now()
        
        self.save_memory(memory)
        
        self.logger.info(f"Updated memory {memory_id}")
        
        return memory
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: ID of the memory to delete
            
        Returns:
            True if the memory was deleted, False otherwise
        """
        if memory_id not in self.memories:
            self.logger.warning(f"Memory {memory_id} not found for deletion")
            return False
        
        memory_path = self.storage_path / f"{memory_id}.json"
        
        try:
            os.remove(memory_path)
        except Exception as e:
            self.logger.error(f"Error deleting memory file {memory_path}: {e}")
        
        del self.memories[memory_id]
        
        self.logger.info(f"Deleted memory {memory_id}")
        
        return True
    
    def search_memories(self, query: MemoryQuery) -> List[Memory]:
        """
        Search for memories based on a query.
        
        Args:
            query: The query to search with
            
        Returns:
            List of matching memories
        """
        results = []
        
        for memory in self.memories.values():
            # Check memory type
            if query.memory_type and memory.type != query.memory_type:
                continue
            
            # Check content
            if query.content_contains and query.content_contains.lower() not in memory.content.lower():
                continue
            
            # Check created time range
            if query.created_after and memory.created_at < query.created_after:
                continue
            
            if query.created_before and memory.created_at > query.created_before:
                continue
            
            # Check metadata
            if query.metadata:
                match = True
                for key, value in query.metadata.items():
                    if key not in memory.metadata or memory.metadata[key] != value:
                        match = False
                        break
                
                if not match:
                    continue
            
            results.append(memory)
        
        # Sort results by creation time (newest first)
        results.sort(key=lambda m: m.created_at, reverse=True)
        
        # Apply limit if specified
        if query.limit and len(results) > query.limit:
            results = results[:query.limit]
        
        # Update last accessed time for retrieved memories
        now = datetime.datetime.now()
        for memory in results:
            memory.last_accessed = now
            self.save_memory(memory)
        
        return results
    
    def clear_all_memories(self) -> None:
        """
        Clear all memories from storage.
        """
        for memory_id in list(self.memories.keys()):
            self.delete_memory(memory_id)
        
        self.logger.warning("Cleared all memories")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored memories.
        
        Returns:
            Dictionary of memory statistics
        """
        memory_types = {}
        total_size = 0
        oldest_memory = None
        newest_memory = None
        
        for memory in self.memories.values():
            # Count by type
            memory_type = memory.type.value
            memory_types[memory_type] = memory_types.get(memory_type, 0) + 1
            
            # Calculate size
            memory_size = len(memory.content) + sum(len(str(k)) + len(str(v)) for k, v in memory.metadata.items())
            total_size += memory_size
            
            # Track oldest and newest
            if oldest_memory is None or memory.created_at < oldest_memory.created_at:
                oldest_memory = memory
            
            if newest_memory is None or memory.created_at > newest_memory.created_at:
                newest_memory = memory
        
        return {
            "total_memories": len(self.memories),
            "memory_types": memory_types,
            "total_size_bytes": total_size,
            "oldest_memory": oldest_memory.id if oldest_memory else None,
            "oldest_memory_date": oldest_memory.created_at.isoformat() if oldest_memory else None,
            "newest_memory": newest_memory.id if newest_memory else None,
            "newest_memory_date": newest_memory.created_at.isoformat() if newest_memory else None
        }