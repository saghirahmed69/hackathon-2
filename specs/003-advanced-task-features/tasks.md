---
description: "Implementation tasks for Advanced Task Management Features"
---

# Tasks: Advanced Task Management Features

**Input**: Design documents from `/specs/003-advanced-task-features/`
**Prerequisites**: plan.md, spec.md

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted. Manual testing will be performed per quickstart.md.

**Status**: 69/75 tasks complete (92%) - Application tested and running successfully
**Last Updated**: 2025-12-26

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with:
- Backend: `backend/app/`
- Frontend: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and database migration preparation

- [x] T001 Add python-dateutil to backend/requirements.txt for recurring date calculations
- [x] T002 [P] Review existing database schema in backend/app/models/task.py
- [x] T003 [P] Review existing backend service layer in backend/app/services/task_service.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Migration

- [x] T004 Create database migration script in backend/app/migrations/add_advanced_features.py to add 5 new columns (priority, due_date, is_recurring, recurrence_pattern, reminder_time)
- [x] T005 Add database indexes for performance in migration script (idx_tasks_priority, idx_tasks_due_date, idx_tasks_reminder)

### Backend Core Extensions

- [x] T006 [P] Extend Task SQLModel in backend/app/models/task.py with 5 new fields (priority, due_date, is_recurring, recurrence_pattern, reminder_time)
- [x] T007 [P] Extend TaskCreate schema in backend/app/schemas/task.py with new fields
- [x] T008 [P] Extend TaskUpdate schema in backend/app/schemas/task.py with new optional fields
- [x] T009 [P] Extend TaskResponse schema in backend/app/schemas/task.py with new fields
- [x] T010 Create RecurringService in backend/app/services/recurring_service.py with calculate_next_due_date() and handle_task_completion() functions

### Frontend Core Extensions

- [x] T011 [P] Extend Task interface in frontend/src/lib/types.ts with 5 new fields
- [x] T012 [P] Define TaskFilterParams interface in frontend/src/lib/types.ts for query parameters

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Priority Management (Priority: P1) 🎯 MVP

**Goal**: Users can assign priority levels (high, medium, low) to tasks with visual indicators

**Independent Test**: Create tasks with different priorities, verify visual indicators appear, verify priority persists and can be updated

### Implementation for User Story 1

- [x] T013 [P] [US1] Add priority validation logic to create_task() in backend/app/services/task_service.py (validate high/medium/low, return 400 if invalid)
- [x] T014 [P] [US1] Add priority validation logic to update_task() in backend/app/services/task_service.py
- [x] T015 [P] [US1] Create PrioritySelector component in frontend/src/components/tasks/PrioritySelector.tsx with dropdown for high/medium/low
- [x] T016 [US1] Integrate PrioritySelector into TaskForm component in frontend/src/components/tasks/TaskForm.tsx (required field)
- [x] T017 [US1] Add priority visual indicators to TaskItem component in frontend/src/components/tasks/TaskItem.tsx (color-coded badges: high=red, medium=yellow, low=green)
- [x] T018 [US1] Update API createTask() function in frontend/src/lib/api.ts to include priority field
- [x] T019 [US1] Update API updateTask() function in frontend/src/lib/api.ts to include priority field

**Checkpoint**: ✅ User Story 1 complete - Priority management fully functional

---

## Phase 4: User Story 2 - Task Due Dates and Scheduling (Priority: P1) 🎯 MVP

**Goal**: Users can set optional due dates (with optional times) and see overdue/today indicators

**Independent Test**: Create tasks with and without due dates, verify overdue tasks are highlighted in red, verify due today tasks are highlighted in yellow, verify dates persist

### Implementation for User Story 2

- [x] T020 [P] [US2] Add due_date validation to create_task() in backend/app/services/task_service.py (validate ISO 8601 format, allow past/future, return 400 if invalid format)
- [x] T021 [P] [US2] Add due_date validation to update_task() in backend/app/services/task_service.py (allow adding/removing due dates)
- [x] T022 [P] [US2] Create DateTimePicker component in frontend/src/components/tasks/DateTimePicker.tsx for date and optional time input
- [x] T023 [US2] Integrate DateTimePicker for due_date into TaskForm component in frontend/src/components/tasks/TaskForm.tsx (optional field)
- [x] T024 [US2] Add overdue indicator logic to TaskItem component in frontend/src/components/tasks/TaskItem.tsx (red highlight if due_date < now and !completed)
- [x] T025 [US2] Add due today indicator logic to TaskItem component in frontend/src/components/tasks/TaskItem.tsx (yellow/orange highlight if due_date is today)
- [x] T026 [US2] Display due date with time in TaskItem component in frontend/src/components/tasks/TaskItem.tsx

