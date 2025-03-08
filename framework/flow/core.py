"""
CoderAI Framework Flow Core
This module provides the core functionality for the workflow management system.
"""

import time
import uuid
import asyncio
from typing import Dict, Any, List, Callable, Optional, Union, Set
from .types import Event, EventStatus, EventHandler, EventGroup, Workflow, EventBus
from ..logger import LoggerManager

logger = LoggerManager.get_logger()

class WorkflowManager:
    """
    Manager for workflows.
    """
    def __init__(self):
        """
        Initialize the workflow manager.
        """
        self.event_bus = EventBus()
        self.running_workflows = set()
        
    def register_handler(self, event_type: str, handler: Callable[[Event], Any], priority: int = 0, metadata: Dict[str, Any] = None):
        """
        Register a handler for an event type.
        
        Args:
            event_type: Type of event to handle
            handler: Handler function
            priority: Priority of the handler
            metadata: Metadata for the handler
        """
        self.event_bus.register_handler(event_type, handler, priority, metadata)
        
    def emit_event(self, event_type: str, data: Dict[str, Any] = None, parent_id: str = None, metadata: Dict[str, Any] = None):
        """
        Emit an event.
        
        Args:
            event_type: Type of event to emit
            data: Data for the event
            parent_id: ID of the parent event
            metadata: Metadata for the event
            
        Returns:
            Emitted event
        """
        if data is None:
            data = {}
            
        if metadata is None:
            metadata = {}
            
        event_id = str(uuid.uuid4())
        current_time = time.time()
        
        event = Event(
            id=event_id,
            type=event_type,
            data=data,
            status=EventStatus.PENDING,
            created_at=current_time,
            updated_at=current_time,
            parent_id=parent_id,
            metadata=metadata,
        )
        
        self.event_bus.emit(event)
        
        return event
        
    def create_event_group(self, name: str, events: List[Event] = None, metadata: Dict[str, Any] = None):
        """
        Create an event group.
        
        Args:
            name: Name of the event group
            events: Events in the group
            metadata: Metadata for the event group
            
        Returns:
            Created event group
        """
        group_id = str(uuid.uuid4())
        
        return self.event_bus.create_event_group(
            id=group_id,
            name=name,
            events=events or [],
            metadata=metadata or {},
        )
        
    def create_workflow(self, name: str, description: str, event_groups: List[EventGroup] = None, metadata: Dict[str, Any] = None):
        """
        Create a workflow.
        
        Args:
            name: Name of the workflow
            description: Description of the workflow
            event_groups: Event groups in the workflow
            metadata: Metadata for the workflow
            
        Returns:
            Created workflow
        """
        workflow_id = str(uuid.uuid4())
        
        return self.event_bus.create_workflow(
            id=workflow_id,
            name=name,
            description=description,
            event_groups=event_groups or [],
            metadata=metadata or {},
        )
        
    def start_workflow(self, workflow: Workflow):
        """
        Start a workflow.
        
        Args:
            workflow: Workflow to start
        """
        if workflow.id in self.running_workflows:
            if logger:
                logger.warning(f"Workflow '{workflow.name}' is already running")
            return
            
        self.running_workflows.add(workflow.id)
        
        current_time = time.time()
        workflow.status = EventStatus.RUNNING
        workflow.updated_at = current_time
        
        for event_group in workflow.event_groups:
            event_group.status = EventStatus.RUNNING
            event_group.updated_at = current_time
            
            for event in event_group.events:
                # Only start events with no dependencies
                if not event.dependencies:
                    event.status = EventStatus.RUNNING
                    event.updated_at = current_time
                    
                    self.event_bus.emit(event)
                    
        if logger:
            logger.info(f"Started workflow '{workflow.name}'")
            
    def stop_workflow(self, workflow: Workflow):
        """
        Stop a workflow.
        
        Args:
            workflow: Workflow to stop
        """
        if workflow.id not in self.running_workflows:
            if logger:
                logger.warning(f"Workflow '{workflow.name}' is not running")
            return
            
        self.running_workflows.remove(workflow.id)
        
        current_time = time.time()
        workflow.status = EventStatus.CANCELLED
        workflow.updated_at = current_time
        workflow.completed_at = current_time
        
        for event_group in workflow.event_groups:
            event_group.status = EventStatus.CANCELLED
            event_group.updated_at = current_time
            event_group.completed_at = current_time
            
            for event in event_group.events:
                if event.status in [EventStatus.PENDING, EventStatus.RUNNING]:
                    event.status = EventStatus.CANCELLED
                    event.updated_at = current_time
                    event.completed_at = current_time
                    
        if logger:
            logger.info(f"Stopped workflow '{workflow.name}'")
            
    def get_workflow_status(self, workflow: Workflow):
        """
        Get the status of a workflow.
        
        Args:
            workflow: Workflow to get status for
            
        Returns:
            Status of the workflow
        """
        # Check if all event groups are completed
        all_completed = True
        all_failed = True
        
        for event_group in workflow.event_groups:
            if event_group.status != EventStatus.COMPLETED:
                all_completed = False
                
            if event_group.status != EventStatus.FAILED:
                all_failed = False
                
        if all_completed:
            workflow.status = EventStatus.COMPLETED
            workflow.updated_at = time.time()
            workflow.completed_at = time.time()
            
            if workflow.id in self.running_workflows:
                self.running_workflows.remove(workflow.id)
                
            if logger:
                logger.info(f"Workflow '{workflow.name}' completed")
                
        elif all_failed:
            workflow.status = EventStatus.FAILED
            workflow.updated_at = time.time()
            workflow.completed_at = time.time()
            
            if workflow.id in self.running_workflows:
                self.running_workflows.remove(workflow.id)
                
            if logger:
                logger.error(f"Workflow '{workflow.name}' failed")
                
        return workflow.status
        
    def get_event_group_status(self, event_group: EventGroup):
        """
        Get the status of an event group.
        
        Args:
            event_group: Event group to get status for
            
        Returns:
            Status of the event group
        """
        # Check if all events are completed
        all_completed = True
        all_failed = True
        
        for event in event_group.events:
            if event.status != EventStatus.COMPLETED:
                all_completed = False
                
            if event.status != EventStatus.FAILED:
                all_failed = False
                
        if all_completed:
            event_group.status = EventStatus.COMPLETED
            event_group.updated_at = time.time()
            event_group.completed_at = time.time()
            
            if logger:
                logger.info(f"Event group '{event_group.name}' completed")
                
        elif all_failed:
            event_group.status = EventStatus.FAILED
            event_group.updated_at = time.time()
            event_group.completed_at = time.time()
            
            if logger:
                logger.error(f"Event group '{event_group.name}' failed")
                
        return event_group.status
        
    def update_event_dependencies(self, event: Event):
        """
        Update dependencies for an event.
        
        Args:
            event: Event to update dependencies for
        """
        # Check if all dependencies are completed
        all_dependencies_completed = True
        
        for dep_id in event.dependencies:
            dep_event = self.event_bus.events.get(dep_id)
            
            if not dep_event or dep_event.status != EventStatus.COMPLETED:
                all_dependencies_completed = False
                break
                
        if all_dependencies_completed and event.status == EventStatus.PENDING:
            event.status = EventStatus.RUNNING
            event.updated_at = time.time()
            
            self.event_bus.emit(event)
            
    def update_dependent_events(self, event: Event):
        """
        Update events that depend on the given event.
        
        Args:
            event: Event that dependents depend on
        """
        for dep_id in event.dependents:
            dep_event = self.event_bus.events.get(dep_id)
            
            if dep_event:
                self.update_event_dependencies(dep_event)
                
    def add_dependency(self, event: Event, dependency: Event):
        """
        Add a dependency to an event.
        
        Args:
            event: Event to add dependency to
            dependency: Dependency to add
        """
        if dependency.id not in event.dependencies:
            event.dependencies.append(dependency.id)
            
        if event.id not in dependency.dependents:
            dependency.dependents.append(event.id)
            
    def remove_dependency(self, event: Event, dependency: Event):
        """
        Remove a dependency from an event.
        
        Args:
            event: Event to remove dependency from
            dependency: Dependency to remove
        """
        if dependency.id in event.dependencies:
            event.dependencies.remove(dependency.id)
            
        if event.id in dependency.dependents:
            dependency.dependents.remove(event.id)
            
    def add_event_to_group(self, event: Event, event_group: EventGroup):
        """
        Add an event to an event group.
        
        Args:
            event: Event to add
            event_group: Event group to add to
        """
        if event not in event_group.events:
            event_group.events.append(event)
            
    def remove_event_from_group(self, event: Event, event_group: EventGroup):
        """
        Remove an event from an event group.
        
        Args:
            event: Event to remove
            event_group: Event group to remove from
        """
        if event in event_group.events:
            event_group.events.remove(event)
            
    def add_event_group_to_workflow(self, event_group: EventGroup, workflow: Workflow):
        """
        Add an event group to a workflow.
        
        Args:
            event_group: Event group to add
            workflow: Workflow to add to
        """
        if event_group not in workflow.event_groups:
            workflow.event_groups.append(event_group)
            
    def remove_event_group_from_workflow(self, event_group: EventGroup, workflow: Workflow):
        """
        Remove an event group from a workflow.
        
        Args:
            event_group: Event group to remove
            workflow: Workflow to remove from
        """
        if event_group in workflow.event_groups:
            workflow.event_groups.remove(event_group)

# Create global workflow manager
workflow_manager = WorkflowManager()
