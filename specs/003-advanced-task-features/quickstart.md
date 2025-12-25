# Quickstart Testing Guide - Phase III: Advanced Task Features

**Feature Branch**: `003-advanced-task-features`
**Created**: 2025-12-26
**Purpose**: Manual testing guide for validating all 7 user stories and 20 success criteria

---

## Prerequisites

Before running these tests, ensure:

1. **Database Migration Applied**:
   ```bash
   # Execute the migration script to add new columns
   cd backend
   python app/migrations/add_advanced_features.py
   ```

2. **Dependencies Installed**:
   ```bash
   # Backend dependencies (including python-dateutil)
   cd backend
   pip install -r requirements.txt

   # Frontend dependencies
   cd frontend
   npm install
   ```

3. **Services Running**:
   ```bash
   # Terminal 1: Start backend
   cd backend
   uvicorn app.main:app --reload
   # Backend should be available at http://localhost:8000

   # Terminal 2: Start frontend
   cd frontend
   npm run dev
   # Frontend should be available at http://localhost:3000
   ```

4. **Test Account**:
   - Navigate to http://localhost:3000/signup
   - Create a test account or use existing credentials
   - Sign in at http://localhost:3000/signin

---

## Testing Approach

- **Test each user story independently** - Each story can be validated on its own
- **Test in priority order** - Start with P1 (MVP) features, then P2, then P3
- **Check visual indicators** - Verify all UI elements display correctly
- **Test edge cases** - Verify error handling and boundary conditions
- **Verify backward compatibility** - Ensure Phase II features still work

---

## User Story 1: Task Priority Management (P1 - MVP)

**Goal**: Verify priority assignment, visual indicators, and validation

### Test Scenario 1.1: Create Task with Priority

