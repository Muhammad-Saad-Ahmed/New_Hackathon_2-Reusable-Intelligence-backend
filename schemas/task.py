"""
Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


# User schemas
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    # Note: hashed_password is intentionally excluded from the response

    class Config:
        from_attributes = True


# Task schemas
class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = Field(default="medium", pattern="^(low|medium|high)$")  # low, medium, high
    tags: Optional[List[str]] = []


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")  # low, medium, high
    tags: Optional[List[str]] = None


class Task(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Response schemas
class TaskResponse(BaseModel):
    success: bool
    data: Task


class TasksResponse(BaseModel):
    success: bool
    data: List[Task]


class MessageResponse(BaseModel):
    success: bool
    message: str


class TokenData(BaseModel):
    user_id: str