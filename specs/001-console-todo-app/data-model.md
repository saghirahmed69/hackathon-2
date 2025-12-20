# Data Model: Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2025-12-19
**Status**: Complete

## Overview

This document defines the data structures and storage model for the Phase I Console Todo Application. All data is stored in-memory only (no persistence).

---

## Entity: Task

### Description

Represents a single todo item with a unique identifier, descriptive content, and completion status.

### Attributes

| Attribute | Type | Required | Default | Constraints | Spec Reference |
|-----------|------|----------|---------|-------------|----------------|
| `id` | `int` | Yes | Auto-generated | Unique, positive integer, immutable | FR-002 |
| `title` | `str` | Yes | None | Non-empty, non-whitespace | FR-001 |
| `description` | `str` | No | Empty string `""` | Any string (including empty) | FR-001 |
| `completed` | `bool` | Yes | `False` | Boolean (True/False) | Key Entities |

### Field Details

#### `id` (Task ID)

- **Purpose**: Unique identifier for the task
- **Generation**: Auto-incrementing integer starting at 1
- **Immutability**: Cannot be changed after task creation
- **Stability**: Not reassigned when other tasks are deleted (FR-014)
- **Type**: Positive integer (1, 2, 3, ...)

#### `title` (Task Title)

- **Purpose**: Brief description of the task
- **Validation**:
  - Cannot be empty string
  - Cannot be whitespace-only
  - Length: 1-1000 characters (practical limit)
- **Examples**:
  - "Buy groceries"
  - "Call dentist"
  - "Complete project proposal"

#### `description` (Task Description)

- **Purpose**: Optional detailed information about the task
- **Validation**: Any string (including empty)
- **Default**: Empty string if not provided
- **Length**: 0-5000 characters (practical limit)
- **Examples**:
  - "" (empty - no description)
  - "milk, eggs, bread"
  - "Schedule appointment for teeth cleaning on Tuesday"

#### `completed` (Completion Status)

- **Purpose**: Tracks whether task is done
- **Values**:
  - `False`: Task is incomplete (default)
  - `True`: Task is complete
- **Toggleable**: Can be changed from False→True and True→False (FR-006)

---

## Data Structures

### In-Memory Storage

**Primary Storage**: Dictionary (hash map) mapping task IDs to Task objects

```python
# Storage structure
tasks: dict[int, Task] = {}
```

**ID Generator**: Integer counter for next available ID

```python
next_id: int = 1  # Starts at 1, increments after each task creation
```

### Example State

```python
# After adding 3 tasks:
tasks = {
    1: Task(id=1, title="Buy groceries", description="milk, eggs, bread", completed=False),
    2: Task(id=2, title="Call dentist", description="", completed=True),
    3: Task(id=3, title="Finish report", description="Quarterly sales analysis", completed=False)
}
next_id = 4  # Next task will get ID 4
```

### After Deletion

```python
# After deleting task ID 2:
tasks = {
    1: Task(id=1, title="Buy groceries", description="milk, eggs, bread", completed=False),
    3: Task(id=3, title="Finish report", description="Quarterly sales analysis", completed=False)
}
next_id = 4  # ID 2 is NOT reused (FR-014)
```

---

## Data Operations

### Create (Add Task)

**Input**:
- `title` (required, non-empty string)
- `description` (optional, defaults to empty string)

**Process**:
1. Validate title is non-empty
2. Generate new ID from `next_id`
3. Increment `next_id`
4. Create Task object with ID, title, description, completed=False
5. Store in `tasks` dict with ID as key

**Output**: Task ID (integer)

**Spec Reference**: FR-001, FR-002

---

### Read (View Tasks)

**Input**: None (retrieves all tasks)

**Process**:
1. Retrieve all Task objects from `tasks` dict
2. Return as list or iterate for display

**Output**: Collection of all Task objects

**Spec Reference**: FR-003

---

### Update (Modify Task)

**Input**:
- `task_id` (required, must exist)
- `new_title` (optional, updates title if provided)
- `new_description` (optional, updates description if provided)

**Process**:
1. Validate task_id exists in `tasks`
2. Retrieve Task object
3. Update title if new_title provided (validate non-empty)
4. Update description if new_description provided
5. Store updated Task back to `tasks`

**Output**: Success confirmation or error

**Spec Reference**: FR-004

---

### Delete (Remove Task)

**Input**: `task_id` (required, must exist)

**Process**:
1. Validate task_id exists in `tasks`
2. Remove entry from `tasks` dict
3. Do NOT decrement `next_id` (preserve ID stability)

**Output**: Success confirmation or error

**Spec Reference**: FR-005, FR-014

---

### Toggle Completion (Mark Complete/Incomplete)

**Input**: `task_id` (required, must exist)

**Process**:
1. Validate task_id exists in `tasks`
2. Retrieve Task object
3. Toggle `completed` field (False→True or True→False)
4. Store updated Task back to `tasks`

**Output**: Success confirmation with new status or error

**Spec Reference**: FR-006

---

## Data Validation Rules

### On Task Creation

| Field | Rule | Error Message |
|-------|------|---------------|
| `title` | Not empty | "Title cannot be empty." |
| `title` | Not whitespace-only | "Title cannot be empty." |
| `description` | (No validation) | N/A |

### On Task Update

| Field | Rule | Error Message |
|-------|------|---------------|
| `task_id` | Must exist in tasks | "Task with ID {id} not found." |
| `new_title` | If provided, not empty | "Title cannot be empty." |
| `new_title` | If provided, not whitespace-only | "Title cannot be empty." |
| `new_description` | (No validation) | N/A |

