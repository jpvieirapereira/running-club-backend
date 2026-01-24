from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.task import Task


class TaskRepository(ABC):
    """Repository interface for Task entity."""
    
    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Create a new task."""
        pass
    
    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID."""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Task]:
        """Get all tasks for a user."""
        pass
    
    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Update existing task."""
        pass
    
    @abstractmethod
    async def delete(self, task_id: UUID) -> bool:
        """Delete task by ID."""
        pass
