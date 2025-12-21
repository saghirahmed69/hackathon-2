# Research: Full-Stack Web Todo Application

**Feature**: 002-web-todo-app
**Date**: 2025-12-21
**Purpose**: Document technology decisions and implementation patterns for Phase II

## Technology Stack Research

### 1. Next.js 16+ App Router with Authentication

**Decision**: Use Next.js 16+ with App Router for frontend application

**Rationale**:
- **App Router Benefits**: Server Components by default reduce client-side JavaScript, improve performance
- **Built-in Features**: File-based routing, middleware support for route protection, API routes (though we'll use separate FastAPI backend)
- **Better Auth Compatibility**: Better Auth v1.0+ has first-class Next.js App Router support
- **TypeScript Support**: Excellent TypeScript integration for type safety
- **Production Ready**: Vercel deployment optimized, edge runtime support

**Alternatives Considered**:
- **Next.js Pages Router**: Older pattern, less performant, migrating to App Router is recommended
- **Create React App**: No SSR/SSG, no built-in routing, requires additional libraries
- **Vite + React Router**: Faster dev server but less opinionated, no SSR out of box

**Implementation Pattern**:
- Use Server Components for static pages (landing, signup, signin forms)
- Use Client Components only where interactivity needed (forms with state, task list with real-time updates)
- Middleware at `src/middleware.ts` for route protection (redirect unauthenticated users)
- Environment variables via `.env.local` (not committed to git)

---

### 2. Better Auth for Authentication

**Decision**: Use Better Auth with JWT token strategy

**Rationale**:
- **Next.js First**: Designed specifically for Next.js App Router
- **JWT Support**: Issues JWT tokens that can be verified by separate backend
- **Secure Defaults**: HTTP-only cookies, CSRF protection, secure password hashing (bcrypt)
- **TypeScript Native**: Full TypeScript support with type inference
- **Minimal Configuration**: Convention over configuration approach

**Alternatives Considered**:
- **NextAuth.js (Auth.js)**: More complex, heavier, OAuth-focused (overkill for email/password)
- **Clerk**: Third-party SaaS, vendor lock-in, costs money at scale
- **Custom JWT Implementation**: Reinventing wheel, security risks, more code to maintain

**Implementation Pattern**:
- Better Auth configured in `src/lib/auth.ts`
- Email/password provider enabled
- JWT tokens stored in HTTP-only cookies (secure, not accessible to JavaScript)
- Token includes user ID claim for backend verification
- Signin/signup endpoints provided by Better Auth
- Frontend calls Better Auth API, receives token, redirects to dashboard

**Integration with Backend**:
- Frontend sends JWT token in `Authorization: Bearer <token>` header
- Backend verifies JWT signature using shared secret (from environment variable)
- Backend extracts user ID from token payload for database queries

---

### 3. FastAPI Backend with SQLModel

**Decision**: Use FastAPI with SQLModel ORM for backend API

**Rationale**:
- **FastAPI Benefits**: High performance (async), automatic OpenAPI docs, Pydantic validation, Python 3.10+ type hints
- **SQLModel**: Combines SQLAlchemy (ORM) + Pydantic (validation), single model definition for DB and API
- **Type Safety**: Full type checking, reduces runtime errors
- **Async Support**: Native async/await for database operations (better concurrency)
- **Modern Python**: Leverages latest Python features

**Alternatives Considered**:
- **Django + DRF**: Heavier, more opinionated, ORM separate from serializers (duplicate definitions)
- **Flask + SQLAlchemy**: Synchronous by default, less modern, more boilerplate
- **Raw SQL**: No ORM protection, SQL injection risks, more code to maintain

**Implementation Pattern**:
- Models in `app/models/` (User, Task) using SQLModel
- Schemas in `app/schemas/` for request/response DTOs (Pydantic)
- Services in `app/services/` for business logic (auth, task CRUD)
- Routes in `app/api/` for HTTP endpoints
- Dependency injection for database sessions
- Middleware for JWT verification on protected routes

---

### 4. JWT Verification in FastAPI

**Decision**: Use `python-jose[cryptography]` for JWT verification with custom middleware

**Rationale**:
- **python-jose**: Industry standard JWT library for Python, secure, well-maintained
- **Cryptography**: Uses cryptography library (not pure Python) for performance and security
- **FastAPI Integration**: Works well with dependency injection pattern
- **Shared Secret**: Backend verifies tokens using same secret as Better Auth (via environment variable)

**Alternatives Considered**:
- **PyJWT**: Less features, requires more manual configuration
- **Custom Implementation**: Security risks, not recommended

**Implementation Pattern**:
- Middleware in `app/middleware/jwt_middleware.py`
- Dependency `get_current_user()` extracts and verifies JWT from `Authorization` header
- Protected routes use dependency: `current_user: User = Depends(get_current_user)`
- Invalid/missing tokens return 401 Unauthorized
- User ID from token used to query database

---

### 5. Neon Serverless PostgreSQL

**Decision**: Use Neon PostgreSQL as database provider

**Rationale**:
- **Serverless**: Auto-scaling, pay-per-use, no server management
- **PostgreSQL Compatible**: Standard PostgreSQL wire protocol, works with any PostgreSQL client
- **Free Tier**: Generous free tier for development/small projects
- **Fast Cold Starts**: Optimized for serverless workloads
- **Branching**: Database branching for development (like Git for databases)

**Alternatives Considered**:
- **Supabase**: More features (auth, storage) but we only need database
- **AWS RDS**: More expensive, requires more configuration
- **Self-hosted PostgreSQL**: Infrastructure management overhead

**Implementation Pattern**:
- Connection string from environment variable `DATABASE_URL`
- SQLModel `create_engine()` with async driver: `asyncpg`
- Connection pooling handled by SQLModel/SQLAlchemy
- Database migrations: Use SQLModel's `SQLModel.metadata.create_all()` for Phase II (Alembic for Phase III)

---

### 6. Monorepo Structure

**Decision**: Monorepo with `frontend/` and `backend/` directories at repository root

**Rationale**:
- **Simplicity**: Single repository, single PR workflow, easier to coordinate changes
- **Code Sharing**: Can share TypeScript types between frontend/backend if needed
- **Development**: Run both services from single repository
- **Deployment**: Can deploy separately (frontend to Vercel, backend to Railway/Render)

**Alternatives Considered**:
- **Separate Repositories**: More complex coordination, harder to keep in sync
- **Nested Structure**: `apps/frontend`, `apps/backend` - overkill for 2 projects

**Implementation Pattern**:
- `frontend/` - Complete Next.js application with its own `package.json`
- `backend/` - Complete FastAPI application with its own `requirements.txt`
- Root `.gitignore` covers both Python and Node.js patterns
- Separate README sections for frontend and backend setup

---

### 7. Environment Variable Management

**Decision**: Use `.env` files with `.example` templates, never commit secrets

**Rationale**:
- **Security**: Secrets not in version control
- **Portability**: Different environments (dev, staging, prod) use different values
- **Convention**: Industry standard approach

**Implementation Pattern**:

**Backend** (`backend/.env.example`):
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

**Frontend** (`frontend/.env.local.example`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

**Naming Conventions**:
- `NEXT_PUBLIC_*` - Exposed to browser (use for non-sensitive config only)
- Other variables - Server-side only (not exposed to browser)

---

### 8. Password Hashing

**Decision**: Use `passlib` with `bcrypt` for password hashing

**Rationale**:
- **Passlib**: Python password hashing library, supports multiple algorithms
- **Bcrypt**: Industry standard, slow by design (resistant to brute force), salted automatically
- **Better Auth Compatibility**: Better Auth uses bcrypt, backend should match for potential future migration

**Alternatives Considered**:
- **Argon2**: More modern, but Better Auth uses bcrypt
- **PBKDF2**: Older, less resistant to GPU attacks

**Implementation Pattern**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash(plain_password)

# Verify password
is_valid = pwd_context.verify(plain_password, hashed_password)
```

---

### 9. CORS Configuration

**Decision**: Configure CORS in FastAPI to allow frontend origin

**Rationale**:
- **Development**: Frontend (localhost:3000) needs to call backend (localhost:8000)
- **Production**: Frontend domain needs to call backend domain
- **Security**: Restrict to specific origins, not wildcard `*`

**Implementation Pattern**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 10. Error Handling Strategy

**Decision**: Consistent error response format across all API endpoints

**Rationale**:
- **Predictability**: Frontend knows how to parse errors
- **Debugging**: Clear error messages in development
- **Security**: Don't leak sensitive info in production

**Implementation Pattern**:
```python
# Error response schema
{
    "detail": "Error message here",
    "error_code": "INVALID_CREDENTIALS",  # Optional
    "field_errors": {  # Optional, for validation errors
        "email": ["Invalid email format"]
    }
}
```

**HTTP Status Codes**:
- `200 OK` - Successful GET, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Valid token but insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server errors

---

## Summary

All technology decisions align with Phase II Constitution requirements:
- ✅ Full-stack web application (Next.js + FastAPI)
- ✅ Authentication via Better Auth with JWT
- ✅ Persistent storage in Neon PostgreSQL
- ✅ Clean architecture with clear separation
- ✅ User isolation enforced at database and API levels
- ✅ Environment variables for all secrets
- ✅ No manual coding (all patterns support code generation)

**Next Steps**: Proceed to Phase 1 - Design (data-model.md, contracts/, quickstart.md)
