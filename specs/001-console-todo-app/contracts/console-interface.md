# Console Interface Contract

**Feature**: 001-console-todo-app
**Date**: 2025-12-19
**Status**: Complete

## Overview

This document defines the exact console interface contract for the Phase I Todo Application. It specifies all user interactions, prompts, inputs, outputs, and error messages.

---

## Main Menu

### Display Format

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

### Input Specification

- **Prompt**: `Enter your choice (1-6): `
- **Expected Input**: Single integer from 1 to 6
- **Validation**:
  - Accept integers 1-6 only
  - Reject non-numeric input
  - Reject numbers outside 1-6 range

### Error Handling

**Invalid Input Examples**:
- `abc` → "Invalid choice. Please enter a number between 1 and 6."
- `7` → "Invalid choice. Please enter a number between 1 and 6."
- `0` → "Invalid choice. Please enter a number between 1 and 6."
- `` (empty) → "Invalid choice. Please enter a number between 1 and 6."

**After Error**: Redisplay menu and prompt again

---

## Operation 1: Add Task

### Interaction Flow

```
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): milk, eggs, bread

✓ Task added successfully! (ID: 1)

[Press Enter to continue]
```

### Prompts & Inputs

1. **Title Prompt**: `Enter task title: `
   - Input: Any non-empty string
   - Validation: Cannot be empty or whitespace-only

2. **Description Prompt**: `Enter task description (optional, press Enter to skip): `
   - Input: Any string (including empty)
   - Validation: None (empty is allowed)

### Success Message

```
✓ Task added successfully! (ID: {task_id})
```

### Error Messages

**Empty Title**:
```
Enter task title:
✗ Error: Title cannot be empty.

[Press Enter to continue]
```

**Whitespace-Only Title**:
```
Enter task title:
✗ Error: Title cannot be empty.

[Press Enter to continue]
```

### Spec Reference

FR-001, FR-002, User Story 1

---

## Operation 2: View All Tasks

### Empty List Display

```
=== All Tasks ===

No tasks found. Add a task to get started!

[Press Enter to continue]
```

### Tasks Display Format

```
=== All Tasks ===

[ ] #1: Buy groceries
    Description: milk, eggs, bread

[✓] #2: Call dentist
    Description: (none)

[ ] #3: Finish report
    Description: Quarterly sales analysis

Total: 3 tasks (1 completed, 2 incomplete)

[Press Enter to continue]
```

### Display Rules

**Task Entry Format**:
```
[{status}] #{id}: {title}
    Description: {description or "(none)"}
```

**Status Symbols**:
- `[ ]` = Incomplete task (completed=False)
- `[✓]` = Complete task (completed=True)

**Description Display**:
- If description is empty: show `(none)`
- If description has content: show the description

**Summary Line**:
```
Total: {count} tasks ({completed_count} completed, {incomplete_count} incomplete)
```

### Spec Reference

FR-003, User Story 1

---

## Operation 3: Update Task

### Interaction Flow (Update Title)

```
Enter task ID to update: 1
Current title: Buy groceries
Enter new title (or press Enter to keep current): Buy groceries and supplies
Current description: milk, eggs, bread
Enter new description (or press Enter to keep current):

✓ Task updated successfully!

[Press Enter to continue]
```

### Interaction Flow (Keep Both)

```
Enter task ID to update: 2
Current title: Call dentist
Enter new title (or press Enter to keep current):
Current description: (none)
Enter new description (or press Enter to keep current):

✓ Task updated successfully!

[Press Enter to continue]
```

### Prompts & Inputs

1. **ID Prompt**: `Enter task ID to update: `
   - Input: Integer task ID
   - Validation: Must exist in tasks

2. **Title Display**: `Current title: {current_title}`

3. **Title Update Prompt**: `Enter new title (or press Enter to keep current): `
   - Input: String (empty to skip)
   - Validation: If provided, cannot be empty/whitespace

4. **Description Display**: `Current description: {current_description or "(none)"}`

5. **Description Update Prompt**: `Enter new description (or press Enter to keep current): `
   - Input: String (empty to skip)
   - Validation: None

### Success Message

```
✓ Task updated successfully!
```

### Error Messages

**Invalid Task ID**:
```
Enter task ID to update: 999
✗ Error: Task with ID 999 not found.

[Press Enter to continue]
```

**Non-Numeric ID**:
```
Enter task ID to update: abc
✗ Error: Invalid task ID. Please enter a number.

[Press Enter to continue]
```

**Empty New Title**:
```
Enter new title (or press Enter to keep current):
✗ Error: Title cannot be empty. Task not updated.

[Press Enter to continue]
```

### Spec Reference

FR-004, User Story 3

---

## Operation 4: Delete Task

### Interaction Flow

```
Enter task ID to delete: 2

✓ Task deleted successfully!

[Press Enter to continue]
```

### Prompts & Inputs

1. **ID Prompt**: `Enter task ID to delete: `
   - Input: Integer task ID
   - Validation: Must exist in tasks

### Success Message

```
✓ Task deleted successfully!
```

### Error Messages

**Invalid Task ID**:
```
Enter task ID to delete: 999
✗ Error: Task with ID 999 not found.

[Press Enter to continue]
```

