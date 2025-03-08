"""
CoderAI Framework Memory Types
This module defines the data types used in the memory management system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import uuid
from enum import Enum, auto

class MemoryType(Enum):
    """
    Types of memories that can be stored.
    """
    CONVERSATION = "conversation"
    CODE_SNIPPET = "code_snippet"
    REQUIREMENT = "requirement"
    PREFERENCE = "preference"
    FEEDBACK = "feedback"
    ERROR = "error"
    SOLUTION = "solution"
    GENERAL = "general"

@dataclass
class MemoryQuery:
    """
    Query parameters for searching memories.
    """
    memory_type: Optional[MemoryType] = None
    content_contains: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    limit: Optional[int] = None

@dataclass
class Memory:
    """
    Memory item in the memory management system.
    """
    id: str
    content: str
    type: MemoryType = MemoryType.GENERAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None
    embedding: Optional[List[float]] = None
    
    @classmethod
    def create(cls, content: str, memory_type: MemoryType = MemoryType.GENERAL, metadata: Dict[str, Any] = None):
        """
        Create a new memory.
        
        Args:
            content: Content of the memory
            memory_type: Type of the memory
            metadata: Metadata for the memory
            
        Returns:
            Created memory
        """
        return cls(
            id=str(uuid.uuid4()),
            content=content,
            type=memory_type,
            metadata=metadata or {},
        )

@dataclass
class MemoryGroup:
    """
    Group of related memories.
    """
    id: str
    name: str
    memories: List[Memory] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, name: str, memories: List[Memory] = None, metadata: Dict[str, Any] = None):
        """
        Create a new memory group.
        
        Args:
            name: Name of the memory group
            memories: Memories in the group
            metadata: Metadata for the memory group
            
        Returns:
            Created memory group
        """
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            memories=memories or [],
            metadata=metadata or {},
        )

@dataclass
class MemorySearchResult:
    """
    Result of a memory search.
    """
    memory: Memory
    score: float
    
    def __lt__(self, other):
        return self.score < other.score