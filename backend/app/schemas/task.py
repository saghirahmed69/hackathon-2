"""
Pydantic schemas for task requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    """Request schema for creating a task."""

    title: str = Field(min_length=1, max_length=1000)
    description: Optional[str] = Field(default=None, max_length=10000)


class TaskUpdate(BaseModel):
    """Request schema for updating a task (all fields optional)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Response schema for task data."""

    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True
