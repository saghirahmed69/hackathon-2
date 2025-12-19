# Quickstart Guide: Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2025-12-19
**Status**: Complete

## Overview

This guide shows you how to run and use the Phase I Console Todo Application. The application is a simple, in-memory task manager that runs in your terminal.

---

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python Version**: Python 3.10 or higher (tested with Python 3.13)
- **No External Dependencies**: Uses Python standard library only

### Check Python Version

```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.10.x` or higher

---

## Installation

### Option 1: Clone Repository

```bash
git clone <repository-url>
cd hackathon-2
git checkout 001-console-todo-app
```

### Option 2: From Source Files

Ensure you have the following directory structure:

```
hackathon-2/
├── src/
│   ├── models/
│   │   └── task.py
│   ├── services/
│   │   └── task_manager.py
│   ├── ui/
│   │   └── console_ui.py
│   └── main.py
```

---

## Running the Application

### Quick Start

From the project root directory:

```bash
python src/main.py
# or
python3 src/main.py
```

### Expected Output

```
=== Todo Application ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

---

## Usage Guide

### Basic Operations

#### 1. Add a Task

**Steps**:
1. Select option `1` from menu
2. Enter task title (required)
3. Enter description (optional - press Enter to skip)

**Example**:
```
Enter your choice (1-6): 1
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): milk, eggs, bread

✓ Task added successfully! (ID: 1)

[Press Enter to continue]
```

---

#### 2. View All Tasks

**Steps**:
1. Select option `2` from menu
2. View your task list

**Example (with tasks)**:
```
Enter your choice (1-6): 2

=== All Tasks ===

[ ] #1: Buy groceries
    Description: milk, eggs, bread

[✓] #2: Call dentist
    Description: (none)

Total: 2 tasks (1 completed, 1 incomplete)

[Press Enter to continue]
```

**Example (empty list)**:
```
Enter your choice (1-6): 2

=== All Tasks ===

No tasks found. Add a task to get started!

[Press Enter to continue]
```

---

#### 3. Update a Task

**Steps**:
1. Select option `3` from menu
2. Enter task ID to update
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

**Example**:
```
Enter your choice (1-6): 3
Enter task ID to update: 1
Current title: Buy groceries
Enter new title (or press Enter to keep current): Buy groceries and supplies
Current description: milk, eggs, bread
Enter new description (or press Enter to keep current): milk, eggs, bread, coffee

✓ Task updated successfully!

[Press Enter to continue]
```

---

#### 4. Delete a Task

**Steps**:
1. Select option `4` from menu
2. Enter task ID to delete

**Example**:
```
Enter your choice (1-6): 4
Enter task ID to delete: 2

✓ Task deleted successfully!

[Press Enter to continue]
```

---

#### 5. Mark Task Complete/Incomplete

**Steps**:
1. Select option `5` from menu
2. Enter task ID to toggle

**Example (mark complete)**:
```
Enter your choice (1-6): 5
Enter task ID to toggle completion: 1

✓ Task marked as complete!

[Press Enter to continue]
```

**Example (mark incomplete)**:
```
Enter your choice (1-6): 5
Enter task ID to toggle completion: 1

✓ Task marked as incomplete!

[Press Enter to continue]
```

**Note**: This operation toggles the status. If task is complete, it becomes incomplete, and vice versa.

---

#### 6. Exit Application

**Steps**:
1. Select option `6` from menu

**Example**:
```
Enter your choice (1-6): 6

