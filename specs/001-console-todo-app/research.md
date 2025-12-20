# Research & Technical Decisions: Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2025-12-19
**Status**: Complete

## Overview

This document captures all technical decisions and their rationale for the Phase I Console Todo Application implementation.

## Technology Stack Decisions

### 1. Programming Language

**Decision**: Python 3.13+

**Rationale**:
- Specified in project requirements
- Excellent standard library support for console I/O
- Simple, readable syntax aligns with clean code principles
- Native support for data structures (dict, list) for in-memory storage
- Cross-platform compatibility (Linux/macOS/Windows)

**Alternatives Considered**: None - language was specified in requirements

**Constitutional Alignment**: Principle III (Phase I Scope Discipline) - Python specified for Phase I

---

### 2. Dependencies

**Decision**: Python standard library only (no external packages)

**Rationale**:
- Constitutional requirement (FR-012)
- Standard library provides all needed functionality:
  - `dataclasses` for Task model
  - `typing` for type hints
  - Built-in `input()` and `print()` for console I/O
- Zero dependency complexity
- No installation or version management overhead
- Simplifies deployment and execution

**Alternatives Considered**:
- External packages (rejected per FR-012)
- Third-party CLI frameworks (rejected - unnecessary complexity)

**Constitutional Alignment**: Principle II (No Manual Coding), Principle III (Phase I Scope)

---

### 3. Data Storage

**Decision**: In-memory dictionary (dict) with integer keys

**Rationale**:
- Constitutional requirement (FR-007: in-memory only)
- Python dict provides O(1) lookup by task ID
- Native Python data structure (no external dependencies)
- Simple to implement and maintain
- Suitable for Phase I scale (<10k tasks)
- Automatic memory management via Python garbage collection

**Storage Structure**:
```python
tasks: dict[int, Task] = {}
next_id: int = 1
```

**Alternatives Considered**:
- List with linear search (rejected - O(n) lookup inefficient)
- File persistence (rejected per FR-007)
- Database (rejected per constitutional scope)

**Constitutional Alignment**: Principle III (Phase I Scope Discipline), Principle IV (Feature Completeness)

---

### 4. Architecture Pattern

**Decision**: Simple 3-layer modular architecture

**Layers**:
1. **Model Layer** (`models/task.py`) - Data structures
2. **Service Layer** (`services/task_manager.py`) - Business logic
3. **UI Layer** (`ui/console_ui.py`) - User interaction

**Rationale**:
- Clear separation of concerns (constitutional requirement)
- Single responsibility principle for each module
- Easy to test each layer independently
- Minimal complexity for Phase I scope
- Prepares for future phases (web UI can replace console UI)

**Alternatives Considered**:
- Single monolithic file (rejected - violates clean architecture principle)
- MVC pattern (rejected - unnecessary complexity for console app)
- Repository pattern (rejected - overkill for in-memory dict)

**Constitutional Alignment**: Principle VI (Clean Architecture), Principle VIII (Testability)

---

### 5. Task ID Generation

**Decision**: Sequential auto-incrementing integer starting at 1

**Rationale**:
- Simplest implementation (counter variable)
- User-friendly (IDs are small, predictable: 1, 2, 3...)
- Meets FR-002 requirement (unique numeric ID, sequential)
- IDs remain stable after deletion (FR-014)
- No collision risk (single user, single session)

**Implementation**:
```python
class TaskManager:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> int:
        task_id = self._next_id
        self._next_id += 1
        # ... create task
        return task_id
```

**Alternatives Considered**:
- UUID (rejected - unnecessarily complex, not user-friendly)
- Hash of task title (rejected - can collide, not sequential per FR-002)

**Constitutional Alignment**: FR-002, FR-014, Principle VI (Clean Architecture)

---

### 6. Error Handling Strategy

**Decision**: Explicit validation with user-friendly error messages

**Approach**:
- Validate all user inputs before processing
- Return clear error messages for invalid operations
- Never crash the application (graceful degradation)
- Always return user to main menu after errors

**Error Categories**:
1. **Invalid menu choice** - "Invalid option. Please enter 1-6."
2. **Invalid task ID** - "Task with ID {id} not found."
3. **Empty title** - "Title cannot be empty."
4. **Empty task list** - "No tasks found. Add a task to get started."

**Rationale**:
- Meets FR-010 and FR-011 requirements
- Predictable behavior (constitutional requirement)
- User can recover from all errors without restart
- Clear user feedback improves experience

**Constitutional Alignment**: Principle V (Deterministic Behavior), FR-010, FR-011

---

### 7. Console Interface Design

**Decision**: Numbered menu with simple integer input

**Menu Structure**:
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

**Rationale**:
- Simplest user interaction model
- Numeric input is easy to validate
- Clear option numbering
- Meets FR-008 requirement (clear menu)
- Familiar pattern for console applications

**Interaction Flow**:
1. Display menu
2. Get user choice
3. Execute operation (with sub-prompts as needed)
4. Display result/confirmation
5. Return to menu (loop until exit)

**Constitutional Alignment**: Principle VII (Explicit Interaction Contracts), FR-008, FR-009

---

### 8. Testing Strategy

**Decision**: Manual console verification against spec acceptance scenarios

