# Tasks: Console-Based Todo Application (Phase I)

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/console-interface.md

**Tests**: Manual verification only (no automated test framework in Phase I)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Single project structure at repository root:
- Source code: `src/`
- Manual tests: `tests/manual/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and initialize Python environment

- [x] T001 Create source directory structure (src/models/, src/services/, src/ui/)
- [x] T002 Create tests directory structure (tests/manual/)
- [x] T003 [P] Create manual test scenarios document in tests/manual/test_scenarios.md from spec acceptance criteria

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Core Infrastructure)

**Purpose**: Implement foundational Task model that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement Task dataclass in src/models/task.py with id, title, description, completed fields
- [x] T005 Implement TaskManager class skeleton in src/services/task_manager.py with __init__, _tasks dict, and _next_id counter

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View and Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and optional description, and view all tasks with their details

**Independent Test**: Launch app, add 2-3 tasks (some with descriptions, some without), view the list, verify all tasks appear with ID, title, description, and completion status

**Acceptance Criteria**:
- Empty list shows "No tasks found" message
- Add task with title and description creates task with unique ID
- Add task with only title creates task with empty description
- View all tasks displays ID, title, description, and completion status

### Implementation for User Story 1

- [x] T006 [P] [US1] Implement add_task method in src/services/task_manager.py (validate title, generate ID, create Task, store in dict)
- [x] T007 [P] [US1] Implement get_all_tasks method in src/services/task_manager.py (return list of all Task objects)
- [x] T008 [US1] Implement display_menu function in src/ui/console_ui.py (print menu with 6 options, return void)
- [x] T009 [US1] Implement get_menu_choice function in src/ui/console_ui.py (prompt for choice 1-6, validate, handle errors)
- [x] T010 [US1] Implement handle_add_task function in src/ui/console_ui.py (prompt for title and description, call TaskManager.add_task, display success message)
- [x] T011 [US1] Implement handle_view_tasks function in src/ui/console_ui.py (call TaskManager.get_all_tasks, format and display with status symbols, handle empty list)
- [x] T012 [US1] Implement main application loop in src/main.py (initialize TaskManager, loop display_menu until exit, dispatch to handlers)
- [x] T013 [US1] Add error handling for empty title in src/services/task_manager.py (raise ValueError if title is empty or whitespace-only)
- [x] T014 [US1] Add error handling for invalid menu choice in src/ui/console_ui.py (catch ValueError, display error message, redisplay menu)

**Checkpoint**: User Story 1 complete - users can add and view tasks. This is a functional MVP!

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete to track progress

**Independent Test**: Create 3 tasks, mark 2 as complete, view list to verify status changes, unmark 1 task and verify it shows as incomplete

**Acceptance Criteria**:
- Mark incomplete task as complete updates status and shows confirmation
- Mark complete task as incomplete updates status and shows confirmation
- Invalid task ID shows error message and doesn't crash

### Implementation for User Story 2

- [x] T015 [P] [US2] Implement toggle_completion method in src/services/task_manager.py (validate ID exists, toggle completed field, return new status)
- [x] T016 [P] [US2] Implement task_exists method in src/services/task_manager.py (check if task_id in _tasks dict)
- [x] T017 [US2] Implement handle_toggle_completion function in src/ui/console_ui.py (prompt for task ID, call toggle_completion, display appropriate message)
- [x] T018 [US2] Add error handling for invalid task ID in src/ui/console_ui.py (catch exception, display "Task with ID not found" error)
- [x] T019 [US2] Integrate toggle completion handler into main loop in src/main.py (add menu option 5 dispatch)

**Checkpoint**: User Stories 1 and 2 complete - users can add, view, and mark tasks complete independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can update task title or description without deleting and recreating

**Independent Test**: Create task with title "Buy milk" and no description, update title to "Buy groceries", add description "milk, eggs", verify changes persist

**Acceptance Criteria**:
- Update title changes task title and shows confirmation
- Update description changes task description and shows confirmation
- Empty input in update prompts keeps current value
- Invalid task ID shows error message and doesn't crash
- Empty new title shows error and doesn't update

### Implementation for User Story 3

- [x] T020 [US3] Implement update_task method in src/services/task_manager.py (validate ID exists, update title if provided and non-empty, update description if provided)
- [x] T021 [US3] Implement handle_update_task function in src/ui/console_ui.py (prompt for ID, show current values, prompt for new values, handle empty input to keep current)
- [x] T022 [US3] Add validation for empty new title in src/ui/console_ui.py (check if new title is whitespace-only, display error, don't update)
- [x] T023 [US3] Integrate update task handler into main loop in src/main.py (add menu option 3 dispatch)

**Checkpoint**: User Stories 1, 2, and 3 complete - full task management with add, view, complete, and update

---

## Phase 6: User Story 4 - Delete Unwanted Tasks (Priority: P3)

**Goal**: Users can remove tasks they no longer need to reduce clutter

**Independent Test**: Create 5 tasks, delete tasks with IDs 2 and 4, view list to verify they're gone, confirm remaining tasks have original IDs

**Acceptance Criteria**:
- Delete task removes it from list and shows confirmation
- Remaining tasks retain original IDs (IDs not reassigned)
- Invalid task ID shows error message and doesn't crash

### Implementation for User Story 4

- [x] T024 [US4] Implement delete_task method in src/services/task_manager.py (validate ID exists, remove from _tasks dict, do NOT decrement _next_id)
- [x] T025 [US4] Implement handle_delete_task function in src/ui/console_ui.py (prompt for task ID, call delete_task, display success message)
- [x] T026 [US4] Add error handling for invalid task ID in delete operation in src/ui/console_ui.py (catch exception, display "Task with ID not found" error)
- [x] T027 [US4] Integrate delete task handler into main loop in src/main.py (add menu option 4 dispatch)

**Checkpoint**: All user stories complete - full CRUD operations functional

---

## Phase 7: Polish & Edge Cases

**Purpose**: Handle edge cases and improve robustness across all features

- [x] T028 [P] Add keyboard interrupt (Ctrl+C) handler in src/main.py (catch KeyboardInterrupt, display "Application interrupted. Goodbye!")
- [x] T029 [P] Add EOF signal (Ctrl+D) handler in src/main.py (catch EOFError, display "Application terminated. Goodbye!")
- [x] T030 [P] Implement exit handler in src/ui/console_ui.py (display "Goodbye! Your tasks will be lost when you exit.")
- [x] T031 Add input truncation for very long titles in src/services/task_manager.py (max 1000 characters, silent truncation)
- [x] T032 Add input truncation for very long descriptions in src/services/task_manager.py (max 5000 characters, silent truncation)
- [x] T033 [P] Add type hints to all functions in src/models/task.py
- [x] T034 [P] Add type hints to all functions in src/services/task_manager.py
- [x] T035 [P] Add type hints to all functions in src/ui/console_ui.py
- [x] T036 [P] Add type hints to all functions in src/main.py
- [x] T037 [P] Add docstrings to all public functions in src/services/task_manager.py
- [x] T038 [P] Add docstrings to all public functions in src/ui/console_ui.py
- [x] T039 Verify manual test scenarios in tests/manual/test_scenarios.md work correctly
- [x] T040 Run complete example session from quickstart.md to validate all operations

**Checkpoint**: Application complete, polished, and robust

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational (Phase 2) completion
  - User stories CAN proceed in parallel (different handlers, different use cases)
  - OR sequentially in priority order (P1 → P2 → P3 → P3)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)

**Key Insight**: After Foundational phase, ALL user stories are independent and can be implemented in parallel!

### Within Each User Story

- UI handlers can be written in parallel (marked [P]) if they operate on different operations
- Service methods can be written in parallel (marked [P]) if they implement different operations
- Main loop integration tasks must be done sequentially (one menu option at a time)

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003 can run in parallel with T001-T002

**Phase 2 (Foundational)**:
- T004 and T005 can run in parallel (different files)

**Phase 3 (US1)**:
- T006 and T007 can run in parallel (different methods in same file)
- T008, T009, T010, T011 can run in parallel (different functions in same file)

**Phase 4 (US2)**:
- T015 and T016 can run in parallel (different methods)
- T017 and T018 can be done together (same function with error handling)

**Phase 5 (US3)**:
- T020 and T021 can run in parallel (different files)

**Phase 6 (US4)**:
- T024 and T025 can run in parallel (different files)

**Phase 7 (Polish)**:
- T028, T029, T030 can run in parallel (different error handlers)
- T033, T034, T035, T036 can run in parallel (different files)
- T037, T038 can run in parallel (different files)

---

## Parallel Example: User Story 1

```bash
# Launch parallel tasks for service methods:
Task T006: "Implement add_task method in src/services/task_manager.py"
Task T007: "Implement get_all_tasks method in src/services/task_manager.py"

