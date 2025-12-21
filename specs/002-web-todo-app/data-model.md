# Data Model: Full-Stack Web Todo Application

**Feature**: 002-web-todo-app
**Date**: 2025-12-21
**Purpose**: Define database entities, relationships, and validation rules

## Entity Relationship Diagram

```
┌─────────────────┐           ┌─────────────────┐
│      User       │           │      Task       │
├─────────────────┤           ├─────────────────┤
│ id (PK)         │───────────│ user_id (FK)    │
│ email (UNIQUE)  │   1:N     │ id (PK)         │
│ hashed_password │           │ title           │
│ created_at      │           │ description     │
└─────────────────┘           │ completed       │
                              │ created_at      │
                              │ updated_at      │
                              └─────────────────┘

Relationship: One user has many tasks (1:N)
```

## Entities

### 1. User

**Purpose**: Represents an authenticated user account

**Table Name**: `users`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (used for signin) |
| `hashed_password` | VARCHAR(255) | NOT NULL | Bcrypt-hashed password (never store plain text) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Validation Rules**:
- **Email Format**: Must match regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **Email Uniqueness**: Must be unique across all users (enforced at database level)
- **Password Length**: Minimum 8 characters (validated before hashing)
- **Password Storage**: Must be hashed using bcrypt before storage (never store plain text)

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for fast lookup during signin)

**Security Considerations**:
- Password field named `hashed_password` to prevent accidental exposure of plain text
- Email should be case-insensitive for lookups (convert to lowercase before storage)
- Created_at helps track account age for security audits

**Sample Data**:
```sql
INSERT INTO users (id, email, hashed_password, created_at) VALUES
  ('550e8400-e29b-41d4-a716-446655440000', 'user@example.com', '$2b$12$...', '2025-12-21 10:00:00');
```

---

### 2. Task

**Purpose**: Represents a todo item belonging to a user

**Table Name**: `tasks`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE, NOT NULL | Owner of the task |
| `title` | VARCHAR(1000) | NOT NULL | Task title (required) |
| `description` | TEXT | NULL | Task description (optional, can be empty) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Task creation timestamp |
| `updated_at` | TIMESTAMP | NULL | Last modification timestamp (NULL if never updated) |

**Validation Rules**:
- **Title Required**: Cannot be NULL or empty string or only whitespace
- **Title Length**: Maximum 1000 characters (truncate or reject longer)
- **Description Length**: Maximum 10,000 characters (optional, can be NULL)
- **User Ownership**: `user_id` must reference an existing user
- **Completed Default**: New tasks default to `completed = FALSE`

**Indexes**:
- Primary key index on `id` (automatic)
- Foreign key index on `user_id` (for fast user-specific queries)
- Composite index on `(user_id, completed)` for filtering by status

**Relationships**:
- **Many-to-One with User**: Each task belongs to exactly one user
- **Cascade Delete**: If user is deleted, all their tasks are deleted automatically

**Security Considerations**:
- Foreign key ensures referential integrity (cannot create task for non-existent user)
- API must verify `user_id` matches authenticated user (prevent cross-user access)
- No soft deletes in Phase II (tasks are permanently deleted)

**Sample Data**:
```sql
INSERT INTO tasks (id, user_id, title, description, completed, created_at, updated_at) VALUES
  ('660e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440000',
   'Buy groceries', 'Milk, eggs, bread', FALSE, '2025-12-21 10:05:00', NULL),
  ('770e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440000',
   'Finish project', NULL, TRUE, '2025-12-21 10:10:00', '2025-12-21 11:00:00');
```

---

## Database Schema (SQL DDL)

```sql
-- Enable UUID extension (PostgreSQL specific)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for fast lookups
CREATE UNIQUE INDEX idx_users_email ON users(LOWER(email));

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(1000) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create indexes for efficient queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Add constraint to ensure title is not empty
ALTER TABLE tasks ADD CONSTRAINT chk_title_not_empty
    CHECK (TRIM(title) <> '');
```

---

## SQLModel Class Definitions (Backend)

