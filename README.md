# Hackathon II - Evolution of Todo: Phase II

A full-stack web todo application with authentication built using Spec-Driven Development.

## Phase II: Full-Stack Web Application

Phase II extends the console application to a full-stack web platform with user authentication, persistent storage, and REST APIs.

### Technology Stack

**Frontend**:
- Next.js 16+ with App Router
- React 19
- TypeScript
- Tailwind CSS

**Backend**:
- FastAPI (Python 3.10+)
- SQLModel ORM
- Neon Serverless PostgreSQL
- JWT Authentication

### Features

✅ **User Authentication**:
- Sign up with email and password
- Sign in with JWT token issuance
- Logout functionality
- Protected routes

✅ **Task Management**:
- Create tasks with title and description
- View all user's tasks
- Update task details
- Mark tasks as complete/incomplete
- Delete tasks

✅ **Multi-User Support**:
- User isolation (each user sees only their own tasks)
- Database-level and API-level enforcement
- Secure password hashing (bcrypt)

### Project Structure

```
hackathon-2/
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── models/              # SQLModel database models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/            # Business logic
│   │   ├── api/                 # API route handlers
│   │   ├── middleware/          # Authentication middleware
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database connection
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                    # Next.js frontend
│   ├── src/
│   │   ├── app/                 # Next.js 16+ App Router
│   │   ├── components/          # React components
│   │   └── lib/                 # Utilities and types
│   ├── package.json
│   ├── tsconfig.json
│   └── .env.local.example
│
└── specs/                       # Design documentation
    └── 002-web-todo-app/
        ├── spec.md              # Feature specification
        ├── plan.md              # Implementation plan
        ├── tasks.md             # Task breakdown
        ├── data-model.md        # Entity specifications
        ├── contracts/           # API contracts
        ├── research.md          # Technology decisions
        └── quickstart.md        # Setup and testing guide
```

### Quick Start

#### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Neon PostgreSQL account (free tier at [neon.tech](https://neon.tech))

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection string and JWT secret

# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API documentation (Swagger): `http://localhost:8000/docs`

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local if needed (default API URL is http://localhost:8000)

# Run frontend server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### Environment Variables

#### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/db?sslmode=require

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Generate Secure JWT_SECRET**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Frontend (.env.local)

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-super-secret-auth-key-change-this-in-production
BETTER_AUTH_URL=http://localhost:3000

# Environment
NODE_ENV=development
```

**Generate Secure BETTER_AUTH_SECRET**:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

#### Database Setup

1. Create a Neon PostgreSQL account at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Update `backend/.env` with the connection string (make sure to use `postgresql+asyncpg://` prefix)
5. Database tables will be created automatically on first run

### Usage

1. **Sign Up**: Navigate to `/signup` and create an account
2. **Sign In**: Navigate to `/signin` and log in with your credentials
3. **Dashboard**: View and manage your tasks at `/dashboard`
4. **Create Task**: Click "Add Task" and fill in title and description
5. **Update Task**: Click "Edit" on any task to modify it
6. **Toggle Complete**: Check/uncheck the checkbox to mark tasks complete/incomplete
7. **Delete Task**: Click "Delete" and confirm to remove a task

### Development Approach

This project follows **Spec-Driven Development (SDD)** methodology:

1. ✅ **Specification** (`spec.md`) - Complete requirements and user stories
2. ✅ **Planning** (`plan.md`) - Architecture and technology decisions
3. ✅ **Task Breakdown** (`tasks.md`) - Detailed implementation tasks
4. ✅ **Implementation** - All code generated by Claude Code
5. ⏭️ **Testing** - Manual testing via quickstart.md scenarios
6. ⏭️ **Deployment** - Ready for production deployment

### Troubleshooting

#### Backend Issues

**Error: "Could not import app.main"**
- Verify you're in the `backend/` directory
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Error: "Connection refused (database)"**
- Check `DATABASE_URL` is correct in `.env`
- Verify Neon database is active (not suspended)
- Ensure `+asyncpg` is in the connection string: `postgresql+asyncpg://...`

**Error: "JWT decode error"**
- Check `JWT_SECRET` matches between frontend and backend
- Verify token is sent in `Authorization: Bearer <token>` header

**Error: "CORS error"**
- Check `FRONTEND_URL` in backend `.env` matches frontend URL
- Verify CORS middleware is enabled in `backend/app/main.py`

#### Frontend Issues

**Error: "Module not found"**
- Run `npm install`
- Delete `node_modules/` and `package-lock.json`, then run `npm install` again

**Error: "API request failed"**
- Check `NEXT_PUBLIC_API_URL` in `.env.local` points to `http://localhost:8000`
- Verify backend server is running
- Check browser console for CORS errors

**Error: "Better Auth configuration error"**
- Check `BETTER_AUTH_SECRET` is set in `.env.local`
- Verify `BETTER_AUTH_URL` matches your frontend URL

**Build Errors**
- Run `npm run type-check` to see TypeScript errors
- Clear Next.js cache: `rm -rf .next` and restart

#### Database Issues

**Tables not created**
- Check DATABASE_URL connection string
- Verify Neon project is active
- Check backend logs for SQLModel errors

**User data not persisting**
- Verify you're using Neon PostgreSQL (not in-memory)
- Check database connection in Neon dashboard

### Testing

Comprehensive manual test scenarios are documented in `specs/002-web-todo-app/quickstart.md`:

1. User Registration & Authentication
2. View and Create Tasks
3. Mark Tasks Complete/Incomplete
4. Update Task Details
5. Delete Tasks
6. User Isolation
7. Authentication Protection

### API Endpoints

**Authentication**:
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Sign in and get JWT token
- `POST /api/auth/logout` - Logout (client-side token removal)

**Tasks** (all require JWT authentication):
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/{id}` - Update task (title, description, or completion status)
- `DELETE /api/tasks/{id}` - Delete task

**API Documentation**:
- Interactive Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Complete specification: `specs/002-web-todo-app/contracts/api-endpoints.md`

### Security

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ User isolation at database level (foreign keys)
- ✅ User isolation at API level (ownership verification)
- ✅ CORS configuration
- ✅ Environment variables for secrets
- ✅ Input validation (client and server)
- ✅ SQL injection protection (ORM)
- ✅ XSS protection (React auto-escaping)

### Deployment

**Frontend**: Deploy to [Vercel](https://vercel.com) or [Netlify](https://netlify.com)
**Backend**: Deploy to [Railway](https://railway.app), [Render](https://render.com), or AWS
**Database**: Neon PostgreSQL (already cloud-hosted)

Deployment guides coming in Phase III.

### Phase History

- **Phase I**: Console-based Python application with in-memory storage (completed)
- **Phase II**: Full-stack web application with authentication and PostgreSQL (current)
- **Phase III**: AI chatbot integration with OpenAI API and MCP (planned)
- **Phase IV**: Cloud-native architecture (planned)
- **Phase V**: Kubernetes deployment (planned)

### Documentation

For detailed documentation, see the `specs/002-web-todo-app/` directory:

- `spec.md` - Complete feature specification with user stories
- `plan.md` - Implementation architecture and design decisions
- `tasks.md` - Detailed task breakdown (148 tasks)
- `data-model.md` - Database entity specifications
- `contracts/api-endpoints.md` - Complete API documentation
- `research.md` - Technology research and decisions
- `quickstart.md` - Comprehensive setup and testing guide

### License

This project was built as part of Hackathon II using the Specify framework and Claude Code.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
