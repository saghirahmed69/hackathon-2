"""
Task model for SQLModel ORM.
"""

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime
import uuid


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Relationships:
        - Belongs to one User (many-to-one)
    """
    __tablename__ = "tasks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=1000)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship (optional - only if User model has back_populates)
    # owner: Optional["User"] = Relationship(back_populates="tasks")