**Steps**:
1. Navigate to dashboard (http://localhost:3000/dashboard)
2. In the "Create New Task" form (left panel):
   - Enter title: "High priority task"
   - Leave description empty
   - Select priority: **High**
   - Leave due date empty
   - Click "Create Task"

**Expected Result**:
- ✅ Task appears in task list (right panel)
- ✅ Task displays **red priority badge** with "🔴 High" text
- ✅ Task title is "High priority task"
- ✅ Task is unchecked (pending status)

---

### Test Scenario 1.2: Create Tasks with All Priority Levels

**Steps**:
1. Create task with:
   - Title: "Medium priority task"
   - Priority: **Medium**
2. Create task with:
   - Title: "Low priority task"
   - Priority: **Low**

**Expected Result**:
- ✅ High priority task shows **red badge** (🔴 High)
- ✅ Medium priority task shows **yellow badge** (🟡 Medium)
- ✅ Low priority task shows **green badge** (🟢 Low)
- ✅ All three badges are clearly distinguishable by color and icon

---

### Test Scenario 1.3: Edit Task Priority

**Steps**:
1. Find the "Low priority task" in the list
2. Click the **Edit** button (pencil icon)
3. Change priority dropdown to **High**
4. Click "Save"

**Expected Result**:
- ✅ Task updates immediately
- ✅ Badge changes from green (🟢 Low) to red (🔴 High)
- ✅ Updated timestamp appears in task details

---

### Test Scenario 1.4: Priority Validation

**Steps**:
1. Open browser developer tools (F12) → Network tab
2. Try to create a task with invalid priority via API:
   ```bash
   # Use curl or Postman to send request
   curl -X POST http://localhost:8000/api/tasks \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Invalid priority","priority":"urgent"}'
   ```

**Expected Result**:
- ✅ API returns **HTTP 400 Bad Request**
- ✅ Error message indicates invalid priority value
- ✅ Task is NOT created in database

---

### Test Scenario 1.5: Priority Default Value

**Steps**:
1. Check the priority dropdown in the create form

**Expected Result**:
- ✅ Priority dropdown defaults to **Medium**

---

## User Story 2: Task Due Dates and Scheduling (P1 - MVP)

**Goal**: Verify due date assignment, overdue detection, and visual indicators

### Test Scenario 2.1: Create Task with Future Due Date

**Steps**:
1. Create a new task:
   - Title: "Future deadline task"
   - Description: "Due in 3 days"
   - Priority: Medium
   - Due Date: Select a date **3 days from today** at 5:00 PM
   - Click "Create Task"

**Expected Result**:
- ✅ Task appears in list
- ✅ Task displays **blue due date badge** with "📅" icon
- ✅ Badge shows date in format "Dec 29, 2025, 5:00 PM" (with time)
- ✅ Task has no overdue or "due today" indicator

---

### Test Scenario 2.2: Create Task with Due Date (Date Only)

**Steps**:
1. Create a new task:
   - Title: "Date-only deadline"
   - Due Date: Select a date **1 week from today** (don't set time)

**Expected Result**:
- ✅ Task displays due date badge
- ✅ Badge shows date in format "Jan 2, 2026" (no time shown)

---

### Test Scenario 2.3: Create Overdue Task

**Steps**:
1. Create a new task:
   - Title: "Overdue task"
   - Due Date: Select **yesterday's date**
   - Click "Create Task"

**Expected Result**:
- ✅ Task appears immediately with **red border and red background** (border-red-300 bg-red-50)
- ✅ Due date badge is **red** with "⚠️ Overdue" text
- ✅ Badge shows the past date
- ✅ Task stands out visually from non-overdue tasks

---

### Test Scenario 2.4: Create Task Due Today

**Steps**:
1. Create a new task:
   - Title: "Due today task"
   - Due Date: Select **today's date** at 11:59 PM
   - Click "Create Task"

**Expected Result**:
- ✅ Task appears with **yellow border and yellow background** (border-yellow-300 bg-yellow-50)
- ✅ Due date badge is **yellow** with "📅 Due Today" text
- ✅ Badge shows today's date and time

---

### Test Scenario 2.5: Create Task Without Due Date

**Steps**:
1. Create a new task:
   - Title: "No deadline task"
   - Priority: Low
   - Leave due date empty
   - Click "Create Task"

**Expected Result**:
- ✅ Task is created successfully
- ✅ Task shows priority badge only (no due date badge)
- ✅ Task has normal border (no overdue/today coloring)

---

### Test Scenario 2.6: Edit Due Date

**Steps**:
1. Find "No deadline task" from previous test
2. Click **Edit** button
3. Set due date to **tomorrow** at 2:00 PM
4. Click "Save"

**Expected Result**:
- ✅ Task updates immediately
- ✅ Blue due date badge appears showing tomorrow's date and time
- ✅ Task maintains normal border (not overdue or due today)

---

### Test Scenario 2.7: Remove Due Date

**Steps**:
1. Edit "Future deadline task"
2. Click **Clear** button next to due date picker
3. Click "Save"

**Expected Result**:
- ✅ Task updates immediately
- ✅ Due date badge disappears
- ✅ Task reverts to normal border (no coloring)

---

### Test Scenario 2.8: Complete Overdue Task

**Steps**:
1. Find the "Overdue task" (with red border)
2. Click the **checkbox** to mark complete

**Expected Result**:
- ✅ Task title gets strikethrough
- ✅ Task text turns gray
- ✅ **Red border and background disappear** (completed tasks don't show overdue indicator)
- ✅ Due date badge remains visible but no longer shows "⚠️ Overdue"

---

### Test Scenario 2.9: Invalid Date Format

**Steps**:
1. Using API or browser console, attempt to set invalid date:
   ```bash
   curl -X PATCH http://localhost:8000/api/tasks/TASK_ID \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"due_date":"invalid-date"}'
   ```

**Expected Result**:
- ✅ API returns **HTTP 400 Bad Request**
- ✅ Error message indicates invalid date format
- ✅ Task due date is unchanged

---

## User Story 3: Search Tasks by Keyword (P2)

**Goal**: Verify real-time search, case-insensitivity, and substring matching

### Test Scenario 3.1: Setup - Create Test Data

**Steps**:
1. Create the following tasks (if not already present):
   - "Write project documentation" (description: "Complete API docs and user guide")
   - "Review pull requests" (description: "Check code quality")
   - "Meeting with team" (description: "Discuss project timeline")
   - "Buy groceries" (description: "Milk, eggs, bread")

---

### Test Scenario 3.2: Search by Title (Exact Word)

**Steps**:
1. In the search bar at top of task list, type: **project**
2. Wait 300ms (debounce delay)

**Expected Result**:
- ✅ Only 2 tasks displayed:
  - "Write project documentation"
  - "Meeting with team" (matches "project" in description)
- ✅ Other tasks hidden
- ✅ Search triggered after stopping typing (debounced)

---

### Test Scenario 3.3: Search by Title (Case-Insensitive)

**Steps**:
1. Clear search field
2. Type: **PROJECT** (all uppercase)
3. Wait 300ms

**Expected Result**:
- ✅ Same 2 tasks displayed as Test 3.2
- ✅ Search is case-insensitive

---

### Test Scenario 3.4: Search by Description

**Steps**:
1. Clear search
2. Type: **code**
3. Wait 300ms

**Expected Result**:
- ✅ Only "Review pull requests" displayed (matches "code" in description)

---

### Test Scenario 3.5: Search with Partial Match

**Steps**:
1. Clear search
2. Type: **doc**
3. Wait 300ms

**Expected Result**:
- ✅ "Write project documentation" displayed
- ✅ Partial word matches work (doc matches documentation)

---

### Test Scenario 3.6: Search with No Results

**Steps**:
1. Clear search
2. Type: **xyz12345**
3. Wait 300ms

**Expected Result**:
- ✅ Task list shows empty state
- ✅ Message displays "No tasks found"
- ✅ No error occurs

---

### Test Scenario 3.7: Clear Search

**Steps**:
1. With search active showing filtered results
2. Click the **Clear** button (X icon) in search bar

**Expected Result**:
- ✅ All tasks reappear immediately
- ✅ Search field is empty

---

### Test Scenario 3.8: Real-Time Debounced Search

**Steps**:
1. Clear search
2. Type slowly: **m** (wait 100ms) **e** (wait 100ms) **e** (wait 100ms) **t**
3. Stop typing for 300ms

**Expected Result**:
- ✅ Search does NOT trigger after each letter
- ✅ Search triggers once, 300ms after typing "meet"
- ✅ "Meeting with team" task appears
- ✅ Network tab shows only 1 API request (not 4)

---

### Test Scenario 3.9: Search with Special Characters

**Steps**:
1. Create task: "Calculate 10% discount"
2. Search for: **10%**

**Expected Result**:
- ✅ Task "Calculate 10% discount" appears
- ✅ Special character % is treated as literal
- ✅ No SQL errors occur

---

## User Story 4: Filter Tasks by Status, Priority, and Date (P2)

**Goal**: Verify filtering by multiple criteria and filter combinations

### Test Scenario 4.1: Setup - Create Test Data

**Steps**:
1. Ensure you have tasks with varied properties:
   - At least 2 completed tasks
   - At least 3 pending tasks
   - At least 1 high, 1 medium, 1 low priority task
   - At least 1 overdue task
   - At least 1 task due today

---

### Test Scenario 4.2: Filter by Status - Pending

**Steps**:
1. Clear all filters (click "Clear all" if any filters active)
2. In filter panel, select Status: **Pending**

**Expected Result**:
- ✅ Only unchecked (incomplete) tasks displayed
- ✅ Completed tasks hidden
- ✅ Filter updates within 2 seconds

---

### Test Scenario 4.3: Filter by Status - Completed

**Steps**:
1. Change Status filter to: **Completed**

**Expected Result**:
- ✅ Only checked (completed) tasks displayed
- ✅ All completed tasks have strikethrough text
- ✅ Pending tasks hidden

---

### Test Scenario 4.4: Filter by Priority

**Steps**:
1. Clear all filters
2. Select Priority: **High**

**Expected Result**:
- ✅ Only tasks with red priority badge (🔴 High) displayed
- ✅ Medium and low priority tasks hidden

---

### Test Scenario 4.5: Filter by Due Date - Overdue

**Steps**:
1. Clear all filters
2. Select Due Date: **Overdue**

**Expected Result**:
- ✅ Only tasks with due dates in the past displayed
- ✅ Tasks should have red border/background and "⚠️ Overdue" badge
- ✅ Tasks without due dates are hidden
- ✅ Future tasks are hidden

---

### Test Scenario 4.6: Filter by Due Date - Due Today

**Steps**:
1. Change Due Date filter to: **Due Today**

**Expected Result**:
- ✅ Only tasks with today's date displayed
- ✅ Tasks should have yellow border/background and "📅 Due Today" badge
- ✅ Overdue and future tasks hidden

---

### Test Scenario 4.7: Filter by Due Date - Upcoming

**Steps**:
1. Change Due Date filter to: **Upcoming**

**Expected Result**:
- ✅ Only tasks with future due dates displayed (tomorrow and beyond)
- ✅ Overdue and today tasks hidden
- ✅ Tasks without due dates hidden

---

### Test Scenario 4.8: Combine Multiple Filters

**Steps**:
1. Clear all filters
2. Set Status: **Pending**
3. Set Priority: **High**
4. Set Due Date: **Overdue**

**Expected Result**:
- ✅ Only tasks matching ALL THREE criteria displayed:
  - Incomplete (not checked)
  - High priority (red badge)
  - Due date in past (red border, overdue badge)
- ✅ Tasks missing any criterion are hidden

---

### Test Scenario 4.9: Filter with Zero Results

**Steps**:
1. Set filters that match no tasks:
   - Status: **Completed**
   - Priority: **High**
   - Due Date: **Due Today**
   (Assuming you don't have completed high-priority tasks due today)

**Expected Result**:
- ✅ Task list shows empty state
- ✅ Message displays "No tasks match your filters"
- ✅ "Clear all" button is visible

---

### Test Scenario 4.10: Clear All Filters

**Steps**:
1. With multiple filters active
2. Click **Clear all** button in filter panel

**Expected Result**:
- ✅ All filters reset to "All"
- ✅ All tasks reappear
- ✅ "Clear all" button disappears (no active filters)

---

### Test Scenario 4.11: Combine Search and Filters

**Steps**:
1. Clear all filters
2. Search for: **project**
3. Set filter Priority: **High**

**Expected Result**:
- ✅ Only tasks containing "project" AND having high priority are shown
- ✅ Both search and filter apply together

---

## User Story 5: Sort Tasks by Multiple Criteria (P3)

**Goal**: Verify sorting by due date, priority, and title with ascending/descending order

### Test Scenario 5.1: Setup - Create Test Data

**Steps**:
1. Ensure you have tasks with:
   - Different due dates (past, today, tomorrow, next week, none)
   - Different priorities (high, medium, low)
   - Different titles (A-Z range)

---

### Test Scenario 5.2: Sort by Due Date - Ascending

**Steps**:
1. Clear all filters and search
2. In sort controls (top right), select Sort by: **Due Date**
3. Ensure sort order arrow points UP (ascending)

**Expected Result**:
- ✅ Tasks ordered from earliest to latest due date
- ✅ Tasks WITHOUT due dates appear at the END of the list
- ✅ Order updates within 1 second

---

### Test Scenario 5.3: Sort by Due Date - Descending

**Steps**:
1. Click the sort order toggle button (up/down arrow)
2. Arrow should now point DOWN (descending)

**Expected Result**:
- ✅ Tasks ordered from latest to earliest due date
- ✅ Tasks WITHOUT due dates appear at the START of the list
- ✅ Order reverses immediately

---

### Test Scenario 5.4: Sort by Priority - Descending

**Steps**:
1. Change Sort by to: **Priority**
2. Set sort order to: **Descending** (down arrow)

**Expected Result**:
- ✅ Tasks ordered: **High → Medium → Low**
- ✅ All high priority tasks appear first
- ✅ All medium priority tasks appear second
- ✅ All low priority tasks appear last

---

### Test Scenario 5.5: Sort by Priority - Ascending

**Steps**:
1. Toggle sort order to: **Ascending** (up arrow)

**Expected Result**:
- ✅ Tasks ordered: **Low → Medium → High**
- ✅ Order reverses from previous test

---

### Test Scenario 5.6: Sort by Title - Ascending (A-Z)

**Steps**:
1. Change Sort by to: **Title**
2. Set sort order to: **Ascending**

**Expected Result**:
- ✅ Tasks ordered alphabetically A-Z by title
- ✅ Case-insensitive sorting (e.g., "apple" and "Apple" treated equally)
- ✅ Numbers sorted before letters

---

### Test Scenario 5.7: Sort by Title - Descending (Z-A)

**Steps**:
1. Toggle sort order to: **Descending**

**Expected Result**:
- ✅ Tasks ordered alphabetically Z-A
- ✅ Order reverses from previous test

---

### Test Scenario 5.8: Sort with Active Filters

**Steps**:
1. Set filter Status: **Pending**
2. Set sort by: **Due Date**, order: **Ascending**

**Expected Result**:
- ✅ Only pending tasks shown (filter applied)
- ✅ Pending tasks sorted by due date ascending
- ✅ Completed tasks remain hidden

---

### Test Scenario 5.9: Reset to Default Sort

**Steps**:
1. Change Sort by to: **Default**

**Expected Result**:
- ✅ Tasks return to creation order (newest first, based on created_at)
- ✅ Sort order toggle button disappears

---

## User Story 6: Recurring Tasks (P3)

**Goal**: Verify recurring task creation, completion, and automatic regeneration

### Test Scenario 6.1: Create Daily Recurring Task

**Steps**:
1. Create a new task:
   - Title: "Daily standup"
   - Description: "Morning team sync"
   - Priority: Medium
   - Due Date: **Today** at 9:00 AM
   - Check "Recurring task" checkbox
   - Select recurrence pattern: **Daily**
   - Click "Create Task"

**Expected Result**:
- ✅ Task appears in list
- ✅ Task shows **purple recurring badge** with "🔁 daily" text
- ✅ Task shows due date badge with today's date and 9:00 AM

---

### Test Scenario 6.2: Complete Daily Recurring Task

**Steps**:
1. Find "Daily standup" task
2. Click checkbox to mark complete
3. Wait 3 seconds

**Expected Result**:
- ✅ Original task is marked complete (strikethrough, gray text)
- ✅ NEW task appears in list with title "Daily standup"
- ✅ New task is unchecked (pending)
- ✅ New task has due date of **tomorrow at 9:00 AM** (+1 day)
- ✅ New task has recurring badge "🔁 daily"
- ✅ New task has same description and priority

---

### Test Scenario 6.3: Create Weekly Recurring Task

**Steps**:
1. Create a new task:
   - Title: "Weekly report"
   - Due Date: **Next Monday** at 5:00 PM
   - Check "Recurring task"
   - Select pattern: **Weekly**
   - Click "Create Task"

**Expected Result**:
- ✅ Task shows recurring badge "🔁 weekly"

---

### Test Scenario 6.4: Complete Weekly Recurring Task

**Steps**:
1. Mark "Weekly report" complete
2. Wait 3 seconds

**Expected Result**:
- ✅ Original task marked complete
- ✅ New task created with due date **7 days later** (next Monday +1 week at 5:00 PM)
- ✅ New task has recurring badge "🔁 weekly"

---

### Test Scenario 6.5: Create Monthly Recurring Task

**Steps**:
1. Create a new task:
   - Title: "Monthly review"
   - Due Date: **1st of next month** at 10:00 AM
   - Check "Recurring task"
   - Select pattern: **Monthly**

**Expected Result**:
- ✅ Task shows recurring badge "🔁 monthly"

---

### Test Scenario 6.6: Complete Monthly Recurring Task

**Steps**:
1. Mark "Monthly review" complete
2. Wait 3 seconds

**Expected Result**:
- ✅ Original task marked complete
- ✅ New task created with due date **1 month later** (1st of month after next at 10:00 AM)
- ✅ New task has recurring badge "🔁 monthly"

---

### Test Scenario 6.7: Monthly Recurring Edge Case (Month-End)

**Steps**:
1. Create task:
   - Title: "End of month task"
   - Due Date: **January 31, 2026** at 3:00 PM
   - Recurring: **Monthly**
2. Mark complete

**Expected Result**:
- ✅ New task created with due date **February 28, 2026** at 3:00 PM (or Feb 29 if leap year)
- ✅ System handles month-end edge case correctly (since Feb doesn't have 31 days)

---

### Test Scenario 6.8: Recurring Task Without Due Date

**Steps**:
1. Create task:
   - Title: "Regular checkin"
   - Recurring: checked
   - Pattern: **Daily**
   - Due Date: Leave empty
2. Mark complete

**Expected Result**:
- ✅ Original task marked complete
- ✅ New task created immediately
- ✅ New task has NO due date (NULL)
- ✅ New task is pending

---

### Test Scenario 6.9: Edit Recurring Task

**Steps**:
1. Find one of the recurring tasks (original or regenerated)
2. Click Edit
3. Change recurrence pattern from "Daily" to "Weekly"
4. Click Save

**Expected Result**:
- ✅ ONLY this specific instance is updated
- ✅ Recurring badge changes to "🔁 weekly"
- ✅ When completed, new instance will use weekly pattern

---

### Test Scenario 6.10: Disable Recurrence on Task

**Steps**:
1. Edit a recurring task
2. Uncheck "Recurring task" checkbox
3. Click Save

**Expected Result**:
- ✅ Recurring badge disappears
- ✅ When task is completed, NO new instance is created

---

### Test Scenario 6.11: Delete Recurring Task Instance

**Steps**:
1. Find a recurring task
2. Click Delete button
3. Confirm deletion

**Expected Result**:
- ✅ ONLY this specific instance is deleted
- ✅ Other instances (if any) remain unaffected

---

### Test Scenario 6.12: Multiple Recurring Tasks Complete Simultaneously

**Steps**:
1. Create 3 daily recurring tasks
2. Mark all 3 complete quickly (within 5 seconds)

**Expected Result**:
- ✅ All 3 original tasks marked complete
- ✅ 3 new tasks created (one for each)
- ✅ No interference between task generations
- ✅ Each new task has correct due date (+1 day from respective original)

---

## User Story 7: Task Reminders with Browser Notifications (P3)

**Goal**: Verify reminder scheduling, browser notification delivery, and permission handling

### Test Scenario 7.1: Set Reminder on Task

**Steps**:
1. Create a new task:
   - Title: "Call dentist"
   - Reminder: Set to **5 minutes from now**
   - Click "Create Task"

**Expected Result**:
- ✅ Task appears in list
- ✅ Task shows **indigo reminder badge** with "🔔 Reminder" text
- ✅ Reminder time is stored

---

### Test Scenario 7.2: Browser Notification Permission Request

**Steps**:
1. If this is first time setting reminder:
   - Browser should prompt for notification permission
2. Click **Allow** when prompted

**Expected Result**:
- ✅ Browser shows native permission dialog
- ✅ Dialog mentions notifications for tasks
- ✅ After allowing, no error messages appear

---

### Test Scenario 7.3: Receive Notification for Pending Task

**Steps**:
1. Wait for 5 minutes (from Test 7.1)
2. Keep browser tab open (can be in background)

**Expected Result**:
- ✅ Browser notification appears within 5 seconds of scheduled time
- ✅ Notification title includes "Task Reminder" or similar
- ✅ Notification body includes task title: "Call dentist"
- ✅ Notification has app icon

---

### Test Scenario 7.4: Click Notification to Navigate

**Steps**:
1. When notification appears, click on it

**Expected Result**:
- ✅ Browser navigates to dashboard (http://localhost:3000/dashboard)
- ✅ Task "Call dentist" is highlighted/scrolled into view
- ✅ Task is in pending state (not completed)

---

### Test Scenario 7.5: No Notification for Completed Task

**Steps**:
1. Create task:
   - Title: "Test completed reminder"
   - Reminder: **3 minutes from now**
2. Immediately mark task as complete (checkbox)
3. Wait 3+ minutes

**Expected Result**:
- ✅ NO notification appears
- ✅ Reminder badge disappears when task is completed
- ✅ System correctly suppresses notification for completed tasks

---

### Test Scenario 7.6: Edit Reminder Time

**Steps**:
1. Create task with reminder in 10 minutes
2. Edit task
3. Change reminder to **2 minutes from now**
4. Save

**Expected Result**:
- ✅ Old reminder (10 min) is cancelled
- ✅ New reminder (2 min) is scheduled
- ✅ Notification appears after 2 minutes (not 10)

---

### Test Scenario 7.7: Remove Reminder

**Steps**:
1. Edit task with reminder
2. Click **Clear** button next to reminder field
3. Save

**Expected Result**:
- ✅ Reminder badge disappears
- ✅ No notification will be sent
- ✅ Old reminder is cancelled

---

### Test Scenario 7.8: Reminder in the Past (Validation)

**Steps**:
1. Using API or browser console, try to set reminder in past:
   ```bash
   curl -X POST http://localhost:8000/api/tasks \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test","reminder_time":"2023-01-01T10:00:00"}'
   ```

**Expected Result**:
- ✅ API returns **HTTP 400 Bad Request**
- ✅ Error message: "Reminder time must be in the future"
- ✅ Task is NOT created

---

### Test Scenario 7.9: Notification Permission Denied

**Steps**:
1. Block notifications in browser settings:
   - Chrome: Settings → Privacy → Site Settings → Notifications → Block localhost:3000
   - Firefox: Similar path
2. Create task with reminder
3. Wait for reminder time

**Expected Result**:
- ✅ Task is created with reminder badge
- ✅ UI shows warning: "Notifications are disabled. Enable in browser settings."
- ✅ No notification appears (since permission denied)
- ✅ App doesn't crash or error

---

### Test Scenario 7.10: Recurring Task with Reminder

**Steps**:
1. Create task:
   - Title: "Daily reminder task"
   - Due Date: Tomorrow 9:00 AM
   - Recurring: Daily
   - Reminder: Tomorrow 8:45 AM (15 min before due)
2. Complete task after receiving reminder

**Expected Result**:
- ✅ Notification appears at 8:45 AM tomorrow
- ✅ After completion, new instance is created
- ✅ New instance has reminder scheduled for **next day** 8:45 AM
- ✅ Reminder recurs along with task

---

## Edge Cases & Error Handling

### Test Scenario E.1: Very Long Search Query

**Steps**:
1. Enter search query with 600 characters
2. Observe behavior

**Expected Result**:
- ✅ Search query is truncated to 500 characters
- ✅ No performance degradation
- ✅ Search still works correctly

---

### Test Scenario E.2: Search with SQL Special Characters

**Steps**:
1. Create task: "50% discount OR 1=1; DROP TABLE tasks;"
2. Search for: **OR 1=1**

**Expected Result**:
- ✅ Task appears in results
- ✅ Special SQL characters treated as literals
- ✅ No SQL injection vulnerability
- ✅ Database remains intact

---

### Test Scenario E.3: Empty Search Query

**Steps**:
1. Clear search field completely
2. Submit search

**Expected Result**:
- ✅ All tasks displayed (same as no search)
- ✅ No error occurs

---

### Test Scenario E.4: Filter and Sort Together

**Steps**:
1. Set filter Status: Pending
2. Set filter Priority: High
3. Set sort: Due Date Ascending

**Expected Result**:
- ✅ Only pending high-priority tasks shown
- ✅ Results sorted by due date ascending
- ✅ Filters and sort work together correctly

---

### Test Scenario E.5: Concurrent Changes During Notification Wait

**Steps**:
1. Create task with reminder in 2 minutes
2. After 1 minute, edit task and mark complete
3. Wait 1 more minute

**Expected Result**:
- ✅ No notification appears (task was completed before reminder time)
- ✅ System correctly tracks task state changes

---

## Backward Compatibility Tests (Phase II Features)

**Goal**: Ensure all existing Phase II functionality still works

### Test Scenario BC.1: Create Simple Task (Phase II)

**Steps**:
1. Create task with only:
   - Title: "Simple task"
   - Description: "Just like Phase II"
   (Leave ALL new Phase III fields at defaults)

**Expected Result**:
- ✅ Task created successfully
- ✅ Priority defaults to Medium
- ✅ No due date
- ✅ Not recurring
- ✅ No reminder
- ✅ Behaves exactly like Phase II tasks

---

### Test Scenario BC.2: Update Task Title/Description Only

**Steps**:
1. Edit any task
2. Change only title or description
3. Don't touch priority, due date, recurring, or reminder
4. Save

**Expected Result**:
- ✅ Title/description updated
- ✅ All Phase III fields remain unchanged
- ✅ No unexpected changes to priority or other fields

---

### Test Scenario BC.3: Complete/Uncomplete Task

**Steps**:
1. Toggle checkbox on various tasks

**Expected Result**:
- ✅ Completion status updates correctly
- ✅ Strikethrough applied/removed
- ✅ No impact on other fields
- ✅ Same behavior as Phase II

---

### Test Scenario BC.4: Delete Task

**Steps**:
1. Delete a task

**Expected Result**:
- ✅ Confirmation dialog appears
- ✅ Task is deleted from database
- ✅ Task disappears from list
- ✅ Same behavior as Phase II

---

### Test Scenario BC.5: Sign Out

**Steps**:
1. Click "Sign Out" button

**Expected Result**:
- ✅ User logged out
- ✅ Redirected to signin page
- ✅ Auth token cleared

---

### Test Scenario BC.6: Authentication Required

**Steps**:
1. Log out
2. Navigate directly to http://localhost:3000/dashboard

**Expected Result**:
- ✅ Redirected to signin page
- ✅ Cannot access dashboard without auth
- ✅ Same security as Phase II

---

## Performance & Quality Tests

### Test Scenario P.1: Search Response Time

**Steps**:
1. Create 50+ tasks
2. Open browser DevTools → Network tab
3. Perform search
4. Measure time from last keystroke to results display

**Expected Result**:
- ✅ Results appear within **2 seconds**
- ✅ Meets SC-003 success criterion

---

### Test Scenario P.2: Filter Response Time

**Steps**:
1. With 50+ tasks loaded
2. Apply multiple filters simultaneously
3. Measure time to results

**Expected Result**:
- ✅ Results appear within **2 seconds**
- ✅ Meets SC-004 success criterion

---

### Test Scenario P.3: Sort Response Time

**Steps**:
1. Change sort order
2. Measure time to reorder

**Expected Result**:
- ✅ Reordering completes within **1 second**
- ✅ Meets SC-005 success criterion

---

### Test Scenario P.4: Recurring Task Generation Time

**Steps**:
1. Complete recurring task
2. Measure time until new task appears

**Expected Result**:
- ✅ New task appears within **3 seconds**
- ✅ Meets SC-006 success criterion

---

### Test Scenario P.5: Notification Delivery Time

**Steps**:
1. Set reminder for specific time
2. Measure time from scheduled time to notification appearance

**Expected Result**:
- ✅ Notification appears within **5 seconds** of scheduled time
- ✅ Meets SC-007 success criterion

---

## Accessibility Tests

### Test Scenario A.1: Keyboard Navigation

**Steps**:
1. Navigate entire interface using only Tab, Enter, Space, Arrow keys
2. Create task, edit task, change filters, search

**Expected Result**:
- ✅ All interactive elements are keyboard accessible
- ✅ Focus indicators visible
- ✅ Tab order is logical

---

### Test Scenario A.2: Screen Reader (Optional)

**Steps**:
1. Enable screen reader (NVDA, JAWS, or VoiceOver)
2. Navigate task list

**Expected Result**:
- ✅ Task titles announced
- ✅ Priority levels announced
- ✅ Completion status announced
- ✅ Form labels are read correctly

---

### Test Scenario A.3: Color Contrast

**Steps**:
1. Use browser DevTools or WAVE tool
2. Check contrast ratios for:
   - Priority badges (red, yellow, green)
   - Due date badges (red, yellow, blue)
   - Text on colored backgrounds

**Expected Result**:
- ✅ All text meets WCAG AA standards (4.5:1 ratio)
- ✅ Visual indicators distinguishable without color alone

---

## Security Tests

### Test Scenario S.1: User Isolation

**Steps**:
1. Create tasks with User A
2. Log out
3. Sign in with User B
4. View task list

**Expected Result**:
- ✅ User B sees ONLY their own tasks
- ✅ User A's tasks completely hidden
- ✅ No cross-user data leakage

---

### Test Scenario S.2: SQL Injection Protection

**Steps**:
1. Search for: **'; DROP TABLE tasks; --**
2. Filter with malformed query parameters

**Expected Result**:
- ✅ No database errors
- ✅ Special characters treated as literals
- ✅ ORM provides automatic escaping

---

### Test Scenario S.3: Authentication on All Endpoints

**Steps**:
1. Log out
2. Try to access API directly:
   ```bash
   curl http://localhost:8000/api/tasks
   ```

**Expected Result**:
- ✅ Returns **HTTP 401 Unauthorized**
- ✅ No task data returned

---

## Final Validation Checklist

After completing all tests above, verify:

- [ ] All 7 user stories validated independently
- [ ] All 20 success criteria met (SC-001 to SC-020)
- [ ] All 78 functional requirements covered (FR-001 to FR-078)
- [ ] All edge cases tested (priority validation, invalid dates, special characters, etc.)
- [ ] All Phase II features still work (backward compatibility)
- [ ] Performance benchmarks met (<2s for search/filter, <1s for sort, <3s for recurring, <5s for notifications)
- [ ] Accessibility verified (keyboard nav, color contrast)
- [ ] Security verified (user isolation, SQL injection protection, auth required)
- [ ] Database migration applied successfully (priority, due_date, is_recurring, recurrence_pattern, reminder_time columns exist)
- [ ] No console errors in browser DevTools
- [ ] No server errors in backend logs

---

## Known Limitations & Future Work

- **Browser Notifications**: Require user permission; won't work if denied
- **Notification Timing**: Relies on browser tab being open; no server-side push notifications
- **Recurring Task Timezone**: Uses browser local time; no timezone configuration
- **No Automated Tests**: All testing is manual per project specifications

---

## Troubleshooting

### Issue: Notifications not appearing

**Solution**:
1. Check browser console for permission errors
2. Verify notification permission in browser settings (should be "Allow")
3. Ensure browser tab is open (notifications won't trigger if tab is closed)
4. Check reminder time is in the future

### Issue: Search/filter not working

**Solution**:
1. Check browser DevTools Network tab for API errors
2. Verify backend is running (http://localhost:8000/docs should show API docs)
3. Clear browser cache and reload
4. Check for JavaScript console errors

### Issue: Recurring tasks not regenerating

**Solution**:
1. Verify RecurringService is integrated in task_service.py
2. Check backend logs for errors during task completion
3. Ensure task has is_recurring=true and valid recurrence_pattern
4. Try completing task again after refresh

### Issue: Overdue/Today indicators not showing

**Solution**:
1. Verify task has a due_date set
2. Check browser date/time is correct
3. Refresh page to re-render visual indicators
4. Inspect task in DevTools to verify due_date value

---

## Support & Feedback

For issues or questions:
- Check backend logs: `backend/app/main.py` console output
- Check browser console: F12 → Console tab
- Review API documentation: http://localhost:8000/docs
- Review spec: `specs/003-advanced-task-features/spec.md`
- Review implementation tasks: `specs/003-advanced-task-features/tasks.md`

---

**End of Quickstart Testing Guide**
