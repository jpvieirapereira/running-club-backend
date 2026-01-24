from typing import Optional
from uuid import UUID
from src.domain.entities.base import Entity


class Task(Entity):
    """Task domain entity."""
    
    def __init__(
        self,
        title: str,
        user_id: UUID,
        description: Optional[str] = None,
        completed: bool = False,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self.title = title
        self.description = description
        self.completed = completed
        self.user_id = user_id
    
    def mark_as_completed(self):
        """Mark task as completed."""
        self.completed = True
    
    def mark_as_incomplete(self):
        """Mark task as incomplete."""
        self.completed = False
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None):
        """Update task details."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