**Non-Numeric ID**:
```
Enter task ID to delete: abc
✗ Error: Invalid task ID. Please enter a number.

[Press Enter to continue]
```

### Spec Reference

FR-005, FR-014, User Story 4

---

## Operation 5: Mark Task Complete/Incomplete

### Interaction Flow (Mark Complete)

```
Enter task ID to toggle completion: 1

✓ Task marked as complete!

[Press Enter to continue]
```

### Interaction Flow (Mark Incomplete)

```
Enter task ID to toggle completion: 1

✓ Task marked as incomplete!

[Press Enter to continue]
```

### Prompts & Inputs

1. **ID Prompt**: `Enter task ID to toggle completion: `
   - Input: Integer task ID
   - Validation: Must exist in tasks

### Success Messages

**Marked Complete** (was incomplete):
```
✓ Task marked as complete!
```

**Marked Incomplete** (was complete):
```
✓ Task marked as incomplete!
```

### Error Messages

**Invalid Task ID**:
```
Enter task ID to toggle completion: 999
✗ Error: Task with ID 999 not found.

[Press Enter to continue]
```

**Non-Numeric ID**:
```
Enter task ID to toggle completion: abc
✗ Error: Invalid task ID. Please enter a number.

[Press Enter to continue]
```

### Spec Reference

FR-006, User Story 2

---

## Operation 6: Exit

### Interaction Flow

```
Goodbye! Your tasks will be lost when you exit.
```

### Exit Message

```
Goodbye! Your tasks will be lost when you exit.
```

### Behavior

- Display exit message
- Terminate application
- All tasks are lost (in-memory only, no persistence)

### Spec Reference

FR-007, FR-009

---

## General Interface Rules

### Continuation Prompt

After every operation (except Exit), display:
```
[Press Enter to continue]
```

Then wait for Enter keypress before returning to main menu.

### Error Message Format

All error messages follow this pattern:
```
✗ Error: {specific error message}

[Press Enter to continue]
```

### Success Message Format

All success messages follow this pattern:
```
✓ {specific success message}

[Press Enter to continue]
```

### Input Handling

**Leading/Trailing Whitespace**:
- Strip whitespace from all text inputs (except description content)
- Example: `"  Buy milk  "` → `"Buy milk"`

**Case Sensitivity**:
- Task titles and descriptions are case-sensitive
- Menu choices are numeric (no case issues)

**Empty Input**:
- Empty title → Error
- Empty description → Allowed (stored as empty string)
- Empty menu choice → Error
- Empty in update prompts → Keep current value

---

## Edge Case Handling

### Keyboard Interrupt (Ctrl+C)

```
^C
Application interrupted. Goodbye!
```

### EOF Signal (Ctrl+D)

```
^D
Application terminated. Goodbye!
```

### Very Long Input

**Title > 1000 characters**:
- Accept but truncate to 1000 characters
- No error message (silent truncation)

**Description > 5000 characters**:
- Accept but truncate to 5000 characters
- No error message (silent truncation)

### Special Characters

All special characters are allowed in title and description:
- Emojis: ✓ (allowed)
- Unicode: ✓ (allowed)
- Newlines in input: Treated as single line (input() limitation)

---

## Complete Example Session

```
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

Enter your choice (1-6): 2

=== All Tasks ===

[ ] #1: Buy groceries
    Description: milk, eggs, bread

Total: 1 tasks (0 completed, 1 incomplete)

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

Total: 1 tasks (1 completed, 0 incomplete)

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

## Spec Compliance Matrix

| Requirement | Interface Implementation |
|-------------|-------------------------|
| FR-008: Clear menu | Numbered menu with 6 clear options |
| FR-009: Loop until exit | Menu redisplays after each operation |
| FR-010: Handle invalid inputs | All input types validated with error messages |
| FR-011: User-friendly errors | Descriptive error messages with ✗ symbol |
| SC-001: Add task <10 seconds | Simple 2-prompt flow |
| SC-002: All details displayed | Task list shows ID, title, description, status |
| SC-004: Clear error messages | All errors have specific, helpful messages |

---

## Implementation Notes

### Console Clearing

**Not Required**: Do not clear console between operations. Let output scroll naturally.

**Rationale**: Allows users to see history of operations and review previous outputs.

### Input Parsing

**Integer Inputs** (menu choice, task ID):
```python
try:
    choice = int(input("Enter your choice (1-6): "))
except ValueError:
    print("✗ Error: Invalid choice. Please enter a number between 1 and 6.")
```

**String Inputs** (title, description):
```python
title = input("Enter task title: ").strip()
if not title:
    print("✗ Error: Title cannot be empty.")
```

### Pause for Continue

```python
input("\n[Press Enter to continue]")
```

---

## Summary

The console interface contract is complete and deterministic. Every user interaction is specified with exact prompts, validations, success messages, and error messages. This contract ensures:

- **Predictable Behavior**: Same input always produces same output
- **User-Friendly**: Clear prompts and helpful error messages
- **Spec Compliant**: All FR requirements met
- **Testable**: Every scenario can be manually verified

Ready for implementation via `/sp.tasks` and `/sp.implement`.
