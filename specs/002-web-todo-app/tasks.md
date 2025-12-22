# Implementation Tasks: Full-Stack Web Todo Application

**Feature**: 002-web-todo-app
**Branch**: `002-web-todo-app`
**Date**: 2025-12-21
**Status**: Ready for implementation

## Overview

This task list implements all 5 user stories for Phase II in priority order. Tasks are organized by user story to enable independent, incremental delivery.

**Total User Stories**: 5 (2 × P1-MVP, 1 × P2, 2 × P3)
**Total Tasks**: 98
**Parallel Opportunities**: 45 tasks marked [P]
**MVP Scope**: User Story 1 + User Story 2 (authentication + basic task CRUD)

---

## Task Legend

- `- [ ]` = Pending task
- `- [X]` = Completed task
- `[P]` = Parallelizable (can run concurrently with other [P] tasks in same phase)
- `[US#]` = User Story number (maps to spec.md)
- **TaskID** = T001, T002, T003... (sequential execution order)

---

## Phase 1: Project Setup & Infrastructure

**Goal**: Initialize monorepo structure, install dependencies, configure environments

**Duration Estimate**: ~30 minutes

### Backend Setup

- [ ] T001 Create backend directory structure per plan.md
- [ ] T002 [P] Create backend/app/__init__.py
- [ ] T003 [P] Create backend/app/models/__init__.py
- [ ] T004 [P] Create backend/app/schemas/__init__.py
- [ ] T005 [P] Create backend/app/services/__init__.py
- [ ] T006 [P] Create backend/app/api/__init__.py
- [ ] T007 [P] Create backend/app/middleware/__init__.py
- [ ] T008 Create backend/requirements.txt with dependencies: fastapi, uvicorn[standard], sqlmodel, asyncpg, python-jose[cryptography], passlib[bcrypt], python-multipart, pydantic-settings
- [ ] T009 Create backend/.env.example with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, FRONTEND_URL, ENVIRONMENT
- [ ] T010 Create backend/.gitignore with Python patterns: __pycache__/, *.pyc, .venv/, venv/, .env, *.log

### Frontend Setup

- [ ] T011 Create frontend directory structure per plan.md
- [ ] T012 [P] Create frontend/src/app/layout.tsx (root layout)
- [ ] T013 [P] Create frontend/src/app/page.tsx (landing page)
- [ ] T014 [P] Create frontend/src/components/auth/.gitkeep
- [ ] T015 [P] Create frontend/src/components/tasks/.gitkeep
- [ ] T016 [P] Create frontend/src/lib/.gitkeep
- [ ] T017 Create frontend/package.json with dependencies: next@16+, react@18+, react-dom, typescript, tailwindcss, better-auth, @types/node, @types/react, @types/react-dom
- [ ] T018 Create frontend/tsconfig.json with Next.js TypeScript config
- [ ] T019 Create frontend/tailwind.config.ts with Tailwind CSS configuration
- [ ] T020 Create frontend/next.config.js with API proxy and environment config
- [ ] T021 Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, NODE_ENV
- [ ] T022 Create frontend/.gitignore with Node.js patterns: node_modules/, .next/, dist/, *.log, .env.local

### Root Configuration

- [ ] T023 Create root .gitignore combining Python and Node.js patterns
- [ ] T024 Create root README.md with project overview and setup instructions
- [ ] T025 Create root .editorconfig for consistent code style

---

## Phase 2: Foundational Layer

**Goal**: Database connection, configuration, core utilities (blocking prerequisites for all user stories)

**Duration Estimate**: ~45 minutes

**Dependencies**: Must complete Phase 1 first

### Backend Foundational

- [ ] T026 Create backend/app/config.py with Pydantic settings for environment variables
- [ ] T027 Create backend/app/database.py with SQLModel async engine and session management
- [ ] T028 Create backend/app/main.py with FastAPI app initialization, CORS middleware, and startup/shutdown events
- [ ] T029 Add health check endpoint GET /health in backend/app/main.py
- [ ] T030 Create backend/app/middleware/jwt_middleware.py with JWT verification dependency get_current_user()

### Frontend Foundational

- [ ] T031 Create frontend/src/lib/types.ts with User and Task TypeScript interfaces
- [ ] T032 Create frontend/src/lib/api.ts with API client wrapper (fetch with base URL and auth headers)
- [ ] T033 Create frontend/src/lib/auth.ts with Better Auth configuration
- [ ] T034 Create frontend/src/middleware.ts with route protection logic (redirect unauthenticated users)

