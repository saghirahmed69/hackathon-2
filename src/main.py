"""Main entry point for the console todo application."""

from src.services.task_manager import TaskManager
from src.ui.console_ui import (
    display_menu,
    get_menu_choice,
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_toggle_completion,
    handle_exit
)


def main() -> None:
    """Run the main application loop."""
    task_manager = TaskManager()

    try:
        while True:
            display_menu()
            choice = get_menu_choice()

            if choice == 1:
                handle_add_task(task_manager)
            elif choice == 2:
                handle_view_tasks(task_manager)
            elif choice == 3:
                handle_update_task(task_manager)
            elif choice == 4:
                handle_delete_task(task_manager)
            elif choice == 5:
                handle_toggle_completion(task_manager)
            elif choice == 6:
                handle_exit()
                break

    except (EOFError, KeyboardInterrupt):
        # Already handled in UI functions
        pass


if __name__ == "__main__":
    main()