# Launch parallel tasks for UI functions:
Task T008: "Implement display_menu function in src/ui/console_ui.py"
Task T009: "Implement get_menu_choice function in src/ui/console_ui.py"
Task T010: "Implement handle_add_task function in src/ui/console_ui.py"
Task T011: "Implement handle_view_tasks function in src/ui/console_ui.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T005) - **CRITICAL BLOCKER**
3. Complete Phase 3: User Story 1 (T006-T014)
4. **STOP and VALIDATE**: Test MVP independently using manual test scenarios
5. Deploy/demo basic todo app with add and view operations

**Result**: Functional MVP with core value (add and view tasks)

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 (T006-T014) → Test independently → **Deploy MVP!**
3. Add User Story 2 (T015-T019) → Test independently → Deploy with completion tracking
4. Add User Story 3 (T020-T023) → Test independently → Deploy with update capability
5. Add User Story 4 (T024-T027) → Test independently → Deploy with full CRUD
6. Add Polish (T028-T040) → Validate → Deploy production-ready application

**Each story adds value without breaking previous stories**

### Parallel Team Strategy

With multiple developers (if applicable):

1. Team completes Setup (Phase 1) and Foundational (Phase 2) together
2. Once Foundational is done, split work:
   - Developer A: User Story 1 (T006-T014)
   - Developer B: User Story 2 (T015-T019)
   - Developer C: User Story 3 (T020-T023)
   - Developer D: User Story 4 (T024-T027)
