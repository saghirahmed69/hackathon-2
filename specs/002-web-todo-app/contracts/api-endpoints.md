# API Endpoints Contract

**Feature**: 002-web-todo-app
**Date**: 2025-12-21
**Base URL**: `http://localhost:8000` (development), `https://api.yourdomain.com` (production)
**API Version**: v1

## Authentication

All protected endpoints require a valid JWT token in the `Authorization` header:
```
Authorization: Bearer <jwt_token>
```

**Token Format**: JWT (JSON Web Token) issued by Better Auth
**Token Payload**:
```json
{
  "sub": "user-uuid-here",  // User ID
  "email": "user@example.com",
  "exp": 1735000000  // Expiration timestamp
}
```

## Error Response Format

All error responses follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

For validation errors:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

---

## Authentication Endpoints

### POST /api/auth/signup

Create a new user account.

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Validation**:
- `email`: Required, valid email format, max 255 characters
- `password`: Required, minimum 8 characters

**Success Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2025-12-21T10:00:00Z"
}
```

**Error Responses**:
- **400 Bad Request**: Invalid email format or password too short
  ```json
  {
    "detail": "Password must be at least 8 characters"
  }
  ```

- **409 Conflict**: Email already registered
  ```json
  {
    "detail": "Email already registered"
  }
  ```

- **500 Internal Server Error**: Database or server error
  ```json
  {
    "detail": "Internal server error"
  }
  ```

**Mapped to**: User Story 1 (FR-001, FR-002, FR-003, FR-004)

---

### POST /api/auth/signin

Sign in an existing user and receive JWT token.

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Validation**:
- `email`: Required, valid email format
- `password`: Required

**Success Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2025-12-21T10:00:00Z"
  }
}
```

**Error Responses**:
- **401 Unauthorized**: Invalid credentials
  ```json
  {
    "detail": "Invalid email or password"
  }
  ```

- **500 Internal Server Error**: Database or server error
  ```json
  {
    "detail": "Internal server error"
  }
  ```

**Mapped to**: User Story 1 (FR-005, FR-006)

---

### POST /api/auth/logout

Logout the current user (invalidate token on client side).

**Authentication**: Required (Bearer token)

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Successfully logged out"
}
```

**Error Responses**:
- **401 Unauthorized**: Missing or invalid token
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

**Note**: In Phase II, logout is primarily client-side (remove token from storage). Server-side token revocation is out of scope.

**Mapped to**: User Story 1 (FR-009)

---

## Task Management Endpoints

### GET /api/tasks

Retrieve all tasks for the authenticated user.

**Authentication**: Required (Bearer token)

**Query Parameters**: None (future: filtering by `completed` status)

**Success Response** (200 OK):
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-21T10:05:00Z",
    "updated_at": null
  },
  {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Finish project",
    "description": null,
    "completed": true,
    "created_at": "2025-12-21T10:10:00Z",
    "updated_at": "2025-12-21T11:00:00Z"
  }
]
```

**Empty State** (200 OK):
```json
[]
```

**Error Responses**:
- **401 Unauthorized**: Missing or invalid token
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

- **500 Internal Server Error**: Database error
  ```json
  {
    "detail": "Internal server error"
  }
  ```

**Mapped to**: User Story 2 (FR-017, FR-018, FR-020, FR-021)

---

### POST /api/tasks

Create a new task for the authenticated user.

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Request Validation**:
- `title`: Required, non-empty/non-whitespace, max 1000 characters
- `description`: Optional, max 10000 characters

**Success Response** (201 Created):
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "New task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2025-12-21T12:00:00Z",
  "updated_at": null
}
```

**Error Responses**:
- **400 Bad Request**: Validation error
  ```json
  {
    "detail": "Title cannot be empty"
  }
  ```

- **401 Unauthorized**: Missing or invalid token
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

- **500 Internal Server Error**: Database error
  ```json
  {
    "detail": "Internal server error"
  }
  ```

**Mapped to**: User Story 2 (FR-011, FR-012, FR-013, FR-014, FR-015, FR-016)

---

### PATCH /api/tasks/{task_id}

Update an existing task (title, description, or completion status).

**Authentication**: Required (Bearer token)

**Path Parameters**:
- `task_id`: UUID of the task to update

**Request Body** (partial update - all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Request Validation**:
- At least one field must be provided
- `title`: If provided, non-empty/non-whitespace, max 1000 characters
- `description`: If provided, max 10000 characters (can be null to clear)
- `completed`: If provided, must be boolean

**Success Response** (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2025-12-21T10:05:00Z",
  "updated_at": "2025-12-21T12:30:00Z"
}
```

