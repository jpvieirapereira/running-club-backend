from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from src.application.use_cases import TaskUseCase
from src.application.dtos import CreateTaskDTO, UpdateTaskDTO, UserDTO
from src.presentation.schemas import TaskCreate, TaskUpdate, TaskResponse
from src.presentation.api.dependencies import get_current_active_user
from src.infrastructure.container import Container


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_task(
    task_data: TaskCreate,
    current_user: UserDTO = Depends(get_current_active_user),
    task_use_case: TaskUseCase = Depends(Provide[Container.task_use_case])
):
    """Create a new task."""
    dto = CreateTaskDTO(title=task_data.title, description=task_data.description)
    task = await task_use_case.create_task(dto, current_user.id)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id
    )


@router.get("", response_model=List[TaskResponse])
@inject
async def list_tasks(
    current_user: UserDTO = Depends(get_current_active_user),
    task_use_case: TaskUseCase = Depends(Provide[Container.task_use_case])
):
    """List all tasks for the current user."""
    tasks = await task_use_case.list_user_tasks(current_user.id)
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id
        )
        for task in tasks
    ]


@router.get("/{task_id}", response_model=TaskResponse)
@inject
async def get_task(
    task_id: UUID,
    current_user: UserDTO = Depends(get_current_active_user),
    task_use_case: TaskUseCase = Depends(Provide[Container.task_use_case])
):
    """Get a specific task."""
    task = await task_use_case.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id
    )


@router.put("/{task_id}", response_model=TaskResponse)
@inject
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: UserDTO = Depends(get_current_active_user),
    task_use_case: TaskUseCase = Depends(Provide[Container.task_use_case])
):
    """Update a task."""
    dto = UpdateTaskDTO(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )
    task = await task_use_case.update_task(task_id, dto, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_task(
    task_id: UUID,
    current_user: UserDTO = Depends(get_current_active_user),
    task_use_case: TaskUseCase = Depends(Provide[Container.task_use_case])
):
    """Delete a task."""
    success = await task_use_case.delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
