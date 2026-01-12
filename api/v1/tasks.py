"""
Task API endpoints for the Todo Application backend.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from services.task_service import TaskService
from schemas.task import TaskCreate, TaskUpdate, Task, TasksResponse, TaskResponse, MessageResponse
from middleware.auth_middleware import JWTBearer
from uuid import UUID
import uuid


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=TasksResponse)
async def get_tasks(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter by status: completed, incomplete"),
    priority: Optional[str] = Query(None, description="Filter by priority: high, medium, low"),
    db: Session = Depends(get_db),
    token_data: dict = Depends(JWTBearer())
):
    """
    Retrieve all tasks for a specific user with optional filtering.
    """
    # Verify that the user_id in the token matches the one in the URL
    if token_data.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access to these tasks"
        )
    try:
        user_uuid = uuid.UUID(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    task_service = TaskService(db)
    tasks = task_service.get_tasks_by_user(user_uuid, status, priority)

    return TasksResponse(success=True, data=tasks)


@router.post("/{user_id}/tasks", response_model=TaskResponse)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(JWTBearer())
):
    """
    Create a new task for a specific user.
    """
    # Verify that the user_id in the token matches the one in the URL
    if token_data.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to create tasks for this user"
        )
    try:
        user_uuid = uuid.UUID(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    task_service = TaskService(db)
    task = task_service.create_task(user_uuid, task_data)

    return TaskResponse(success=True, data=task)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    token_data: dict = Depends(JWTBearer())
):
    """
    Retrieve a specific task for a user.
    """
    # Verify that the user_id in the token matches the one in the URL
    if token_data.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access to this task"
        )
    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user or task ID format")

    task_service = TaskService(db)
    task = task_service.get_task_by_id(user_uuid, task_uuid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(success=True, data=task)


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(JWTBearer())
):
    """
    Update a specific task for a user.
    """
    # Verify that the user_id in the token matches the one in the URL
    if token_data.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to update this task"
        )
    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user or task ID format")

    task_service = TaskService(db)
    task = task_service.update_task(user_uuid, task_uuid, task_data)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(success=True, data=task)


@router.delete("/{user_id}/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(
    user_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    token_data: dict = Depends(JWTBearer())
):
    """
    Delete a specific task for a user.
    """
    # Verify that the user_id in the token matches the one in the URL
    if token_data.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to delete this task"
        )
    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user or task ID format")

    task_service = TaskService(db)
    success = task_service.delete_task(user_uuid, task_uuid)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return MessageResponse(success=True, message="Task deleted successfully")


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    completed: bool = Query(..., description="Set the completion status"),
    db: Session = Depends(get_db),
    token_data: dict = Depends(JWTBearer())
):
    """
    Toggle the completion status of a specific task for a user.
    """
    # Verify that the user_id in the token matches the one in the URL
    if token_data.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to update this task"
        )
    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user or task ID format")

    task_service = TaskService(db)
    task = task_service.toggle_task_completion(user_uuid, task_uuid, completed)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(success=True, data=task)