### On Task Deletion

| Field | Rule | Error Message |
|-------|------|---------------|
| `task_id` | Must exist in tasks | "Task with ID {id} not found." |

### On Toggle Completion

| Field | Rule | Error Message |
|-------|------|---------------|
| `task_id` | Must exist in tasks | "Task with ID {id} not found." |

---

## Data Lifecycle

### Task Lifecycle States

```
[Created] --→ [Incomplete] ⟷ [Complete]
                               ↓
                          [Deleted]
```

**State Transitions**:
1. **Created**: Task added with `completed=False`
2. **Incomplete→Complete**: User marks task as done
3. **Complete→Incomplete**: User unmarks task (corrects mistake)
4. **Deleted**: Task removed from storage (any state)

### Session Lifecycle

```
[Application Start]
        ↓
  Initialize empty storage
  (tasks = {}, next_id = 1)
        ↓
  [User Operations]
  (Add, View, Update, Delete, Toggle)
        ↓
  [Application Exit]
        ↓
  All data lost (in-memory only)
```

**Important**: All tasks are lost when application exits (FR-007 - no persistence)

---

## Python Implementation Reference

### Task Dataclass (models/task.py)

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __str__(self) -> str:
        """String representation for display."""
        status = "✓" if self.completed else " "
        return f"[{status}] #{self.id}: {self.title}"
```

### TaskManager Storage (services/task_manager.py)

```python
class TaskManager:
    """Manages todo tasks with in-memory storage."""

    def __init__(self):
        """Initialize empty task storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> int:
        """Add a new task and return its ID."""
        # Implementation here
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks."""
        # Implementation here
        pass

    def update_task(self, task_id: int, title: str = None, description: str = None) -> None:
        """Update task title and/or description."""
        # Implementation here
        pass

    def delete_task(self, task_id: int) -> None:
        """Delete task by ID."""
        # Implementation here
        pass

    def toggle_completion(self, task_id: int) -> bool:
        """Toggle task completion status and return new status."""
        # Implementation here
        pass

    def task_exists(self, task_id: int) -> bool:
        """Check if task ID exists."""
        return task_id in self._tasks
```

---

## Constraints & Invariants

### Invariants (Must Always Be True)

1. **ID Uniqueness**: No two tasks can have the same ID
2. **ID Immutability**: Task ID never changes after creation
3. **ID Sequential**: IDs are assigned sequentially (1, 2, 3, ...)
4. **ID Stability**: Deleted IDs are never reused within a session
5. **Title Required**: Every task has a non-empty title
6. **Description Optional**: Description can be empty string
7. **Boolean Status**: `completed` is always True or False (never None)

### Practical Limits

- **Max Tasks**: ~10,000 tasks per session (memory constraint)
- **Title Length**: 1-1000 characters
- **Description Length**: 0-5000 characters
- **ID Range**: 1 to 2,147,483,647 (Python int max - practically unlimited)

---

## Spec Compliance Matrix

| Requirement | Data Model Implementation |
|-------------|---------------------------|
| FR-001: Add task with title and optional description | Task has `title` (required) and `description` (optional, default "") |
| FR-002: Unique numeric ID, auto-generated, sequential | `id` field, auto-incremented via `next_id` counter |
| FR-003: View tasks with ID, title, description, status | All fields present in Task entity |
| FR-004: Update title or description | Task fields are mutable (except `id`) |
| FR-005: Delete task by ID | Task can be removed from `tasks` dict |
| FR-006: Mark complete/incomplete | `completed` boolean field, toggleable |
| FR-007: In-memory storage only | `dict[int, Task]` - no persistence |
| FR-014: Stable IDs (not reassigned) | `next_id` only increments, never reused |

---

## Testing Considerations

### Testable Properties

1. **ID Generation**: Each add_task increments ID
2. **ID Stability**: After delete, next add_task uses next sequential ID (not deleted ID)
3. **Title Validation**: Empty title raises error
4. **Default Values**: New task has `completed=False` and `description=""`
5. **Toggle Logic**: Completed False→True→False works correctly

### Test Scenarios (from Spec)

| Scenario | Data Operation | Expected Result |
|----------|----------------|-----------------|
| Add task with description | Create("Buy groceries", "milk, eggs") | Task ID 1 created |
| Add task without description | Create("Call dentist", "") | Task ID 2 created |
| View empty list | Read() with tasks={} | Empty list returned |
| View multiple tasks | Read() with 3 tasks | All 3 tasks returned |
| Update title | Update(task_id=1, title="New title") | Task 1 title changed |
| Update description | Update(task_id=1, description="New desc") | Task 1 description changed |
| Delete task | Delete(task_id=2) | Task 2 removed, IDs 1 and 3 remain |
| Mark complete | Toggle(task_id=1) | Task 1 completed=True |
| Mark incomplete | Toggle(task_id=1) when completed=True | Task 1 completed=False |
| Invalid ID | Any operation with task_id=999 | Error: "Task not found" |

---

## Summary

The data model is simple, focused, and complete for Phase I requirements:

- **Single Entity**: Task (id, title, description, completed)
- **Simple Storage**: Dict mapping ID to Task
- **Sequential IDs**: Auto-incrementing counter
- **No Persistence**: All data in-memory only
- **Full CRUD Support**: Create, Read, Update, Delete operations
- **Validation**: Title required, ID must exist
- **Deterministic**: Predictable behavior for all operations

Ready for implementation via `/sp.tasks` and `/sp.implement`.