3. Stories complete independently, integrate via main.py menu dispatch
4. Polish together (Phase 7)

**Note**: For Phase I, single developer is expected, but architecture supports parallel work

---

## Manual Testing Checklist

After completing each user story, verify using manual test scenarios:

### User Story 1 Tests
- [ ] Start app with empty list → shows "No tasks found"
- [ ] Add task with title and description → creates with ID 1
- [ ] Add task with only title → creates with ID 2, empty description
- [ ] View all tasks → displays both tasks with all details

### User Story 2 Tests
- [ ] Mark task 1 as complete → status changes, shows confirmation
- [ ] View tasks → task 1 shows [✓]
- [ ] Mark task 1 as incomplete → status changes, shows confirmation
- [ ] Try marking task 999 → shows "Task not found" error

### User Story 3 Tests
- [ ] Update task 1 title → title changes, shows confirmation
- [ ] Update task 1 description → description changes, shows confirmation
- [ ] Update with empty title → shows error, doesn't update
- [ ] Update task 999 → shows "Task not found" error

### User Story 4 Tests
- [ ] Delete task 2 → task removed, shows confirmation
- [ ] View tasks → task 2 gone, task 1 still has ID 1
- [ ] Delete task 999 → shows "Task not found" error

### Edge Cases Tests
- [ ] Press Ctrl+C → shows graceful exit message
- [ ] Enter invalid menu choice → shows error, redisplays menu
- [ ] Add task with very long title (>1000 chars) → truncates silently
- [ ] All operations work correctly per console interface contract

---

## Task Count Summary

- **Total Tasks**: 40
- **Setup (Phase 1)**: 3 tasks
- **Foundational (Phase 2)**: 2 tasks (CRITICAL BLOCKER)
- **User Story 1 (Phase 3)**: 9 tasks - **MVP**
- **User Story 2 (Phase 4)**: 5 tasks
- **User Story 3 (Phase 5)**: 4 tasks
- **User Story 4 (Phase 6)**: 4 tasks
- **Polish (Phase 7)**: 13 tasks

**Parallel Tasks**: 20 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-3 (14 tasks) deliver functional todo app with add/view operations

---

## Notes

- All tasks follow strict checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [P] tasks target different files or different methods/functions within same file
- [Story] labels (US1, US2, US3, US4) map to user stories from spec.md
- Each user story is independently completable and testable
- No automated tests (manual verification only per Phase I scope)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- File paths follow plan.md structure (src/, tests/manual/)
- Constitution compliance: No manual coding, spec-driven, Phase I scope only

**Ready for `/sp.implement` execution!**
