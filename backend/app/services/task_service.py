"""
Task service with CRUD operations and user isolation.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_user_tasks(session: AsyncSession, user_id: str) -> List[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: User ID to filter tasks

    Returns:
        List of tasks belonging to the user
    """
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()
    return list(tasks)


async def create_task(
    session: AsyncSession, user_id: str, data: TaskCreate
) -> Task:
    """
    Create a new task for a user.

    Args:
        session: Database session
        user_id: User ID who owns the task
        data: Task creation data

    Returns:
        Created task

    Raises:
        HTTPException 400: If validation fails (empty title, whitespace only)
    """
    # Validate title (not empty, not whitespace only)
    if not data.title or not data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty or whitespace",
        )

    # Create task
    task = Task(
        user_id=user_id,
        title=data.title.strip(),
        description=data.description.strip() if data.description else None,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def update_task(
    session: AsyncSession, task_id: str, user_id: str, data: TaskUpdate
) -> Optional[Task]:
    """
    Update an existing task (ownership verified).

    Args:
        session: Database session
        task_id: Task ID to update
        user_id: User ID (for ownership verification)
        data: Task update data (partial updates allowed)

    Returns:
        Updated task, or None if task not found or user doesn't own it

    Raises:
        HTTPException 400: If validation fails
    """
    # Get task with ownership check
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        return None

    # Update fields if provided
    if data.title is not None:
        # Validate title
        if not data.title or not data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty or whitespace",
            )
        task.title = data.title.strip()

    if data.description is not None:
        task.description = data.description.strip() if data.description else None

    if data.completed is not None:
        task.completed = data.completed

    # Set updated_at timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(
    session: AsyncSession, task_id: str, user_id: str
) -> bool:
    """
    Delete a task (ownership verified).

    Args:
        session: Database session
        task_id: Task ID to delete
        user_id: User ID (for ownership verification)

    Returns:
        True if deleted, False if task not found or user doesn't own it
    """
    # Get task with ownership check
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        return False

    await session.delete(task)
    await session.commit()

    return True
