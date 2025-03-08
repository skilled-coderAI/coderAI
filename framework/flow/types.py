"""
CoderAI Framework Flow Types
This module defines the data types used in the workflow management system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Optional, Union, Set
from enum import Enum

class EventStatus(Enum):
    """
    Status of an event.
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Event:
    """
    Event in a workflow.
    """
    id: str
    type: str
    data: Dict[str, Any] = field(default_factory=dict)
    status: EventStatus = EventStatus.PENDING
    created_at: float = None
    updated_at: float = None
    completed_at: float = None
    error: Optional[str] = None
    result: Optional[Any] = None
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventHandler:
    """
    Handler for an event.
    """
    event_type: str
    handler: Callable[[Event], Any]
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventGroup:
    """
    Group of related events.
    """
    id: str
    name: str
    events: List[Event] = field(default_factory=list)
    status: EventStatus = EventStatus.PENDING
    created_at: float = None
    updated_at: float = None
    completed_at: float = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Workflow:
    """
    Workflow definition.
    """
    id: str
    name: str
    description: str
    event_groups: List[EventGroup] = field(default_factory=list)
    status: EventStatus = EventStatus.PENDING
    created_at: float = None
    updated_at: float = None
    completed_at: float = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventBus:
    """
    Event bus for managing events.
    """
    handlers: Dict[str, List[EventHandler]] = field(default_factory=lambda: defaultdict(list))
    events: Dict[str, Event] = field(default_factory=dict)
    event_groups: Dict[str, EventGroup] = field(default_factory=dict)
    workflows: Dict[str, Workflow] = field(default_factory=dict)
    
    def register_handler(self, event_type: str, handler: Callable[[Event], Any], priority: int = 0, metadata: Dict[str, Any] = None):
        """
        Register a handler for an event type.
        
        Args:
            event_type: Type of event to handle
            handler: Handler function
            priority: Priority of the handler
            metadata: Metadata for the handler
        """
        if metadata is None:
            metadata = {}
            
        event_handler = EventHandler(
            event_type=event_type,
            handler=handler,
            priority=priority,
            metadata=metadata,
        )
        
        self.handlers[event_type].append(event_handler)
        self.handlers[event_type].sort(key=lambda h: h.priority, reverse=True)
        
    def emit(self, event: Event):
        """
        Emit an event.
        
        Args:
            event: Event to emit
        """
        self.events[event.id] = event
        
        for handler in self.handlers.get(event.type, []):
            try:
                handler.handler(event)
            except Exception as e:
                event.status = EventStatus.FAILED
                event.error = str(e)
                
    def create_event_group(self, id: str, name: str, events: List[Event] = None, metadata: Dict[str, Any] = None):
        """
        Create an event group.
        
        Args:
            id: ID of the event group
            name: Name of the event group
            events: Events in the group
            metadata: Metadata for the event group
            
        Returns:
            Created event group
        """
        if events is None:
            events = []
            
        if metadata is None:
            metadata = {}
            
        event_group = EventGroup(
            id=id,
            name=name,
            events=events,
            metadata=metadata,
        )
        
        self.event_groups[id] = event_group
        
        return event_group
        
    def create_workflow(self, id: str, name: str, description: str, event_groups: List[EventGroup] = None, metadata: Dict[str, Any] = None):
        """
        Create a workflow.
        
        Args:
            id: ID of the workflow
            name: Name of the workflow
            description: Description of the workflow
            event_groups: Event groups in the workflow
            metadata: Metadata for the workflow
            
        Returns:
            Created workflow
        """
        if event_groups is None:
            event_groups = []
            
        if metadata is None:
            metadata = {}
            
        workflow = Workflow(
            id=id,
            name=name,
            description=description,
            event_groups=event_groups,
            metadata=metadata,
        )
        
        self.workflows[id] = workflow
        
        return workflow

# Circular import workaround
from collections import defaultdict
