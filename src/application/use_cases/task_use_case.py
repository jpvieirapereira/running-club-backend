from typing import List, Optional
from uuid import UUID
from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository
from src.application.dtos import TaskDTO, CreateTaskDTO, UpdateTaskDTO


class TaskUseCase:
    """Use case for task management."""
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    async def create_task(self, dto: CreateTaskDTO, user_id: UUID) -> TaskDTO:
        """Create a new task."""
        task = Task(
            title=dto.title,
            description=dto.description,
            user_id=user_id
        )
        
        created_task = await self.task_repository.create(task)
        
        return TaskDTO(
            id=created_task.id,
            title=created_task.title,
            description=created_task.description,
            completed=created_task.completed,
            user_id=created_task.user_id
        )
    
    async def get_task(self, task_id: UUID, user_id: UUID) -> Optional[TaskDTO]:
        """Get a task by ID."""
        task = await self.task_repository.get_by_id(task_id)
        
        if not task or task.user_id != user_id:
            return None
        
        return TaskDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id
        )
    
    async def list_user_tasks(self, user_id: UUID) -> List[TaskDTO]:
        """List all tasks for a user."""
        tasks = await self.task_repository.get_by_user_id(user_id)
        
        return [
            TaskDTO(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id
            )
            for task in tasks
        ]
    
    async def update_task(self, task_id: UUID, dto: UpdateTaskDTO, user_id: UUID) -> Optional[TaskDTO]:
        """Update a task."""
        task = await self.task_repository.get_by_id(task_id)
        
        if not task or task.user_id != user_id:
            return None
        
        if dto.title is not None or dto.description is not None:
            task.update(title=dto.title, description=dto.description)
        
        if dto.completed is not None:
            if dto.completed:
                task.mark_as_completed()
            else:
                task.mark_as_incomplete()
        
        updated_task = await self.task_repository.update(task)
        
        return TaskDTO(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
            user_id=updated_task.user_id
        )
    
    async def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete a task."""
        task = await self.task_repository.get_by_id(task_id)
        
        if not task or task.user_id != user_id:
            return False
        
        return await self.task_repository.delete(task_id)
