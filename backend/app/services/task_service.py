"""
Task service with CRUD operations and user isolation.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, case
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
        HTTPException 400: If validation fails (empty title, whitespace only, invalid priority, etc.)
    """
    # Validate title (not empty, not whitespace only)
    if not data.title or not data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty or whitespace",
        )

    # Phase III: Validate priority (FR-007)
    if data.priority not in ['high', 'medium', 'low']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid priority. Must be 'high', 'medium', or 'low'",
        )

    # Phase III: Validate due_date format (FR-017)
    parsed_due_date = None
    if data.due_date:
        try:
            parsed_due_date = datetime.fromisoformat(data.due_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid due_date format. Use ISO 8601 (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)",
            )

    # Phase III: Validate reminder_time is in future (FR-056)
    parsed_reminder_time = None
    if data.reminder_time:
        try:
            parsed_reminder_time = datetime.fromisoformat(data.reminder_time.replace('Z', '+00:00'))
            if parsed_reminder_time <= datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Reminder time must be in the future",
                )
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reminder_time format. Use ISO 8601",
            )

    # Create task with Phase II and Phase III fields
    task = Task(
        user_id=user_id,
        title=data.title.strip(),
        description=data.description.strip() if data.description else None,
        # Phase III Advanced Features
        priority=data.priority,
        due_date=parsed_due_date,
        is_recurring=data.is_recurring,
        recurrence_pattern=data.recurrence_pattern,
        reminder_time=parsed_reminder_time,
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
    # Import recurring service here to avoid circular imports
    from app.services.recurring_service import handle_task_completion

    # Get task with ownership check
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        return None

    # Track if task is being marked complete (for recurring logic)
    was_completed = task.completed
    is_being_completed = False

    # Update Phase II fields if provided
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
        is_being_completed = (not was_completed) and data.completed
        task.completed = data.completed

    # Update Phase III fields if provided
    if data.priority is not None:
        # Validate priority (FR-007)
        if data.priority not in ['high', 'medium', 'low']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid priority. Must be 'high', 'medium', or 'low'",
            )
        task.priority = data.priority

    if data.due_date is not None:
        # Validate due_date format (FR-017)
        if data.due_date:
            try:
                task.due_date = datetime.fromisoformat(data.due_date.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid due_date format. Use ISO 8601",
                )
        else:
            task.due_date = None

    if data.is_recurring is not None:
        task.is_recurring = data.is_recurring

    if data.recurrence_pattern is not None:
        task.recurrence_pattern = data.recurrence_pattern

    if data.reminder_time is not None:
        # Validate reminder_time is in future (FR-056)
        if data.reminder_time:
            try:
                parsed_reminder = datetime.fromisoformat(data.reminder_time.replace('Z', '+00:00'))
                if parsed_reminder <= datetime.utcnow():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Reminder time must be in the future",
                    )
                task.reminder_time = parsed_reminder
            except (ValueError, AttributeError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid reminder_time format. Use ISO 8601",
                )
        else:
            task.reminder_time = None

    # Set updated_at timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Phase III: Handle recurring task completion (FR-046)
    if is_being_completed and task.is_recurring:
        await handle_task_completion(session, task)

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


# Phase III: Advanced querying with search, filter, and sort
async def get_user_tasks_filtered(
    session: AsyncSession,
    user_id: str,
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = 'asc',
) -> List[Task]:
    """
    Get user tasks with filtering, sorting, and search (Phase III).

    Args:
        session: Database session
        user_id: User ID
        search: Keyword search in title/description (FR-018 to FR-025)
        status: Filter by 'pending' or 'completed' (FR-026)
        priority: Filter by 'high', 'medium', 'low' (FR-027)
        due_date: Filter by due date with operators (before:/after:/on:) (FR-028)
        sort_by: Sort field: 'due_date', 'priority', 'title' (FR-035)
        sort_order: Sort direction: 'asc' or 'desc' (FR-036, default 'asc')

    Returns:
        Filtered and sorted list of tasks
    """
    # Start with base query (always filter by user)
    query = select(Task).where(Task.user_id == user_id)

    # Apply search (FR-018 to FR-025)
    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.where(
            or_(
                Task.title.ilike(search_term),  # Case-insensitive
                Task.description.ilike(search_term)
            )
        )

    # Apply status filter (FR-026)
    if status == 'pending':
        query = query.where(Task.completed == False)
    elif status == 'completed':
        query = query.where(Task.completed == True)

    # Apply priority filter (FR-027)
    if priority:
        query = query.where(Task.priority == priority)

    # Apply due_date filter (FR-028)
    if due_date:
        operator, date_str = parse_due_date_filter(due_date)
        target_date = datetime.fromisoformat(date_str)

        if operator == 'before':
            query = query.where(Task.due_date < target_date)
        elif operator == 'after':
            query = query.where(Task.due_date > target_date)
        elif operator == 'on':
            query = query.where(func.date(Task.due_date) == target_date.date())

    # Apply sorting (FR-034 to FR-042)
    if sort_by == 'due_date':
        if sort_order == 'desc':
            query = query.order_by(Task.due_date.desc().nullsfirst())
        else:
            query = query.order_by(Task.due_date.asc().nullslast())
    elif sort_by == 'priority':
        # Custom priority ordering: high=1, medium=2, low=3
        priority_order = case(
            (Task.priority == 'high', 1),
            (Task.priority == 'medium', 2),
            (Task.priority == 'low', 3),
        )
        if sort_order == 'desc':
            query = query.order_by(priority_order.asc())  # high first when desc
        else:
            query = query.order_by(priority_order.desc())  # low first when asc
    elif sort_by == 'title':
        if sort_order == 'desc':
            query = query.order_by(Task.title.desc())
        else:
            query = query.order_by(Task.title.asc())
    else:
        # Default: order by created_at desc
        query = query.order_by(Task.created_at.desc())

    result = await session.execute(query)
    return list(result.scalars().all())


def parse_due_date_filter(filter_str: str) -> tuple:
    """
    Parse due_date filter string (FR-028).

    Format: 'before:YYYY-MM-DD', 'after:YYYY-MM-DD', 'on:YYYY-MM-DD'

    Returns:
        Tuple of (operator, date_string)

    Raises:
        HTTPException 400: If invalid format
    """
    if ':' not in filter_str:
        raise HTTPException(
            status_code=400,
            detail="Invalid due_date format. Use 'before:YYYY-MM-DD', 'after:YYYY-MM-DD', or 'on:YYYY-MM-DD'"
        )

    operator, date_str = filter_str.split(':', 1)
    if operator not in ['before', 'after', 'on']:
        raise HTTPException(
            status_code=400,
            detail="Invalid due_date operator. Use 'before', 'after', or 'on'"
        )

    try:
        datetime.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    return operator, date_str
