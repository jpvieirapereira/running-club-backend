from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class TaskDTO:
    """Data Transfer Object for Task."""
    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    user_id: UUID


@dataclass
class CreateTaskDTO:
    """DTO for creating a task."""
    title: str
    description: Optional[str] = None


@dataclass
class UpdateTaskDTO:
    """DTO for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
