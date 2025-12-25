"""
Pydantic schemas for task requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


# Type aliases for Phase III Advanced Features
PriorityLevel = Literal['high', 'medium', 'low']
RecurrencePattern = Literal['daily', 'weekly', 'monthly']


class TaskCreate(BaseModel):
    """
    Request schema for creating a task.

    Phase II Fields:
        - title (required)
        - description (optional)

    Phase III Advanced Features:
        - priority (required, default 'medium')
        - due_date (optional ISO 8601 timestamp)
        - is_recurring (optional, default False)
        - recurrence_pattern (optional: daily, weekly, monthly)
        - reminder_time (optional ISO 8601 timestamp, must be in future)
    """

    # Phase II Core Fields
    title: str = Field(min_length=1, max_length=1000)
    description: Optional[str] = Field(default=None, max_length=10000)

    # Phase III Advanced Features (003-advanced-task-features)
    priority: PriorityLevel = Field(default='medium')
    due_date: Optional[str] = Field(default=None)  # ISO 8601 format
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None)
    reminder_time: Optional[str] = Field(default=None)  # ISO 8601 format


class TaskUpdate(BaseModel):
    """
    Request schema for updating a task (all fields optional).

    Phase II Fields:
        - title, description, completed

    Phase III Advanced Features:
        - priority, due_date, is_recurring, recurrence_pattern, reminder_time
    """

    # Phase II Core Fields
    title: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: Optional[bool] = None

    # Phase III Advanced Features (003-advanced-task-features)
    priority: Optional[PriorityLevel] = None
    due_date: Optional[str] = None  # ISO 8601 format
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    reminder_time: Optional[str] = None  # ISO 8601 format


class TaskResponse(BaseModel):
    """
    Response schema for task data.

    Phase II Fields:
        - id, user_id, title, description, completed, created_at, updated_at

    Phase III Advanced Features:
        - priority, due_date, is_recurring, recurrence_pattern, reminder_time
    """

    # Phase II Core Fields
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: Optional[str]

    # Phase III Advanced Features (003-advanced-task-features)
    priority: str  # Returned as string
    due_date: Optional[str]  # ISO 8601 or null
    is_recurring: bool
    recurrence_pattern: Optional[str]  # 'daily', 'weekly', 'monthly', or null
    reminder_time: Optional[str]  # ISO 8601 or null

    class Config:
        from_attributes = True