Goodbye! Your tasks will be lost when you exit.
```

**Important**: All tasks are stored in memory only. When you exit, all data is lost.

---

## Common Workflows

### Workflow 1: Create Your First Todo List

```
1. Run application → python src/main.py
2. Add task → Option 1 → "Buy groceries" → "milk, eggs"
3. Add task → Option 1 → "Call dentist" → (skip description)
4. Add task → Option 1 → "Finish report" → "Quarterly sales"
5. View tasks → Option 2 → See all 3 tasks
6. Exit → Option 6
```

### Workflow 2: Complete Tasks as You Work

```
1. Run application
2. Add several tasks (Option 1)
3. View tasks (Option 2) → See which tasks to do
4. Complete first task → Option 5 → ID 1
5. View tasks (Option 2) → See task 1 is now marked complete [✓]
6. Continue working...
7. Exit when done (Option 6)
```

### Workflow 3: Update Task Details

```
1. Run application
2. Add task with minimal info → "Buy milk" → (no description)
3. Realize you need more → Option 3 → ID 1
4. Update title → "Buy groceries"
5. Add description → "milk, eggs, bread, coffee"
6. View updated task → Option 2
```

---

## Error Handling

### Common Errors and Solutions

#### Error: Invalid Menu Choice

**Error Message**: `Invalid choice. Please enter a number between 1 and 6.`

**Cause**: Entered a non-numeric value or number outside 1-6

**Solution**: Enter a valid number from 1 to 6

**Example**:
```
Enter your choice (1-6): abc
✗ Error: Invalid choice. Please enter a number between 1 and 6.
```

---

#### Error: Task Not Found

**Error Message**: `Task with ID {id} not found.`

**Cause**: Entered a task ID that doesn't exist

**Solution**: View all tasks (Option 2) to see valid IDs, then try again

**Example**:
```
Enter task ID to delete: 999
✗ Error: Task with ID 999 not found.
```

---

#### Error: Empty Title

**Error Message**: `Title cannot be empty.`

**Cause**: Pressed Enter without typing a title

**Solution**: Enter a non-empty task title

**Example**:
```
Enter task title:
✗ Error: Title cannot be empty.
```

---

### Graceful Exit

**Keyboard Interrupt (Ctrl+C)**:
```
^C
Application interrupted. Goodbye!
```

**EOF Signal (Ctrl+D / Ctrl+Z)**:
```
^D
Application terminated. Goodbye!
```

Both methods safely exit the application.

---

## Important Notes

### Data Persistence

**⚠️ No Data Persistence**: All tasks are stored in memory only.

- Tasks are **lost when you exit** the application
- Tasks are **lost if application crashes**
- Tasks are **not saved to disk**

**This is intentional for Phase I**. Future phases will add persistence.

---

### Task ID Behavior

**Task IDs are Stable**:
- IDs start at 1 and increment (1, 2, 3, ...)
- Deleted task IDs are **not reused** during the session
- If you delete task 2, the next task created will be ID 4 (not 2)

**Example**:
```
1. Add task → ID 1
2. Add task → ID 2
3. Add task → ID 3
4. Delete task 2
5. Add task → ID 4 (not 2!)
```

This ensures IDs remain stable and references don't break.

---

### Input Guidelines

**Task Titles**:
- Required (cannot be empty)
- Can contain any characters (letters, numbers, symbols, emojis)
- Length: 1-1000 characters (very long titles are truncated)

**Task Descriptions**:
- Optional (can be empty)
- Can contain any characters
- Length: 0-5000 characters (very long descriptions are truncated)

**Task IDs**:
- Must be positive integers
- Must exist in the task list

---

## Troubleshooting

### Application Won't Start

**Problem**: `python src/main.py` gives error

**Solutions**:
1. Check Python version: `python --version` (need 3.10+)
2. Try `python3 src/main.py` instead
3. Ensure you're in the project root directory
4. Check that `src/main.py` exists

---

### "ModuleNotFoundError"

**Problem**: `ModuleNotFoundError: No module named 'models'`

**Solutions**:
1. Run from project root directory (not from `src/`)
2. Ensure directory structure is correct (see Installation section)
3. Check all files exist: `task.py`, `task_manager.py`, `console_ui.py`, `main.py`

---

### Unicode Display Issues

**Problem**: Checkmarks (✓) or symbols don't display

**Solution**:
- This is a terminal encoding issue (cosmetic only)
- Application still works correctly
- Try a different terminal emulator if needed

---

## Complete Example Session

Here's a full example session showing all operations:

```bash
$ python src/main.py

=== Todo Application ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6): 1
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): milk, eggs, bread

✓ Task added successfully! (ID: 1)

[Press Enter to continue]

=== Todo Application ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6): 1
Enter task title: Call dentist
Enter task description (optional, press Enter to skip):

✓ Task added successfully! (ID: 2)

[Press Enter to continue]

=== Todo Application ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6): 2

=== All Tasks ===

[ ] #1: Buy groceries
    Description: milk, eggs, bread

[ ] #2: Call dentist
    Description: (none)

Total: 2 tasks (0 completed, 2 incomplete)

[Press Enter to continue]

=== Todo Application ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6): 5
Enter task ID to toggle completion: 1

✓ Task marked as complete!

[Press Enter to continue]

=== Todo Application ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6): 2

=== All Tasks ===

[✓] #1: Buy groceries
    Description: milk, eggs, bread

[ ] #2: Call dentist
    Description: (none)

Total: 2 tasks (1 completed, 1 incomplete)

[Press Enter to continue]

=== Todo Application ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6): 6

Goodbye! Your tasks will be lost when you exit.
```

---

## Next Steps

After running the application:

1. **Test All Features**: Try each menu option to familiarize yourself
2. **Review Spec**: See `spec.md` for detailed requirements
3. **Check Data Model**: See `data-model.md` for task structure
4. **Read Interface Contract**: See `contracts/console-interface.md` for complete UI specification

---

## Support

### Documentation

- **Feature Spec**: `specs/001-console-todo-app/spec.md`
- **Implementation Plan**: `specs/001-console-todo-app/plan.md`
- **Data Model**: `specs/001-console-todo-app/data-model.md`
- **Console Interface**: `specs/001-console-todo-app/contracts/console-interface.md`

### Known Limitations (Phase I)

- No data persistence (intentional)
- No search or filter functionality
- No task priorities or categories
- No multi-user support
- No authentication
- No web interface
- No AI features

These limitations are by design for Phase I. Future phases will add these features.

---

## Summary

**Getting Started**:
1. Ensure Python 3.10+ installed
2. Navigate to project root
3. Run `python src/main.py`

**Core Operations**:
- Add tasks with title and optional description
- View all tasks with completion status
- Update task details
- Delete tasks
- Mark tasks complete/incomplete
- Exit application

**Remember**:
- All data is in-memory only (lost on exit)
- Task IDs are stable (not reused after deletion)
- All operations provide clear feedback

Enjoy using the Todo Application! 🎯
