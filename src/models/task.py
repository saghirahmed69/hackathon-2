"""Task data model for the console todo application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique numeric identifier (auto-generated, immutable)
        title: Task title (required, non-empty)
        description: Optional detailed description (defaults to empty string)
        completed: Boolean completion status (defaults to False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __str__(self) -> str:
        """String representation for display.

        Returns:
            Formatted string with status symbol, ID, and title
        """
        status = "✓" if self.completed else " "
        return f"[{status}] #{self.id}: {self.title}"
