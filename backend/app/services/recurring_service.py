"""
Recurring task service for handling task recurrence logic.

Implements automatic task instance generation when recurring tasks are completed.
"""

from datetime import datetime, timedelta
from typing import Optional
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


async def handle_task_completion(
    session: AsyncSession,
    task: Task,
) -> Optional[Task]:
    """
    When a recurring task is marked complete, create a new instance.

    This function is called from task_service.update_task() when a task's
    completed status transitions from False to True.

    Args:
        session: Database session
        task: The task that was just completed

    Returns:
        New task instance if task is recurring, None otherwise

    Behavior:
        - Only creates new instance if task.is_recurring is True
        - Calculates next due_date based on recurrence_pattern
        - Copies title, description, priority, recurrence settings
        - New instance starts as pending (completed=False)
        - If task has no due_date, new instance created immediately without date
        - Reminder time is also shifted by same offset as due_date
    """

    if not task.is_recurring:
        return None

    # Calculate new due date based on recurrence pattern
    new_due_date = calculate_next_due_date(task.due_date, task.recurrence_pattern)

    # Calculate new reminder time (shift by same offset)
    new_reminder_time = calculate_next_reminder(
        task.reminder_time, task.recurrence_pattern
    )

    # Create new task instance with same properties
    new_task = Task(
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=False,  # New instance starts as pending
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern,
        due_date=new_due_date,
        reminder_time=new_reminder_time,
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


def calculate_next_due_date(
    current_due_date: Optional[datetime],
    pattern: Optional[str],
) -> Optional[datetime]:
    """
    Calculate next due date based on recurrence pattern.

    Args:
        current_due_date: Current task due date
        pattern: Recurrence pattern ('daily', 'weekly', 'monthly')

    Returns:
        Next due date, or None if no due date or pattern

    Behavior:
        - daily: Add 1 day
        - weekly: Add 7 days
        - monthly: Add 1 month, handling month-end edge cases
            - If current day doesn't exist in next month, use last day of month
            - Example: Jan 31 -> Feb 28/29, then Mar 28/29 (not Mar 31)
        - No due date: Return None (new instance created immediately)
    """

    if not current_due_date or not pattern:
        return None

    if pattern == 'daily':
        return current_due_date + timedelta(days=1)
    elif pattern == 'weekly':
        return current_due_date + timedelta(weeks=1)
    elif pattern == 'monthly':
        # Handle month-end edge cases using dateutil.relativedelta
        try:
            # Try to add 1 month maintaining the same day
            return current_due_date + relativedelta(months=1)
        except (ValueError, OverflowError):
            # If day doesn't exist in next month, use last day of that month
            next_month = current_due_date + relativedelta(months=1, day=1)
            last_day = next_month + relativedelta(day=31)
            return last_day

    return None


def calculate_next_reminder(
    current_reminder: Optional[datetime],
    pattern: Optional[str],
) -> Optional[datetime]:
    """
    Shift reminder time by same offset as due date.

    Args:
        current_reminder: Current reminder timestamp
        pattern: Recurrence pattern ('daily', 'weekly', 'monthly')

    Returns:
        Next reminder time, or None if no reminder or pattern

    Behavior:
        - Applies same offset as calculate_next_due_date()
        - Ensures reminder time stays synchronized with due date
    """

    if not current_reminder or not pattern:
        return None

    if pattern == 'daily':
        return current_reminder + timedelta(days=1)
    elif pattern == 'weekly':
        return current_reminder + timedelta(weeks=1)
    elif pattern == 'monthly':
        # Handle month-end edge cases
        try:
            return current_reminder + relativedelta(months=1)
        except (ValueError, OverflowError):
            next_month = current_reminder + relativedelta(months=1, day=1)
            last_day = next_month + relativedelta(day=31)
            return last_day

    return None
