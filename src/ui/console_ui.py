"""Console user interface for the todo application."""

from typing import Optional
from src.services.task_manager import TaskManager


def display_menu() -> None:
    """Display the main menu with available options."""
    print("\n=== Todo Application ===\n")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")
    print()


def get_menu_choice() -> int:
    """Prompt for menu choice and validate input.

    Returns:
        Valid menu choice (1-6)

    Note:
        Handles invalid input by displaying error and re-prompting
    """
    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("✗ Error: Invalid choice. Please enter a number between 1 and 6.\n")
        except ValueError:
            print("✗ Error: Invalid choice. Please enter a number between 1 and 6.\n")
        except EOFError:
            print("\n\nApplication terminated. Goodbye!")
            raise SystemExit
        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            raise SystemExit


def handle_add_task(task_manager: TaskManager) -> None:
    """Handle adding a new task.

    Args:
        task_manager: TaskManager instance to add task to
    """
    try:
        title = input("Enter task title: ").strip()

        if not title:
            print("✗ Error: Title cannot be empty.\n")
            input("[Press Enter to continue]")
            return

        description = input("Enter task description (optional, press Enter to skip): ")

        task_id = task_manager.add_task(title, description)
        print(f"\n✓ Task added successfully! (ID: {task_id})\n")

    except ValueError as e:
        print(f"✗ Error: {e}\n")
    except EOFError:
        print("\n\nApplication terminated. Goodbye!")
        raise SystemExit
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        raise SystemExit

    input("[Press Enter to continue]")


def handle_view_tasks(task_manager: TaskManager) -> None:
    """Display all tasks with formatting.

    Args:
        task_manager: TaskManager instance to get tasks from
    """
    print("\n=== All Tasks ===\n")

    tasks = task_manager.get_all_tasks()

    if not tasks:
        print("No tasks found. Add a task to get started!\n")
    else:
        completed_count = sum(1 for task in tasks if task.completed)
        incomplete_count = len(tasks) - completed_count

        for task in tasks:
            status = "✓" if task.completed else " "
            desc = task.description if task.description else "(none)"
            print(f"[{status}] #{task.id}: {task.title}")
            print(f"    Description: {desc}\n")

        print(f"Total: {len(tasks)} tasks ({completed_count} completed, {incomplete_count} incomplete)\n")

    input("[Press Enter to continue]")


def handle_update_task(task_manager: TaskManager) -> None:
    """Handle updating a task's title and/or description.

    Args:
        task_manager: TaskManager instance
    """
    try:
        task_id_str = input("Enter task ID to update: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("✗ Error: Invalid task ID. Please enter a number.\n")
            input("[Press Enter to continue]")
            return

        if not task_manager.task_exists(task_id):
            print(f"✗ Error: Task with ID {task_id} not found.\n")
            input("[Press Enter to continue]")
            return

        # Get current task to display
        tasks = task_manager.get_all_tasks()
        current_task = next(t for t in tasks if t.id == task_id)

        print(f"Current title: {current_task.title}")
        new_title = input("Enter new title (or press Enter to keep current): ").strip()

        current_desc = current_task.description if current_task.description else "(none)"
        print(f"Current description: {current_desc}")
        new_description = input("Enter new description (or press Enter to keep current): ")

        # Update only if values were provided
        title_to_update = new_title if new_title else None
        desc_to_update = new_description if new_description or new_description == "" else None

        # Check for empty new title
        if title_to_update is not None and not title_to_update:
            print("✗ Error: Title cannot be empty. Task not updated.\n")
            input("[Press Enter to continue]")
            return

        task_manager.update_task(task_id, title_to_update, desc_to_update)
        print("\n✓ Task updated successfully!\n")

    except ValueError as e:
        print(f"✗ Error: {e}\n")
    except EOFError:
        print("\n\nApplication terminated. Goodbye!")
        raise SystemExit
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        raise SystemExit

    input("[Press Enter to continue]")


def handle_delete_task(task_manager: TaskManager) -> None:
    """Handle deleting a task.

    Args:
        task_manager: TaskManager instance
    """
    try:
        task_id_str = input("Enter task ID to delete: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("✗ Error: Invalid task ID. Please enter a number.\n")
            input("[Press Enter to continue]")
            return

        task_manager.delete_task(task_id)
        print("\n✓ Task deleted successfully!\n")

    except ValueError as e:
        print(f"✗ Error: {e}\n")
    except EOFError:
        print("\n\nApplication terminated. Goodbye!")
        raise SystemExit
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        raise SystemExit

    input("[Press Enter to continue]")


def handle_toggle_completion(task_manager: TaskManager) -> None:
    """Handle toggling task completion status.

    Args:
        task_manager: TaskManager instance
    """
    try:
        task_id_str = input("Enter task ID to toggle completion: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("✗ Error: Invalid task ID. Please enter a number.\n")
            input("[Press Enter to continue]")
            return

        new_status = task_manager.toggle_completion(task_id)

        if new_status:
            print("\n✓ Task marked as complete!\n")
        else:
            print("\n✓ Task marked as incomplete!\n")

    except ValueError as e:
        print(f"✗ Error: {e}\n")
    except EOFError:
        print("\n\nApplication terminated. Goodbye!")
        raise SystemExit
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        raise SystemExit

    input("[Press Enter to continue]")


def handle_exit() -> None:
    """Display exit message."""
    print("\nGoodbye! Your tasks will be lost when you exit.")