### User Model (`backend/app/models/user.py`)

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="owner", cascade_delete=True)
```

### Task Model (`backend/app/models/task.py`)

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime
import uuid

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=1000)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship
    owner: User = Relationship(back_populates="tasks")
```

---

## TypeScript Types (Frontend)

### User Type (`frontend/src/lib/types.ts`)

```typescript
export interface User {
  id: string;  // UUID as string
  email: string;
  created_at: string;  // ISO 8601 timestamp
  // Note: hashed_password is never sent to frontend
}
```

### Task Type (`frontend/src/lib/types.ts`)

```typescript
export interface Task {
  id: string;  // UUID as string
  user_id: string;  // UUID as string
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;  // ISO 8601 timestamp
  updated_at: string | null;  // ISO 8601 timestamp
}
```

---

## State Transitions

### Task Lifecycle

```
┌─────────────┐
│   Created   │  (completed = false)
│ (incomplete)│
└──────┬──────┘
       │
       │ User marks complete
       ▼
┌─────────────┐
│  Completed  │  (completed = true)
└──────┬──────┘
       │
       │ User marks incomplete
       ▼
┌─────────────┐
│   Created   │  (completed = false)
└─────────────┘
```

**Rules**:
- Tasks can toggle between `completed = true` and `completed = false` unlimited times
- `updated_at` is set to current timestamp on each state change
- No other states exist in Phase II (no "archived", "deleted", "in_progress")

---

## User Isolation Enforcement

### Database Level

**Foreign Key Constraint**:
```sql
user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
```
- Every task MUST have a valid `user_id`
- If user is deleted, all their tasks are automatically deleted
- Cannot create orphaned tasks

### API Level

**Query Pattern** (always filter by user_id):
```python
# Get all tasks for authenticated user
tasks = session.exec(
    select(Task).where(Task.user_id == current_user.id)
).all()

# Get specific task (verify ownership)
task = session.exec(
    select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
).first()

if not task:
    raise HTTPException(status_code=404, detail="Task not found")
```

**Enforcement Rules**:
- ALL task queries MUST include `user_id` filter
- NEVER query tasks without user context
- Return 403 Forbidden if user tries to access another user's task
- Return 404 if task doesn't exist OR doesn't belong to user (don't leak existence)

---

## Data Validation Summary

| Field | Required | Min Length | Max Length | Format | Unique |
|-------|----------|------------|------------|--------|--------|
| User.email | ✅ | - | 255 | Email regex | ✅ |
| User.hashed_password | ✅ | - | 255 | Bcrypt hash | ❌ |
| Task.title | ✅ | 1 (non-whitespace) | 1000 | Any text | ❌ |
| Task.description | ❌ | - | 10000 | Any text | ❌ |
| Task.completed | ✅ | - | - | Boolean | ❌ |

**Client-Side Validation** (Frontend):
- Email format check before submit
- Password minimum 8 characters
- Task title not empty/whitespace
- Character count warnings for title (approaching 1000) and description (approaching 10000)

**Server-Side Validation** (Backend - REQUIRED):
- Email format validation (don't trust client)
- Email uniqueness check
- Password minimum 8 characters (before hashing)
- Task title not empty/whitespace
- Field length limits enforced
- User ownership verification on all task operations

---

## Migration Strategy (Phase II)

**Initial Setup** (Development):
```python
# In backend/app/database.py or main.py
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)  # Creates all tables
```

**Note**: For Phase II, use `create_all()` for simplicity. For Phase III, migrate to Alembic for schema versioning and migrations.

---

## Summary

- ✅ 2 entities: User, Task
- ✅ 1:N relationship (User → Tasks)
- ✅ User isolation enforced at database (FK) and API (query filters)
- ✅ All fields validated at client and server
- ✅ UUIDs for all primary keys (better security than auto-increment integers)
- ✅ Timestamps for audit trail
- ✅ Cascade delete for data cleanup
- ✅ Indexes for query performance

**Next**: Generate API contracts in `contracts/` directory
