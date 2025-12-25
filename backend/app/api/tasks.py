"""
Task API routes for CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Literal

from app.database import get_session
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service
from app.middleware.jwt_middleware import get_current_user
from app.models.user import User


router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    # Phase III: Query parameters for search, filter, sort
    search: Optional[str] = Query(None, max_length=500),
    status: Optional[Literal['pending', 'completed']] = Query(None),
    priority: Optional[Literal['high', 'medium', 'low']] = Query(None),
    due_date: Optional[str] = Query(None),
    sort_by: Optional[Literal['due_date', 'priority', 'title']] = Query(None),
    sort_order: Optional[Literal['asc', 'desc']] = Query('asc'),
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user with optional filtering, sorting, and search.

    Phase III Query Parameters:
        - search: Keyword search in title/description (case-insensitive, substring matching)
        - status: Filter by 'pending' or 'completed'
        - priority: Filter by 'high', 'medium', or 'low'
        - due_date: Filter by due date ('before:YYYY-MM-DD', 'after:YYYY-MM-DD', 'on:YYYY-MM-DD')
        - sort_by: Sort field ('due_date', 'priority', 'title')
        - sort_order: Sort direction ('asc' or 'desc', default 'asc')

    Args:
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        List of user's tasks (filtered, sorted, searched)

    Raises:
        HTTPException 400: If query parameters are invalid
        HTTPException 401: If not authenticated
        HTTPException 500: If server error occurs
    """
    try:
        tasks = await task_service.get_user_tasks_filtered(
            session=session,
            user_id=current_user.id,
            search=search,
            status=status,
            priority=priority,
            due_date=due_date,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return [
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at.isoformat(),
                updated_at=task.updated_at.isoformat() if task.updated_at else None,
                # Phase III: Advanced fields
                priority=task.priority,
                due_date=task.due_date.isoformat() if task.due_date else None,
                is_recurring=task.is_recurring,
                recurrence_pattern=task.recurrence_pattern,
                reminder_time=task.reminder_time.isoformat() if task.reminder_time else None,
            )
            for task in tasks
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tasks: {str(e)}",
        )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        data: Task creation data (title, description)
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        Created task

    Raises:
        HTTPException 400: If validation fails (empty title)
        HTTPException 401: If not authenticated
        HTTPException 500: If server error occurs
    """
    try:
        task = await task_service.create_task(session, current_user.id, data)
        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat() if task.updated_at else None,
            # Phase III: Advanced fields
            priority=task.priority,
            due_date=task.due_date.isoformat() if task.due_date else None,
            is_recurring=task.is_recurring,
            recurrence_pattern=task.recurrence_pattern,
            reminder_time=task.reminder_time.isoformat() if task.reminder_time else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}",
        )


@router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Update an existing task (ownership verified).

    Args:
        task_id: Task ID to update
        data: Task update data (title, description, completed)
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException 400: If validation fails
        HTTPException 401: If not authenticated
        HTTPException 403: If user doesn't own the task
        HTTPException 404: If task not found
        HTTPException 500: If server error occurs
    """
    try:
        task = await task_service.update_task(session, task_id, current_user.id, data)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat() if task.updated_at else None,
            # Phase III: Advanced fields
            priority=task.priority,
            due_date=task.due_date.isoformat() if task.due_date else None,
            is_recurring=task.is_recurring,
            recurrence_pattern=task.recurrence_pattern,
            reminder_time=task.reminder_time.isoformat() if task.reminder_time else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}",
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a task (ownership verified).

    Args:
        task_id: Task ID to delete
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        204 No Content on success

    Raises:
        HTTPException 401: If not authenticated
        HTTPException 404: If task not found or user doesn't own it
        HTTPException 500: If server error occurs
    """
    try:
        deleted = await task_service.delete_task(session, task_id, current_user.id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}",
        )
