from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class TaskBase(BaseModel):
    """Base schema for Task."""
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: UUID
    completed: bool
    user_id: UUID
    
    class Config:
        from_attributes = True
