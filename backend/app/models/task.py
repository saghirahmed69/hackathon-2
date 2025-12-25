"""
Task model for SQLModel ORM.
"""

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, Literal
from datetime import datetime
import uuid


# Type aliases for Phase III Advanced Features
PriorityLevel = Literal['high', 'medium', 'low']
RecurrencePattern = Literal['daily', 'weekly', 'monthly']


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Relationships:
        - Belongs to one User (many-to-one)

    Phase II Fields:
        - id, user_id, title, description, completed, created_at, updated_at

    Phase III Advanced Features:
        - priority: Task importance level (high, medium, low)
        - due_date: Optional deadline with optional time
        - is_recurring: Whether task regenerates when completed
        - recurrence_pattern: Frequency for recurring tasks (daily, weekly, monthly)
        - reminder_time: Optional timestamp for browser notification
    """
    __tablename__ = "tasks"

    # Phase II Core Fields
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=1000)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Phase III Advanced Features (003-advanced-task-features)
    # Note: Using str instead of Literal for SQLModel compatibility
    # Validation happens in Pydantic schemas (task_service.py, schemas/task.py)
    priority: str = Field(default='medium', max_length=10)
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=20, nullable=True)
    reminder_time: Optional[datetime] = Field(default=None, nullable=True)

    # Relationship (optional - only if User model has back_populates)
    # owner: Optional["User"] = Relationship(back_populates="tasks")
