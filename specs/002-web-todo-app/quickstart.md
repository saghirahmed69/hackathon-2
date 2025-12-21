# Quickstart Guide: Full-Stack Web Todo Application

**Feature**: 002-web-todo-app
**Date**: 2025-12-21
**Purpose**: Step-by-step setup, development, and testing guide

## Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Node.js**: 18 or higher
- **npm** or **yarn**: Latest version
- **Neon PostgreSQL**: Free account at [neon.tech](https://neon.tech)
- **Git**: For version control

### Verify Installations

```bash
python --version  # Should be 3.10+
node --version    # Should be 18+
npm --version     # Should be 9+
```

---

## Part 1: Database Setup (Neon PostgreSQL)

### 1. Create Neon Account

1. Go to [https://neon.tech](https://neon.tech)
2. Sign up for free account
3. Create new project: "todo-app-phase-ii"
4. Note down the connection string (you'll need this)

### 2. Get Connection String

From Neon dashboard:
- Go to your project → "Connection Details"
- Copy the connection string, it looks like:
  ```
  postgresql://user:password@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
  ```

### 3. Modify for AsyncPG

Convert the PostgreSQL connection string to async format:
```
# Original (psycopg2):
postgresql://user:password@host/db

# For AsyncPG (add +asyncpg):
postgresql+asyncpg://user:password@host/db
```

---

## Part 2: Backend Setup (FastAPI)

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate (Linux/macOS):
source venv/bin/activate

# Activate (Windows):
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages**:
- fastapi
- uvicorn[standard]
- sqlmodel
- asyncpg
- python-jose[cryptography]
- passlib[bcrypt]
- python-multipart
- pydantic-settings

### 4. Configure Environment Variables

Create `backend/.env` file:

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

**Security Note**: Generate a strong JWT_SECRET:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Initialize Database

The application will auto-create tables on first run using SQLModel's `create_all()`.

###6. Run Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 7. Test Backend

Open browser: `http://localhost:8000/docs`

You should see FastAPI's Swagger UI with all endpoints documented.

**Quick API Test**:
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok","timestamp":"2025-12-21T12:00:00Z"}
```

---

## Part 3: Frontend Setup (Next.js)

### 1. Navigate to Frontend Directory

Open a NEW terminal (keep backend running):

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

**Expected packages**:
- next (16+)
- react (18+)
- react-dom
- typescript
- tailwindcss
- better-auth
- (and their dependencies)

### 3. Configure Environment Variables

Create `frontend/.env.local` file:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-super-secret-auth-key-change-this-in-production
BETTER_AUTH_URL=http://localhost:3000

# Environment
NODE_ENV=development
```

**Security Note**: Generate a strong BETTER_AUTH_SECRET:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### 4. Run Frontend Server

```bash
npm run dev
```

**Expected output**:
```
▲ Next.js 16.0.0
- Local:        http://localhost:3000
- Environments: .env.local

✓ Ready in 2.5s
```

### 5. Open Application

Open browser: `http://localhost:3000`

You should see the landing page with signin/signup links.

---

## Part 4: Manual Testing Scenarios

### Test Scenario 1: User Registration & Authentication

**Steps**:
1. Navigate to `http://localhost:3000/signup`
2. Enter email: `test@example.com`
3. Enter password: `password123` (min 8 chars)
4. Click "Sign Up"
5. **Expected**: Redirected to signin page with success message
6. Enter same credentials on signin page
7. Click "Sign In"
8. **Expected**: Redirected to `/dashboard` with JWT token stored

**Validation**:
- ✅ Email validation works (try invalid email)
- ✅ Password validation works (try <8 chars)
- ✅ Duplicate email rejected (try signing up again)
- ✅ Invalid credentials rejected (try wrong password)

---

### Test Scenario 2: View and Create Tasks

**Prerequisites**: Must be signed in (complete Scenario 1)

**Steps**:
1. On dashboard (`/dashboard`), observe empty state message
2. Click "Add Task" button
3. Enter title: "Buy groceries"
4. Enter description: "Milk, eggs, bread"
5. Click "Create Task"
6. **Expected**: Task appears in list immediately with:
   - Title: "Buy groceries"
   - Description: "Milk, eggs, bread"
   - Completed: unchecked
   - Creation date shown

7. Create another task:
   - Title: "Finish project"
   - Description: (leave empty)
8. **Expected**: Second task appears with empty description

**Validation**:
- ✅ Empty title rejected (try submitting without title)
- ✅ Tasks display in list/table format
- ✅ Both tasks visible
- ✅ Empty state message disappears after first task

---

### Test Scenario 3: Mark Tasks Complete/Incomplete

**Prerequisites**: Must have created tasks (complete Scenario 2)

**Steps**:
1. Find "Buy groceries" task
2. Click checkbox/toggle to mark complete
3. **Expected**:
   - Task marked as completed (visual indication: strikethrough or color change)
   - Confirmation message shown
   - Change persists after page reload

4. Reload page (`Ctrl+R` or `Cmd+R`)
5. **Expected**: Task still marked as complete

6. Click checkbox again to mark incomplete
7. **Expected**: Task returns to incomplete status

**Validation**:
- ✅ Visual distinction between completed/incomplete
- ✅ Changes persist after reload
- ✅ Confirmation message on each toggle

---

### Test Scenario 4: Update Task Details

**Prerequisites**: Must have created tasks (complete Scenario 2)

**Steps**:
1. Find "Finish project" task
2. Click "Edit" button
3. Update title to: "Complete Phase II project"
4. Add description: "Full-stack web app with auth"
5. Click "Save"
6. **Expected**:
   - Task title updated to "Complete Phase II project"
   - Description now shows "Full-stack web app with auth"
   - Confirmation message shown
   - `updated_at` timestamp updated

7. Click "Edit" on any task
8. Clear the title field
9. Try to save
10. **Expected**: Validation error "Title cannot be empty"

11. Click "Cancel" during edit
12. **Expected**: Task returns to original state without changes

**Validation**:
- ✅ Title updates work
- ✅ Description updates work
- ✅ Empty title validation works
- ✅ Cancel button works
- ✅ Changes persist after reload

---

### Test Scenario 5: Delete Tasks

**Prerequisites**: Must have created tasks (complete Scenario 2)

**Steps**:
1. Find any task
2. Click "Delete" button
3. **Expected**: Confirmation dialog appears
4. Click "Cancel"
5. **Expected**: Task remains in list

6. Click "Delete" again
7. Click "Confirm"
8. **Expected**:
   - Task removed from list immediately
   - Confirmation message shown
   - Task count updates

9. Reload page
10. **Expected**: Deleted task does not reappear

**Validation**:
- ✅ Confirmation dialog appears
- ✅ Cancel works (task not deleted)
- ✅ Confirm works (task deleted)
- ✅ Deletion persists after reload

---

### Test Scenario 6: User Isolation

**Prerequisites**: Need two browser profiles or incognito + normal window

**Steps**:
1. **Window 1**: Sign in as `user1@example.com`, create task "User 1's task"
2. **Window 2**: Sign in as `user2@example.com`, create task "User 2's task"
3. **Window 1**: Refresh and view tasks
4. **Expected**: Only see "User 1's task", NOT "User 2's task"
5. **Window 2**: Refresh and view tasks
6. **Expected**: Only see "User 2's task", NOT "User 1's task"

**Advanced Test** (requires browser DevTools):
1. Window 1: Open DevTools → Network tab
2. Create a task and capture the API request
3. Copy the `task_id` from response
4. Window 2: Open DevTools → Console
5. Try to fetch Window 1's task:
   ```javascript
   fetch('http://localhost:8000/api/tasks/TASK_ID_FROM_WINDOW_1', {
     headers: { 'Authorization': 'Bearer YOUR_TOKEN_FROM_WINDOW_2' }
   }).then(r => r.json()).then(console.log)
   ```
6. **Expected**: 404 Not Found (doesn't reveal task exists)

**Validation**:
- ✅ Each user only sees their own tasks
- ✅ Cross-user access returns 404 (not 403, to avoid leaking existence)
- ✅ No data leakage between users

---

### Test Scenario 7: Authentication Protection

**Steps**:
1. Sign out (click "Logout" button)
2. Try to access `/dashboard` directly in URL bar
3. **Expected**: Redirected to `/signin` page

4. Open DevTools → Console
5. Try to call API without token:
   ```javascript
   fetch('http://localhost:8000/api/tasks').then(r => r.json()).then(console.log)
   ```
6. **Expected**: `{"detail":"Not authenticated"}` (401 error)

7. Close browser and reopen
8. Try to access `/dashboard`
9. **Expected**: Redirected to signin (token not persisted across browser restart in Phase II)

**Validation**:
- ✅ Protected routes require authentication
- ✅ API returns 401 for missing token
- ✅ Logout clears session

---

## Part 5: Development Tips

### Backend Development

**Auto-reload on code changes**:
```bash
uvicorn app.main:app --reload
```

**View API docs**:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Database inspection** (using psql):
```bash
# Connect to Neon database
psql "postgresql://user:password@host/db?sslmode=require"

# List tables
\dt

# View users
SELECT * FROM users;

# View tasks
SELECT * FROM tasks;
```

### Frontend Development

**Clear Next.js cache**:
```bash
rm -rf .next
npm run dev
```

**Build for production**:
```bash
npm run build
npm start
```

**Check TypeScript errors**:
```bash
npm run type-check
```

---

## Part 6: Troubleshooting

### Backend Issues

**Error: "Could not import app.main"**
- Check you're in `backend/` directory
- Check virtual environment is activated
- Run `pip install -r requirements.txt`

**Error: "Connection refused (database)"**
- Check DATABASE_URL is correct in `.env`
- Verify Neon database is active (not suspended)
- Check `+asyncpg` is in connection string

**Error: "JWT decode error"**
- Check JWT_SECRET matches between frontend Better Auth config and backend
- Verify token is being sent in `Authorization: Bearer <token>` header

### Frontend Issues

**Error: "Module not found"**
- Run `npm install`
- Delete `node_modules` and `package-lock.json`, run `npm install` again

**Error: "API request failed"**
- Check NEXT_PUBLIC_API_URL in `.env.local` points to `http://localhost:8000`
- Verify backend is running
- Check browser console for CORS errors

**Error: "Better Auth configuration error"**
- Check BETTER_AUTH_SECRET is set in `.env.local`
- Verify BETTER_AUTH_URL matches your frontend URL

---

## Part 7: Next Steps After Validation

Once all 7 test scenarios pass:

1. ✅ **Phase II Complete**: All core features working
2. ⏭️ **Deploy to Production**:
   - Frontend: Vercel or Netlify
   - Backend: Railway, Render, or AWS
   - Database: Neon production tier

3. ⏭️ **Phase III Planning**: AI chatbot integration, MCP server

---

## Summary Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database tables created in Neon
- [ ] Test Scenario 1: User registration works ✓
- [ ] Test Scenario 2: Task creation works ✓
- [ ] Test Scenario 3: Mark complete/incomplete works ✓
- [ ] Test Scenario 4: Update task details works ✓
- [ ] Test Scenario 5: Delete tasks works ✓
- [ ] Test Scenario 6: User isolation enforced ✓
- [ ] Test Scenario 7: Authentication protection works ✓

**Total Test Scenarios**: 7
**All scenarios must pass** for Phase II completion.

---

**Questions or Issues?** Check `specs/002-web-todo-app/contracts/api-endpoints.md` for API details.