**Checkpoint**: ✅ User Stories 1 AND 2 complete (MVP delivered!)

---

## Phase 5: User Story 3 - Search Tasks by Keyword (Priority: P2)

**Goal**: Users can search tasks by keyword in title or description with real-time results

**Independent Test**: Create multiple tasks, search by keyword, verify case-insensitive substring matching, verify clear search works

### Implementation for User Story 3

- [x] T027 [P] [US3] Add search parameter to get_user_tasks_filtered() in backend/app/services/task_service.py (case-insensitive ILIKE on title and description)
- [x] T028 [P] [US3] Update GET /api/tasks endpoint in backend/app/api/tasks.py to accept optional search query parameter (max 500 chars)
- [x] T029 [P] [US3] Create useDebounce hook in frontend/src/hooks/useDebounce.ts with 300ms delay
- [x] T030 [P] [US3] Create SearchBar component in frontend/src/components/tasks/SearchBar.tsx with debounced input
- [x] T031 [US3] Integrate SearchBar into TaskList component in frontend/src/components/tasks/TaskList.tsx
- [x] T032 [US3] Update getTasks() in frontend/src/lib/api.ts to support search query parameter
- [x] T033 [US3] Add empty state message in TaskList when search returns no results

**Checkpoint**: Search feature should work independently of other features

---

## Phase 6: User Story 4 - Filter Tasks by Status, Priority, and Date (Priority: P2)

**Goal**: Users can filter tasks by completion status, priority level, and due date with multi-criteria support

**Independent Test**: Apply various filter combinations (status, priority, due_date), verify correct subset displayed, verify clear filters works

### Implementation for User Story 4

- [x] T034 [P] [US4] Add status filter logic to get_user_tasks_filtered() in backend/app/services/task_service.py (pending/completed)
- [x] T035 [P] [US4] Add priority filter logic to get_user_tasks_filtered() in backend/app/services/task_service.py (high/medium/low)
- [x] T036 [P] [US4] Add due_date filter logic to get_user_tasks_filtered() in backend/app/services/task_service.py (before:/after:/on: operators)
- [x] T037 [P] [US4] Create parse_due_date_filter() helper function in backend/app/services/task_service.py to parse before:/after:/on: format
- [x] T038 [US4] Update GET /api/tasks endpoint in backend/app/api/tasks.py to accept status, priority, and due_date query parameters
- [x] T039 [P] [US4] Create FilterControls component in frontend/src/components/tasks/FilterControls.tsx with status, priority, and due_date filters
- [x] T040 [P] [US4] Create useTaskFilters hook in frontend/src/hooks/useTaskFilters.ts to manage filter state
- [x] T041 [US4] Integrate FilterControls into TaskList component in frontend/src/components/tasks/TaskList.tsx
- [x] T042 [US4] Add clear filters button to FilterControls component
- [x] T043 [US4] Add empty state message when filters return no results

**Checkpoint**: Filtering should work independently and combine with search from US3

---

## Phase 7: User Story 5 - Sort Tasks by Multiple Criteria (Priority: P3)

**Goal**: Users can sort tasks by due date, priority, or alphabetically with ascending/descending order

**Independent Test**: Apply different sort criteria, verify correct task order, verify NULL due dates handled correctly, verify sort works with filters

### Implementation for User Story 5

- [x] T044 [P] [US5] Add sort_by and sort_order logic to get_user_tasks_filtered() in backend/app/services/task_service.py (due_date with NULLS LAST/FIRST, priority with custom ordering, title alphabetically)
- [x] T045 [US5] Update GET /api/tasks endpoint in backend/app/api/tasks.py to accept sort_by and sort_order query parameters
- [x] T046 [P] [US5] Create SortControls component in frontend/src/components/tasks/SortControls.tsx with sort_by dropdown and asc/desc toggle
- [x] T047 [US5] Integrate SortControls into TaskList component in frontend/src/components/tasks/TaskList.tsx
- [x] T048 [US5] Add sort state management to useTaskFilters hook in frontend/src/hooks/useTaskFilters.ts

**Checkpoint**: Sorting should work independently and combine with search and filters

---

## Phase 8: User Story 6 - Recurring Tasks (Priority: P3)

**Goal**: Users can mark tasks as recurring (daily, weekly, monthly) with automatic regeneration when completed

