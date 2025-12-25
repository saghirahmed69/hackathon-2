---
id: 0003
title: Advanced Task Features Implementation Plan
stage: plan
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-advanced-task-features
branch: 003-advanced-task-features
user: saghir
command: /sp.plan
labels: ["planning", "architecture", "database-migration", "api-design", "frontend-components", "recurring-tasks", "browser-notifications"]
links:
  spec: specs/003-advanced-task-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/003-advanced-task-features/plan.md
tests:
 - None (planning phase - no tests yet)
---

## Prompt

You are now tasked with creating a comprehensive implementation plan for the Advanced Task Management Features specification.

**Context:**
- **Feature**: 003-advanced-task-features (extending Phase II web todo application)
- **Specification**: specs/003-advanced-task-features/spec.md (78 functional requirements, 20 success criteria, 7 user stories)
- **Clarifications**: All 5 critical ambiguities resolved (reminder validation, monthly recurrence, migration defaults, search UX, notification navigation)
- **Existing Phase II Stack**:
  - **Backend**: Python 3.10+, FastAPI, SQLModel ORM, Neon Serverless PostgreSQL, JWT authentication
  - **Frontend**: Next.js 16+ with App Router, TypeScript, React 18+, Tailwind CSS, Better Auth
  - **Repository Structure**: Monorepo with frontend/ and backend/ directories
  - **Current Task Model**: id, user_id, title, description, completed, created_at, updated_at

**Requirements:**

1. **Database Evolution**:
   - Add 5 new columns to tasks table: priority, due_date, is_recurring, recurrence_pattern, reminder_time
   - Backward-compatible migration with default values (priority='medium')
   - Preserve existing Phase II data integrity

2. **Backend API Enhancements**:
   - Extend GET /api/tasks with query parameters: search, status, priority, due_date, sort_by, sort_order
   - Update POST /api/tasks and PATCH /api/tasks/{id} to accept new fields
   - Implement server-side filtering, sorting, and search logic
   - Handle recurring task instance generation on completion

3. **Frontend Enhancements**:
   - New components: PrioritySelector, DateTimePicker, SearchBar, FilterControls, SortControls, RecurrenceSelector, ReminderInput
   - Real-time search with 300ms debouncing
   - Browser notification integration with permission request
   - Visual indicators for priority, overdue tasks, completed tasks
   - Dashboard navigation with task highlighting on notification click

4. **API Contracts**:
   - Request/response types for extended task schema
   - Query parameter validation and error responses
   - ISO 8601 date/time formats

5. **Spec Traceability**:
   - Map each implementation decision to specific FR-xxx requirements
   - Reference clarification decisions where applicable
   - Document edge case handling (month-end recurrence, past reminders, invalid inputs)

**Deliverables:**
- plan.md: Complete implementation architecture covering database, backend, frontend, integration, and testing
- Constitution compliance verification (all 13 Phase II principles)
- Risk analysis and mitigation strategies
- ADR suggestions for significant architectural decisions

**Planning Approach:**
- Layer 1: Database schema changes and migration strategy
- Layer 2: Backend API contract extensions
- Layer 3: Service layer business logic (filtering, sorting, recurring task generation)
- Layer 4: Frontend component architecture and state management
- Layer 5: Browser notification integration
- Testing strategy across all layers
- Phase 0/1/2 execution breakdown

## Response snapshot

Successfully created comprehensive 5-layer implementation plan for Advanced Task Management Features extending Phase II.

**Plan Structure**:

1. **Database Layer** (Layer 1):
   - Migration adding 5 columns with backward-compatible defaults
   - Updated Task model with python-dateutil for month-end edge cases
   - Enum types for priority ('high', 'medium', 'low') and recurrence_pattern ('daily', 'weekly', 'monthly')

2. **Backend API Layer** (Layer 2):
   - Extended GET /api/tasks with 6 query parameters (search, status, priority, due_date, sort_by, sort_order)
   - Updated POST/PATCH endpoints to accept new fields with validation
   - Error responses for invalid query params and past reminders (HTTP 400)

3. **Service Layer** (Layer 3):
   - Filtering logic with query composition (SQLModel filters)
   - Search with case-insensitive ILIKE (FR-025)
   - Sorting with type-specific comparisons (nulls last for due_date)
   - Recurring task generation with calculate_next_due_date() using relativedelta
   - Real-time debounced search implementation (300ms delay)

4. **Frontend Layer** (Layer 4):
   - 8 new components (PrioritySelector, DateTimePicker, SearchBar, FilterControls, SortControls, RecurrenceSelector, ReminderInput, TaskCard enhancements)
   - Extended Task interface with new optional fields
   - TaskFilterParams type for query parameters
   - Visual indicators for priority badges, overdue highlights, completion state

5. **Browser Notifications Layer** (Layer 5):
   - NotificationService class with permission request flow
   - setTimeout-based reminder scheduling
   - Navigation to dashboard with task highlighting (scrollIntoView)
   - Permission state management (denied, granted, default)

**Constitution Compliance**: Verified all 13 Phase II principles (Spec-Driven First, No Manual Coding, Phase II Scope Discipline, Authentication First, Persistent Storage, User Isolation, etc.)

**Risk Analysis**:
- Database migration testing (rollback plan documented)
- Month-end recurrence edge cases (python-dateutil handles Feb 29 → Mar 29)
- Browser notification permissions (graceful degradation documented)
- Performance impact of complex filters (EXPLAIN ANALYZE recommended)

**ADR Suggestions** (3 decisions identified):
1. Query-parameter-based filtering vs GraphQL (chose REST extensions for consistency)
2. Recurring task instance generation model (chose "new task on completion" vs update-in-place)
3. Browser notifications vs server-sent events (chose client-side setTimeout for simplicity)

**Files Created**: plan.md (776 lines covering all layers, migration strategy, testing plan, constitution check)

## Outcome

- ✅ Impact: Created complete technical architecture for 78 functional requirements across 5 implementation layers
- 🧪 Tests: No tests yet - plan defines testing strategy for manual testing, backend unit tests, frontend component tests, and integration tests
- 📁 Files: 1 file created (plan.md)
- 🔁 Next prompts: `/sp.tasks` (generate actionable task breakdown), `/sp.implement` (execute implementation)
- 🧠 Reflection: Plan successfully bridges technology-agnostic spec to concrete Phase II stack implementation with full traceability to FRs and clarifications

## Evaluation notes (flywheel)

- Failure modes observed: None - plan passed constitution compliance check (13/13 principles)
- Graders run and results (PASS/FAIL): Constitution check PASS (all Phase II principles verified)
- Prompt variant (if applicable): Standard /sp.plan workflow with extensive Phase II context
- Next experiment (smallest change to try): Proceed to /sp.tasks to generate executable task breakdown