**Approach**:
- No automated test framework in Phase I
- Manual test scenarios derived from spec acceptance criteria
- Test scenarios documented in `tests/manual/test_scenarios.md`
- Each functional requirement maps to test scenario

**Rationale**:
- Aligns with Phase I scope (no test framework required)
- Spec acceptance scenarios provide clear test cases
- Manual testing is deterministic (in-memory state is predictable)
- Prepares for automated testing in future phases

**Test Coverage**:
- All 4 user stories from spec
- All edge cases from spec
- All functional requirements (FR-001 to FR-014)

**Constitutional Alignment**: Principle VIII (Testability by Design), Phase I scope

---

## Best Practices Applied

### Python Code Quality

**Practices**:
1. Type hints on all functions (using `typing` module)
2. Dataclasses for Task model (simple, immutable-friendly)
3. Docstrings for all public functions
4. PEP 8 naming conventions (snake_case)
5. Clear, descriptive variable names
6. Single responsibility per function

**Rationale**: Constitutional requirement for clean, readable code (Principle VI)

---

### Function Design Principles

**Guidelines**:
- Each function does ONE thing
- Function names are verbs (add_task, update_task, display_menu)
- Parameters are validated before use
- Return values are explicit (not side-effect based)
- No global state mutation (encapsulated in TaskManager)

**Example**:
```python
def add_task(self, title: str, description: str = "") -> int:
    """Add a new task and return its ID."""
    if not title.strip():
        raise ValueError("Title cannot be empty")
    # ... rest of implementation
```

**Constitutional Alignment**: Principle VI (Clean Architecture)

---

### Data Flow Design

**Flow Pattern**: Unidirectional (UI → Service → Model)

```
User Input
    ↓
ConsoleUI (validate, parse)
    ↓
TaskManager (business logic)
    ↓
Task (data structure)
    ↓
TaskManager (return result)
    ↓
ConsoleUI (format, display)
    ↓
User Output
```

**Rationale**:
- Clear, predictable data flow
- Easy to trace execution
- Testable at each layer
- No circular dependencies

**Constitutional Alignment**: Principle VI (Clean Architecture), Principle VIII (Testability)

---

## Integration Patterns

Not applicable - Phase I has no external integrations (no database, no network, no files).

All data lives in memory for the session duration.

---

## Performance Considerations

### Expected Performance

**Operation Complexity**:
- Add task: O(1) - dict insertion
- View tasks: O(n) - iterate all tasks
- Update task: O(1) - dict lookup + update
- Delete task: O(1) - dict deletion
- Mark complete: O(1) - dict lookup + boolean toggle

**Memory Usage**: O(n) where n = number of tasks

**Assumptions**:
- Reasonable task limit: <10,000 tasks per session
- Task size: <1KB per task (title + description)
- Max memory: <10MB for application state

**Rationale**: All operations meet "interactive response" requirement (<1 second)

---

## Security & Validation

### Input Validation

**Validation Rules**:
1. **Menu choice**: Must be integer 1-6
2. **Task ID**: Must be valid integer, task must exist
3. **Task title**: Must not be empty or whitespace-only
4. **Task description**: Optional, any string (including empty)

**No Security Requirements**: Single-user, local execution, no authentication (FR-013)

---

## Decision Summary Table

| Decision Area | Choice | Rationale | Spec Reference |
|---------------|--------|-----------|----------------|
| Language | Python 3.13+ | Specified in requirements | User input |
| Dependencies | Stdlib only | No external packages allowed | FR-012 |
| Storage | In-memory dict | No persistence required | FR-007 |
| Architecture | 3-layer modular | Separation of concerns | Principle VI |
| ID Generation | Sequential int | Simple, user-friendly | FR-002, FR-014 |
| Error Handling | Explicit validation | Graceful degradation | FR-010, FR-011 |
| UI Pattern | Numbered menu | Simple, clear | FR-008 |
| Testing | Manual verification | Phase I scope | Principle VIII |

---

## Risks & Mitigations

### Risk 1: Python Version Compatibility

**Risk**: User may not have Python 3.13+ installed

**Mitigation**:
- Document minimum version in quickstart.md
- Use only features available since Python 3.10 (dataclasses, type hints)
- Verify version check not needed (Python 3.10+ is widely available)

**Likelihood**: Low
**Impact**: Low

---

### Risk 2: Large Task Volume Performance

**Risk**: Performance degrades with >10k tasks

**Mitigation**:
- Not a concern for Phase I (single user, single session)
- If needed, could add pagination to view_tasks
- Future phases will address with proper database

**Likelihood**: Very Low (Phase I scope)
**Impact**: Low (acceptable for console app)

---

### Risk 3: Data Loss on Exit

**Risk**: All tasks lost when application exits

**Mitigation**:
- Expected behavior per FR-007 (in-memory only)
- Documented in quickstart.md
- Future phases will add persistence

**Likelihood**: N/A (intended behavior)
**Impact**: N/A

---

## Next Steps

Phase 0 research is complete. All technical decisions documented and aligned with constitutional principles.

**Ready for Phase 1**:
1. Create `data-model.md` (Task entity specification)
2. Create `contracts/console-interface.md` (UI interaction contracts)
3. Create `quickstart.md` (User guide)
4. Update agent context with project technology stack

**No blockers or unresolved questions.**