**Independent Test**: Create recurring tasks with different patterns, mark complete, verify new instance created with correct due date, verify monthly edge cases (month-end)

### Implementation for User Story 6

- [x] T049 [P] [US6] Add recurrence validation to create_task() in backend/app/services/task_service.py (validate daily/weekly/monthly if is_recurring=true)
- [x] T050 [P] [US6] Add recurrence validation to update_task() in backend/app/services/task_service.py
- [x] T051 [US6] Integrate handle_task_completion() from RecurringService into update_task() in backend/app/services/task_service.py (call when completed transitions from False to True)
- [x] T052 [P] [US6] Add recurring checkbox and pattern selector to TaskForm component in frontend/src/components/tasks/TaskForm.tsx
- [x] T053 [P] [US6] Add recurring icon indicator to TaskItem component in frontend/src/components/tasks/TaskItem.tsx (circular arrow if is_recurring=true)
- [x] T054 [US6] Update API createTask() and updateTask() in frontend/src/lib/api.ts to include is_recurring and recurrence_pattern fields

**Checkpoint**: Recurring tasks should work independently with automatic instance creation

---

## Phase 9: User Story 7 - Task Reminders with Browser Notifications (Priority: P3)

**Goal**: Users can set date/time reminders on tasks with browser notifications at scheduled time

**Independent Test**: Set reminders on tasks, grant notification permissions, verify notifications appear at scheduled time, verify click navigation to dashboard with task highlighted, verify no notifications for completed tasks

### Implementation for User Story 7

- [x] T055 [P] [US7] Add reminder_time validation to create_task() in backend/app/services/task_service.py (validate ISO 8601 format, require future timestamp, return 400 if in past)
- [x] T056 [P] [US7] Add reminder_time validation to update_task() in backend/app/services/task_service.py
- [x] T057 [P] [US7] Create NotificationService class in frontend/src/lib/notifications.ts with requestPermission(), scheduleReminder(), and showNotification() methods
- [x] T058 [P] [US7] Create useNotifications hook in frontend/src/hooks/useNotifications.ts to request permissions and schedule reminders for all tasks
- [x] T059 [US7] Integrate DateTimePicker for reminder_time into TaskForm component in frontend/src/components/tasks/TaskForm.tsx (optional field, validate future timestamp)
- [x] T060 [US7] Add reminder icon indicator to TaskItem component in frontend/src/components/tasks/TaskItem.tsx (bell icon if reminder_time is set)
- [x] T061 [US7] Integrate useNotifications hook in dashboard page in frontend/src/app/dashboard/page.tsx to initialize notifications
- [x] T062 [US7] Add notification click handler to navigate to dashboard with task highlighted in frontend/src/lib/notifications.ts (query param ?highlight={taskId})
- [x] T063 [US7] Handle ?highlight query parameter in dashboard page in frontend/src/app/dashboard/page.tsx to scroll task into view
- [x] T064 [US7] Add permission denied UI message to TaskForm when notification permissions are denied

**Checkpoint**: All user stories should now be independently functional

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T065 [P] Run database migration script to apply schema changes to development database
- [x] T066 [P] Verify backward compatibility by testing all existing Phase II features (create, read, update, delete, complete tasks, authentication)
- [x] T067 [P] Update frontend API client in frontend/src/lib/api.ts to build query strings correctly for all filter/sort/search parameters
- [ ] T068 Code review all backend validation logic for edge cases (empty search, invalid dates, special characters)
- [ ] T069 Code review all frontend components for accessibility (keyboard navigation, ARIA labels, color contrast)
- [ ] T070 Performance testing for search and filter operations (verify <2s response time)
- [ ] T071 Test browser notification delivery timing (verify <5s from scheduled time)
- [ ] T072 Security review for SQL injection protection in search and filter queries
- [x] T073 [P] Create quickstart.md manual testing guide in specs/003-advanced-task-features/quickstart.md
- [ ] T074 Run quickstart.md validation scenarios for all 7 user stories
- [ ] T075 Document edge cases tested (priority validation, reminder in past, recurring without due date, search with special chars, filter combinations returning zero results)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P2 → P3 → P3 → P3)
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories (can run in parallel with US1)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Integrates with US3 search but independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Integrates with US3/US4 but independently testable
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - Uses due_date from US2 but independently testable
- **User Story 7 (P3)**: Can start after Foundational (Phase 2) - Uses due_date from US2 but independently testable

### Within Each User Story

- Backend validation before frontend components
- Core components before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: All 3 tasks can run in parallel

