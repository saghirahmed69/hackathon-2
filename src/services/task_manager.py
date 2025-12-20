"""Task management service with CRUD operations."""

from typing import Optional
from src.models.task import Task


class TaskManager:
    """Manages todo tasks with in-memory storage.

    Provides CRUD operations for tasks with automatic ID generation
    and validation.
    """

    def __init__(self) -> None:
        """Initialize empty task storage with ID counter."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> int:
        """Add a new task and return its ID.

        Args:
            title: Task title (required, must be non-empty)
            description: Optional task description (defaults to empty string)

        Returns:
            The unique ID assigned to the new task

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Validate title
        if not title.strip():
            raise ValueError("Title cannot be empty.")

        # Truncate if too long
        title = title[:1000]
        description = description[:5000]

        # Generate ID and create task
        task_id = self._next_id
        self._next_id += 1

        # Create and store task
        task = Task(
            id=task_id,
            title=title.strip(),
            description=description,
            completed=False
        )
        self._tasks[task_id] = task

        return task_id

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks.

        Returns:
            List of all Task objects (may be empty)
        """
        return list(self._tasks.values())

    def task_exists(self, task_id: int) -> bool:
        """Check if task ID exists.

        Args:
            task_id: Task ID to check

        Returns:
            True if task exists, False otherwise
        """
        return task_id in self._tasks

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> None:
        """Update task title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (None to keep current)
            description: New description (None to keep current)

        Raises:
            ValueError: If task_id doesn't exist or new title is empty
        """
        if not self.task_exists(task_id):
            raise ValueError(f"Task with ID {task_id} not found.")

        task = self._tasks[task_id]

        # Update title if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty.")
            task.title = title.strip()[:1000]

        # Update description if provided
        if description is not None:
            task.description = description[:5000]

    def delete_task(self, task_id: int) -> None:
        """Delete task by ID.

        Args:
            task_id: ID of task to delete

        Raises:
            ValueError: If task_id doesn't exist
        """
        if not self.task_exists(task_id):
            raise ValueError(f"Task with ID {task_id} not found.")

        del self._tasks[task_id]
        # Note: _next_id is NOT decremented to preserve ID stability

    def toggle_completion(self, task_id: int) -> bool:
        """Toggle task completion status and return new status.

        Args:
            task_id: ID of task to toggle

        Returns:
            The new completion status (True if now complete, False if now incomplete)

        Raises:
            ValueError: If task_id doesn't exist
        """
        if not self.task_exists(task_id):
            raise ValueError(f"Task with ID {task_id} not found.")

        task = self._tasks[task_id]
        task.completed = not task.completed
        return task.completed