**Error Responses**:
- **400 Bad Request**: Validation error
  ```json
  {
    "detail": "Title cannot be empty"
  }
  ```

- **401 Unauthorized**: Missing or invalid token
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

- **403 Forbidden**: Task belongs to another user
  ```json
  {
    "detail": "Not authorized to update this task"
  }
  ```

- **404 Not Found**: Task doesn't exist or doesn't belong to user
  ```json
  {
    "detail": "Task not found"
  }
  ```

- **500 Internal Server Error**: Database error
  ```json
  {
    "detail": "Internal server error"
  }
  ```

**Mapped to**:
- User Story 3 (FR-024) - Toggle completion
- User Story 4 (FR-022, FR-023, FR-025, FR-026, FR-027, FR-028) - Update title/description

---

### DELETE /api/tasks/{task_id}

Delete a task permanently.

**Authentication**: Required (Bearer token)

**Path Parameters**:
- `task_id`: UUID of the task to delete

**Request Body**: None

**Success Response** (204 No Content):
No response body.

**Error Responses**:
- **401 Unauthorized**: Missing or invalid token
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

- **403 Forbidden**: Task belongs to another user
  ```json
  {
    "detail": "Not authorized to delete this task"
  }
  ```

- **404 Not Found**: Task doesn't exist or doesn't belong to user
  ```json
  {
    "detail": "Task not found"
  }
  ```

- **500 Internal Server Error**: Database error
  ```json
  {
    "detail": "Internal server error"
  }
  ```

**Mapped to**: User Story 5 (FR-029, FR-030, FR-031, FR-032, FR-033)

---

## CORS Configuration

**Allowed Origins** (configurable via environment):
- Development: `http://localhost:3000`
- Production: `https://yourdomain.com`

**Allowed Methods**: `GET`, `POST`, `PATCH`, `DELETE`, `OPTIONS`

**Allowed Headers**: `*` (including `Authorization`, `Content-Type`)

**Allow Credentials**: `true` (for cookies if needed in future)

---

## Rate Limiting (Future - Phase III)

Not implemented in Phase II. Future considerations:
- 100 requests per minute per IP for public endpoints
- 1000 requests per minute per user for authenticated endpoints

---

## API Versioning (Future)

Phase II uses unversioned `/api/` prefix. Future phases may introduce `/api/v2/` for breaking changes.

---

## Testing Endpoints

### Health Check

**GET /health**

**Authentication**: None

**Success Response** (200 OK):
```json
{
  "status": "ok",
  "timestamp": "2025-12-21T12:00:00Z"
}
```

### API Documentation

**GET /docs** - Swagger UI (FastAPI auto-generated)

**GET /redoc** - ReDoc UI (FastAPI auto-generated)

---

## Security Considerations

1. **JWT Secret**: Must be strong, random, stored in environment variable
2. **Password Hashing**: Bcrypt with work factor 12
3. **HTTPS**: Required in production (TLS 1.2+)
4. **Input Validation**: All inputs validated on server (never trust client)
5. **User Isolation**: All task queries filtered by `user_id` from JWT
6. **Error Messages**: Don't leak sensitive information (e.g., don't reveal if email exists during signin)
7. **SQL Injection**: Prevented by SQLModel ORM (parameterized queries)
8. **XSS**: Frontend (React) auto-escapes, backend doesn't render HTML

---

## Summary

| Endpoint | Method | Auth | Purpose | User Story |
|----------|--------|------|---------|------------|
| `/api/auth/signup` | POST | No | Create account | US1 |
| `/api/auth/signin` | POST | No | Get JWT token | US1 |
| `/api/auth/logout` | POST | Yes | Invalidate session | US1 |
| `/api/tasks` | GET | Yes | List user's tasks | US2 |
| `/api/tasks` | POST | Yes | Create new task | US2 |
| `/api/tasks/{id}` | PATCH | Yes | Update task | US3, US4 |
| `/api/tasks/{id}` | DELETE | Yes | Delete task | US5 |

**Total**: 7 endpoints (3 auth, 4 tasks)
**Protected**: 5 endpoints require JWT
**Public**: 2 endpoints (signup, signin)

**Next**: Generate quickstart.md for development and testing