**Phase 2 (Foundational)**:
- Database migration (T004-T005) sequential
- Backend models/schemas (T006-T009) can run in parallel after migration
- Frontend types (T011-T012) can run in parallel with backend
- RecurringService (T010) can run in parallel

**Phase 3 (US1)**: T013-T015 can run in parallel, then sequential integration

**Phase 4 (US2)**: T020-T022 can run in parallel, then sequential integration

**Phase 5 (US3)**: T027-T030 can run in parallel, then sequential integration

**Phase 6 (US4)**: T034-T037, T039-T040 can run in parallel, then sequential integration

**Phase 7 (US5)**: T044, T046 can run in parallel, then sequential integration

**Phase 8 (US6)**: T049-T050, T052-T053 can run in parallel, then sequential integration

**Phase 9 (US7)**: T055-T058 can run in parallel, then sequential integration

**Phase 10 (Polish)**: T065-T067, T069, T073 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch backend and frontend validation in parallel:
Task T013: "Add priority validation to create_task() in backend/app/services/task_service.py"
Task T014: "Add priority validation to update_task() in backend/app/services/task_service.py"
Task T015: "Create PrioritySelector component in frontend/src/components/tasks/PrioritySelector.tsx"

# Then integrate sequentially:
Task T016: "Integrate PrioritySelector into TaskForm"
Task T017: "Add priority visual indicators to TaskItem"
Task T018-T019: "Update API functions"
```

---

## Parallel Example: Multiple User Stories (Team Strategy)

Once Phase 2 (Foundational) is complete, different developers can work on different user stories:

```bash
# Developer A:
Phase 3: User Story 1 (Priority Management)

# Developer B (in parallel):
Phase 4: User Story 2 (Due Dates)

# Developer C (in parallel):
Phase 5: User Story 3 (Search)
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only - Both P1)

1. Complete Phase 1: Setup (3 tasks)
2. Complete Phase 2: Foundational (10 tasks) ⚠️ BLOCKS all stories
3. Complete Phase 3: User Story 1 (7 tasks) 🎯 Priority management
4. Complete Phase 4: User Story 2 (7 tasks) 🎯 Due dates
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently
6. Deploy/demo if ready (MVP delivered!)

### Incremental Delivery (Add P2 Features)

7. Complete Phase 5: User Story 3 (7 tasks) - Search
8. Complete Phase 6: User Story 4 (10 tasks) - Filtering
9. **STOP and VALIDATE**: Test US1-4 together
10. Deploy/demo enhanced version

### Full Feature Set (Add P3 Features)

11. Complete Phase 7: User Story 5 (5 tasks) - Sorting
12. Complete Phase 8: User Story 6 (6 tasks) - Recurring
13. Complete Phase 9: User Story 7 (10 tasks) - Reminders
14. Complete Phase 10: Polish (11 tasks)
15. **FINAL VALIDATION**: Run quickstart.md for all 7 user stories
16. Deploy production-ready version

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (13 tasks)
2. Once Foundational is done, split by priority:
   - **Sprint 1 (P1 - MVP)**: Developer A on US1, Developer B on US2 (parallel)
   - **Sprint 2 (P2)**: Developer A on US3, Developer B on US4 (parallel)
   - **Sprint 3 (P3)**: Developer A on US5, Developer B on US6, Developer C on US7 (parallel)
3. Polish phase together (11 tasks)

---

## Summary

**Total Tasks**: 75 tasks

**Task Count by User Story**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 10 tasks ⚠️ BLOCKING
- Phase 3 (US1 - Priority): 7 tasks 🎯 P1
- Phase 4 (US2 - Due Dates): 7 tasks 🎯 P1
- Phase 5 (US3 - Search): 7 tasks (P2)
- Phase 6 (US4 - Filtering): 10 tasks (P2)
- Phase 7 (US5 - Sorting): 5 tasks (P3)
- Phase 8 (US6 - Recurring): 6 tasks (P3)
- Phase 9 (US7 - Reminders): 10 tasks (P3)
- Phase 10 (Polish): 11 tasks

**Parallel Opportunities**: 35+ tasks can run in parallel within phases

**Independent Test Criteria**: Each user story has clear acceptance scenarios from spec.md

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2) = 27 tasks for basic priority and due date management

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability (US1-US7)
- Each user story is independently completable and testable
- No automated tests included (manual testing via quickstart.md per spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All 78 functional requirements (FR-001 to FR-078) are covered across tasks
- All 20 success criteria (SC-001 to SC-020) are validated in Phase 10