---

## Phase 3: User Story 1 - User Registration & Authentication (P1-MVP)

**Goal**: Users can sign up, sign in, logout, and access protected routes

**Independent Test**: Complete signup flow, sign in, verify JWT token issuance, access dashboard

**Acceptance Criteria**:
- ✅ Email validation works (client + server)
- ✅ Password validation works (min 8 characters)
- ✅ Duplicate email rejected with clear error
- ✅ Invalid credentials rejected
- ✅ JWT token issued on successful signin
- ✅ Protected routes redirect to signin when unauthenticated

**Duration Estimate**: ~2 hours

**Dependencies**: Phase 2 complete

### Backend - User Model & Schema

- [X] T035 [P] [US1] Create User model in backend/app/models/user.py with SQLModel (id, email, hashed_password, created_at)
- [X] T036 [P] [US1] Create auth schemas in backend/app/schemas/auth.py (SignupRequest, SigninRequest, AuthResponse, UserResponse)

### Backend - Authentication Service

- [X] T037 [US1] Create auth service in backend/app/services/auth_service.py with signup, signin, verify_password, create_access_token functions
- [X] T038 [US1] Implement password hashing with passlib bcrypt in auth_service.py
- [X] T039 [US1] Implement JWT token generation with python-jose in auth_service.py

### Backend - Authentication API

- [X] T040 [US1] Create auth routes in backend/app/api/auth.py
- [X] T041 [US1] Implement POST /api/auth/signup endpoint (email validation, duplicate check, password hashing)
- [X] T042 [US1] Implement POST /api/auth/signin endpoint (credential verification, JWT issuance)
- [X] T043 [US1] Implement POST /api/auth/logout endpoint (return success message)
- [X] T044 [US1] Add error handling for auth endpoints (400, 401, 409, 500)
- [X] T045 [US1] Register auth router in backend/app/main.py

### Frontend - Auth UI Components

