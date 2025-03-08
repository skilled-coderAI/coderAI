"""
CoderAI Workflow Module
This module provides workflow management capabilities for CoderAI agents,
allowing them to execute complex multi-step tasks.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional, Union, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto

T = TypeVar('T')

class WorkflowStepStatus(Enum):
    """Status of a workflow step."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class WorkflowStatus(Enum):
    """Status of a workflow."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

@dataclass
class WorkflowStepResult(Generic[T]):
    """Result of a workflow step execution."""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowStep:
    """
    A step in a workflow.
    
    Each step has a unique ID, a name, a function to execute,
    and optional dependencies on other steps.
    """
    id: str
    name: str
    description: str
    function: Callable[..., Any]
    dependencies: List[str] = field(default_factory=list)
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING
    result: Optional[WorkflowStepResult] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        function: Callable[..., Any],
        dependencies: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> 'WorkflowStep':
        """
        Create a new workflow step.
        
        Args:
            name: Name of the step
            description: Description of what the step does
            function: Function to execute for this step
            dependencies: IDs of steps that must complete before this step
            metadata: Additional metadata for the step
            
        Returns:
            Created workflow step
        """
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            function=function,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )
    
    def execute(self, context: Dict[str, Any]) -> WorkflowStepResult:
        """
        Execute the step function with the provided context.
        
        Args:
            context: Context data for execution, including results from previous steps
            
        Returns:
            Result of the step execution
        """
        self.status = WorkflowStepStatus.RUNNING
        self.started_at = datetime.now()
        
        try:
            result_data = self.function(context)
            self.result = WorkflowStepResult(success=True, data=result_data)
            self.status = WorkflowStepStatus.COMPLETED
        except Exception as e:
            error_msg = str(e)
            self.result = WorkflowStepResult(success=False, error=error_msg)
            self.status = WorkflowStepStatus.FAILED
        
        self.completed_at = datetime.now()
        return self.result

@dataclass
class Workflow:
    """
    A workflow composed of multiple steps.
    
    Workflows manage the execution of steps in the correct order,
    respecting dependencies between steps.
    """
    id: str
    name: str
    description: str
    steps: Dict[str, WorkflowStep] = field(default_factory=dict)
    status: WorkflowStatus = WorkflowStatus.PENDING
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        steps: List[WorkflowStep] = None,
        metadata: Dict[str, Any] = None
    ) -> 'Workflow':
        """
        Create a new workflow.
        
        Args:
            name: Name of the workflow
            description: Description of what the workflow does
            steps: Steps to include in the workflow
            metadata: Additional metadata for the workflow
            
        Returns:
            Created workflow
        """
        workflow = cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            metadata=metadata or {},
        )
        
        if steps:
            for step in steps:
                workflow.add_step(step)
        
        return workflow
    
    def add_step(self, step: WorkflowStep) -> None:
        """
        Add a step to the workflow.
        
        Args:
            step: Step to add
        """
        self.steps[step.id] = step
    
    def get_step(self, step_id: str) -> Optional[WorkflowStep]:
        """
        Get a step by ID.
        
        Args:
            step_id: ID of the step to get
            
        Returns:
            The step if found, None otherwise
        """
        return self.steps.get(step_id)
    
    def get_ready_steps(self) -> List[WorkflowStep]:
        """
        Get steps that are ready to be executed.
        
        A step is ready if:
        1. It is in PENDING status
        2. All its dependencies have been COMPLETED
        
        Returns:
            List of steps ready for execution
        """
        ready_steps = []
        
        for step in self.steps.values():
            if step.status != WorkflowStepStatus.PENDING:
                continue
            
            dependencies_met = True
            for dep_id in step.dependencies:
                dep_step = self.steps.get(dep_id)
                if not dep_step or dep_step.status != WorkflowStepStatus.COMPLETED:
                    dependencies_met = False
                    break
            
            if dependencies_met:
                ready_steps.append(step)
        
        return ready_steps
    
    def execute(self) -> Dict[str, WorkflowStepResult]:
        """
        Execute the workflow.
        
        This will execute all steps in the correct order,
        respecting dependencies between steps.
        
        Returns:
            Dictionary mapping step IDs to their results
        """
        self.status = WorkflowStatus.RUNNING
        self.started_at = datetime.now()
        
        # Continue executing steps until all are completed or failed
        while True:
            ready_steps = self.get_ready_steps()
            
            if not ready_steps:
                # No more steps to execute
                all_completed = all(
                    step.status in [WorkflowStepStatus.COMPLETED, WorkflowStepStatus.SKIPPED]
                    for step in self.steps.values()
                )
                
                if all_completed:
                    self.status = WorkflowStatus.COMPLETED
                else:
                    self.status = WorkflowStatus.FAILED
                
                break
            
            # Execute all ready steps
            for step in ready_steps:
                result = step.execute(self.context)
                
                # Add the result to the context for use by later steps
                self.context[step.id] = result.data
        
        self.completed_at = datetime.now()
        
        # Return all step results
        return {step_id: step.result for step_id, step in self.steps.items()}
    
    def cancel(self) -> None:
        """Cancel the workflow execution."""
        self.status = WorkflowStatus.CANCELLED
    
    def pause(self) -> None:
        """Pause the workflow execution."""
        self.status = WorkflowStatus.PAUSED
    
    def resume(self) -> None:
        """Resume the workflow execution."""
        if self.status == WorkflowStatus.PAUSED:
            self.status = WorkflowStatus.RUNNING
    
    def reset(self) -> None:
        """Reset the workflow to its initial state."""
        self.status = WorkflowStatus.PENDING
        self.context = {}
        self.started_at = None
        self.completed_at = None
        
        for step in self.steps.values():
            step.status = WorkflowStepStatus.PENDING
            step.result = None
            step.started_at = None
            step.completed_at = None
    
    def get_execution_graph(self) -> Dict[str, List[str]]:
        """
        Get the execution graph of the workflow.
        
        Returns:
            Dictionary mapping step IDs to lists of dependent step IDs
        """
        graph = {}
        
        for step_id, step in self.steps.items():
            graph[step_id] = []
            
            for other_id, other_step in self.steps.items():
                if step_id in other_step.dependencies:
                    graph[step_id].append(other_id)
        
        return graph
    
    def get_status_summary(self) -> Dict[str, int]:
        """
        Get a summary of step statuses.
        
        Returns:
            Dictionary mapping status names to counts
        """
        summary = {status.value: 0 for status in WorkflowStepStatus}
        
        for step in self.steps.values():
            summary[step.status.value] += 1
        
        return summary