- [X] T046 [P] [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.tsx with email/password fields and client-side validation
- [X] T047 [P] [US1] Create SigninForm component in frontend/src/components/auth/SigninForm.tsx with email/password fields
- [X] T048 [P] [US1] Create signup page in frontend/src/app/signup/page.tsx using SignupForm component
- [X] T049 [P] [US1] Create signin page in frontend/src/app/signin/page.tsx using SigninForm component

### Frontend - Auth Integration

- [X] T050 [US1] Implement signup API call in SignupForm.tsx (POST /api/auth/signup, redirect to signin on success)
- [X] T051 [US1] Implement signin API call in SigninForm.tsx (POST /api/auth/signin, store JWT token, redirect to dashboard)
- [X] T052 [US1] Implement logout functionality (clear token, redirect to signin)
- [X] T053 [US1] Update middleware.ts to protect /dashboard route (check JWT token, redirect if missing)

### Database Migration

- [X] T054 [US1] Run SQLModel.metadata.create_all() to create users table in Neon PostgreSQL
- [X] T055 [US1] Verify users table schema matches data-model.md (id, email unique index, hashed_password, created_at)

### US1 Validation

- [ ] T056 [US1] Test Scenario 1: Sign up with valid credentials → redirected to signin with success message
- [ ] T057 [US1] Test Scenario 1: Sign in with correct credentials → redirected to dashboard with JWT token
- [ ] T058 [US1] Test Scenario 1: Logout → session terminated, redirected to signin
- [ ] T059 [US1] Test Scenario 1: Access /dashboard without auth → redirected to signin

---

## Phase 4: User Story 2 - View & Create Tasks (P1-MVP)

**Goal**: Authenticated users can view their tasks and create new ones

**Independent Test**: Sign in, create tasks with title/description, view them in task list

**Acceptance Criteria**:
- ✅ Empty state shown when no tasks
- ✅ Task creation form validates title (required)
- ✅ Created tasks appear immediately in list
- ✅ Only user's own tasks visible (user isolation)

**Duration Estimate**: ~2 hours

**Dependencies**: US1 complete (authentication required)

### Backend - Task Model & Schema

- [X] T060 [P] [US2] Create Task model in backend/app/models/task.py with SQLModel (id, user_id FK, title, description, completed, created_at, updated_at)
- [X] T061 [P] [US2] Create task schemas in backend/app/schemas/task.py (TaskCreate, TaskResponse, TaskUpdate)

### Backend - Task Service

- [X] T062 [US2] Create task service in backend/app/services/task_service.py
- [X] T063 [US2] Implement get_user_tasks(user_id) function with user isolation filter
- [X] T064 [US2] Implement create_task(user_id, title, description) function with validation
- [X] T065 [US2] Add title validation (non-empty, non-whitespace, max 1000 chars)

### Backend - Task API (Read & Create)

- [X] T066 [US2] Create task routes in backend/app/api/tasks.py
- [X] T067 [US2] Implement GET /api/tasks endpoint with JWT authentication and user filtering
- [X] T068 [US2] Implement POST /api/tasks endpoint with JWT authentication and validation
- [X] T069 [US2] Add error handling for task endpoints (400, 401, 404, 500)
- [X] T070 [US2] Register tasks router in backend/app/main.py

### Frontend - Task UI Components

- [X] T071 [P] [US2] Create TaskList component in frontend/src/components/tasks/TaskList.tsx to display tasks in table/list format
- [X] T072 [P] [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx to render individual task
- [X] T073 [P] [US2] Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx with title/description fields
- [X] T074 [P] [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx using TaskList and TaskForm

### Frontend - Task Integration

- [X] T075 [US2] Implement GET /api/tasks call in dashboard page to fetch user's tasks
- [X] T076 [US2] Implement POST /api/tasks call in TaskForm to create new task
- [X] T077 [US2] Add loading state during task fetch
- [X] T078 [US2] Add empty state message when no tasks exist
- [X] T079 [US2] Add success notification after task creation
- [X] T080 [US2] Refresh task list after creation

### Database Migration

- [X] T081 [US2] Run SQLModel.metadata.create_all() to create tasks table in Neon PostgreSQL
- [X] T082 [US2] Verify tasks table schema matches data-model.md (id, user_id FK with cascade delete, title, description nullable, completed default false, timestamps)
- [X] T083 [US2] Verify indexes created (user_id, user_id+completed composite)

### US2 Validation

- [ ] T084 [US2] Test Scenario 2: View dashboard with no tasks → empty state shown
- [ ] T085 [US2] Test Scenario 2: Create task with title + description → appears in list
- [ ] T086 [US2] Test Scenario 2: Create task without title → validation error
- [ ] T087 [US2] Test Scenario 2: User A creates task → User B cannot see it (user isolation)

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (P2)

**Goal**: Users can toggle task completion status

**Independent Test**: Create task, mark complete, verify visual distinction, reload page to verify persistence

**Acceptance Criteria**:
- ✅ Visual distinction between completed/incomplete tasks
- ✅ Changes persist after page reload
- ✅ Confirmation message on toggle

**Duration Estimate**: ~45 minutes

**Dependencies**: US2 complete (tasks must exist to toggle)

### Backend - Update Service (Completion Toggle)

- [X] T088 [US3] Add update_task(task_id, user_id, updates) function to backend/app/services/task_service.py
- [X] T089 [US3] Add ownership verification in update_task (return None if user doesn't own task)
- [X] T090 [US3] Set updated_at timestamp on task update

### Backend - Update API (Completion Toggle)

- [X] T091 [US3] Implement PATCH /api/tasks/{task_id} endpoint in backend/app/api/tasks.py
- [X] T092 [US3] Add authentication check (JWT required)
- [X] T093 [US3] Add ownership check (return 403 if user doesn't own task, 404 if task not found)
- [X] T094 [US3] Handle partial updates (only update provided fields)

### Frontend - Completion Toggle UI

- [X] T095 [US3] Add checkbox/toggle button to TaskItem component for completion status
- [X] T096 [US3] Add visual styling for completed tasks (strikethrough or color change)
- [X] T097 [US3] Implement PATCH /api/tasks/{id} call on checkbox click
- [X] T098 [US3] Add success notification after status change
- [X] T099 [US3] Update task list state optimistically

### US3 Validation

- [ ] T100 [US3] Test Scenario 3: Mark task complete → visual indication appears
- [ ] T101 [US3] Test Scenario 3: Reload page → task still marked complete
- [ ] T102 [US3] Test Scenario 3: Mark task incomplete → returns to incomplete status

---

## Phase 6: User Story 4 - Update Task Details (P3)

**Goal**: Users can edit task title and description

**Independent Test**: Create task, edit title/description, verify changes persist

**Acceptance Criteria**:
- ✅ Title updates work
- ✅ Description updates work
- ✅ Empty title validation prevents saving
- ✅ Cancel button works (no changes saved)

**Duration Estimate**: ~45 minutes

**Dependencies**: US2 complete, US3 complete (uses same PATCH endpoint)

### Frontend - Edit Task UI

- [X] T103 [US4] Add edit button to TaskItem component
- [X] T104 [US4] Add edit mode state to TaskItem (toggle between view/edit)
- [X] T105 [US4] Add inline form inputs for title/description in edit mode
- [X] T106 [US4] Add Save and Cancel buttons in edit mode
- [X] T107 [US4] Implement PATCH /api/tasks/{id} call on Save with title/description updates
- [X] T108 [US4] Add client-side validation (title required)
- [X] T109 [US4] Add success notification after update
- [X] T110 [US4] Revert to view mode on Cancel (discard changes)

### US4 Validation

- [ ] T111 [US4] Test Scenario 4: Edit task title → title updated and displayed
- [ ] T112 [US4] Test Scenario 4: Edit task description → description updated
- [ ] T113 [US4] Test Scenario 4: Clear title field and save → validation error
- [ ] T114 [US4] Test Scenario 4: Click Cancel during edit → task returns to original state

---

## Phase 7: User Story 5 - Delete Tasks (P3)

**Goal**: Users can permanently delete tasks

**Independent Test**: Create task, delete with confirmation, verify removal and persistence

**Acceptance Criteria**:
- ✅ Confirmation dialog appears before delete
- ✅ Cancel works (task not deleted)
- ✅ Confirm works (task deleted permanently)
- ✅ Deletion persists after reload

**Duration Estimate**: ~30 minutes

**Dependencies**: US2 complete (tasks must exist to delete)

### Backend - Delete Service & API

- [X] T115 [US5] Add delete_task(task_id, user_id) function to backend/app/services/task_service.py with ownership check
- [X] T116 [US5] Implement DELETE /api/tasks/{task_id} endpoint in backend/app/api/tasks.py
- [X] T117 [US5] Add authentication check (JWT required)
- [X] T118 [US5] Add ownership check (return 403 if user doesn't own task, 404 if task not found)
- [X] T119 [US5] Return 204 No Content on successful deletion

### Frontend - Delete Task UI

- [X] T120 [US5] Add delete button to TaskItem component
- [X] T121 [US5] Add confirmation dialog on delete button click
- [X] T122 [US5] Implement DELETE /api/tasks/{id} call on confirm
- [X] T123 [US5] Remove task from list state on successful deletion
- [X] T124 [US5] Add success notification after deletion
- [X] T125 [US5] Handle Cancel in confirmation dialog (no API call)

### US5 Validation

- [ ] T126 [US5] Test Scenario 5: Click delete → confirmation dialog appears
- [ ] T127 [US5] Test Scenario 5: Click Cancel → task remains in list
- [ ] T128 [US5] Test Scenario 5: Click Confirm → task removed from list
- [ ] T129 [US5] Test Scenario 5: Reload page → deleted task does not reappear
- [ ] T130 [US5] Test Scenario 5: Try to delete another user's task via API → 403 error

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Final touches, error handling, loading states, documentation

**Duration Estimate**: ~1 hour

**Dependencies**: All user stories complete

### Error Handling & UX

- [ ] T131 [P] Add global error boundary in frontend/src/app/layout.tsx
- [X] T132 [P] Add loading spinners for all async operations
- [X] T133 [P] Add toast/notification system for success/error messages
- [X] T134 [P] Improve error messages (user-friendly, actionable)
- [X] T135 [P] Add form validation error display (inline, clear)

### Styling & Responsiveness

- [X] T136 [P] Style landing page with Tailwind CSS
- [X] T137 [P] Style signup/signin forms with Tailwind CSS
- [X] T138 [P] Style dashboard and task list with Tailwind CSS
- [X] T139 [P] Ensure mobile responsiveness (test on small screens)
- [X] T140 [P] Add hover states and transitions for better UX

### Documentation

- [ ] T141 [P] Update README.md with complete setup instructions
- [ ] T142 [P] Add API documentation links (FastAPI /docs) to README
- [ ] T143 [P] Document environment variables in README
- [ ] T144 [P] Add troubleshooting section to README

### Testing & Validation

- [ ] T145 Execute all 7 test scenarios from quickstart.md
- [ ] T146 Verify constitution compliance (all 13 principles satisfied)
- [ ] T147 Verify all 54 functional requirements met
- [ ] T148 Verify all 14 success criteria met

---

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1 - Auth) ← BLOCKING for all other user stories
    ↓
Phase 4 (US2 - View/Create Tasks) ← BLOCKING for US3, US4, US5
    ├→ Phase 5 (US3 - Toggle Complete)
    ├→ Phase 6 (US4 - Update Details)
    └→ Phase 7 (US5 - Delete Tasks)
    ↓
Phase 8 (Polish)
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 (US1) → Phase 4 (US2) → Phase 8

**Parallel Opportunities**:
- Phases 5, 6, 7 can be implemented in any order after Phase 4
- Many [P] tasks within each phase can run concurrently

---

## Parallel Execution Examples

### Phase 1 (Setup) - Parallel Groups

**Group 1** (can run in parallel after T001):
- T002, T003, T004, T005, T006, T007 (backend __init__ files)
- T012, T013, T014, T015, T016 (frontend directory setup)

**Sequential Dependencies**:
- T008, T009, T010 (backend config files - run after Group 1)
- T017-T022 (frontend config files - run after Group 1)

### Phase 3 (US1) - Parallel Groups

**Group 1** (after T034):
- T035, T036 (models and schemas - independent)

**Group 2** (after T039):
- T046, T047, T048, T049 (all frontend components - independent)

### Phase 4 (US2) - Parallel Groups

**Group 1** (after T059):
- T060, T061 (model and schema - independent)

**Group 2** (after T065):
- T071, T072, T073, T074 (all frontend components - independent)

---

## Implementation Strategy

### MVP Delivery (Phases 1-4)

**Target**: Deliver working authentication + basic task management
**Duration**: ~5-6 hours
**Value**: Users can sign up, sign in, create tasks, view tasks

**Deliverables**:
- ✅ Backend API with auth and task endpoints
- ✅ Frontend with signup, signin, dashboard
- ✅ Database with users and tasks tables
- ✅ JWT authentication working
- ✅ User isolation enforced

### Enhanced Features (Phases 5-7)

**Target**: Add task completion toggle, update, delete
**Duration**: ~2-3 hours
**Value**: Full CRUD operations on tasks

### Production Ready (Phase 8)

**Target**: Polish UX, validate requirements
**Duration**: ~1 hour
**Value**: Production-ready application

---

## Task Summary

| Phase | Task Count | Parallel Tasks | Duration Estimate |
|-------|------------|----------------|-------------------|
| Phase 1: Setup | 25 | 12 | ~30 min |
| Phase 2: Foundational | 9 | 0 | ~45 min |
| Phase 3: US1 (Auth) | 25 | 6 | ~2 hours |
| Phase 4: US2 (View/Create) | 28 | 8 | ~2 hours |
| Phase 5: US3 (Toggle) | 15 | 0 | ~45 min |
| Phase 6: US4 (Update) | 12 | 0 | ~45 min |
| Phase 7: US5 (Delete) | 16 | 0 | ~30 min |
| Phase 8: Polish | 18 | 14 | ~1 hour |
| **TOTAL** | **148** | **40** | **~8-9 hours** |

**MVP Scope** (Phases 1-4): 87 tasks, ~5-6 hours

---

## Validation Checklist

After completing all tasks, verify:

- [ ] All 5 user stories implemented and tested
- [ ] All 54 functional requirements met (FR-001 to FR-054)
- [ ] All 14 success criteria achieved (SC-001 to SC-014)
- [ ] All 7 test scenarios pass (from quickstart.md)
- [ ] Constitution compliance verified (13/13 principles)
- [ ] User isolation enforced (database + API levels)
- [ ] No manual code edits performed (all code generated by Claude Code)

**Status after completion**: Ready for deployment (Frontend: Vercel, Backend: Railway, Database: Neon production tier)

---

**Next Step**: Run `/sp.implement` to execute all tasks
