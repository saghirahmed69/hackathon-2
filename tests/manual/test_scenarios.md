# Manual Test Scenarios: Console Todo Application

**Feature**: 001-console-todo-app
**Purpose**: Manual verification of all user stories and acceptance criteria
**Execution**: Run `python src/main.py` and follow scenarios below

---

## User Story 1: View and Add Tasks (Priority: P1)

### Scenario 1.1: View Empty Task List
**Given**: Application is started with no tasks
**When**: User selects menu option 2 (View All Tasks)
**Then**: System displays "No tasks found. Add a task to get started!"

### Scenario 1.2: Add Task with Title and Description
**Given**: Application is running
**When**: User selects option 1, enters title "Buy groceries", description "milk, eggs, bread"
**Then**: System displays "✓ Task added successfully! (ID: 1)"

### Scenario 1.3: Add Task with Only Title
**Given**: Application is running with 1 existing task
**When**: User selects option 1, enters title "Call dentist", presses Enter to skip description
**Then**: System displays "✓ Task added successfully! (ID: 2)"

### Scenario 1.4: View Multiple Tasks
**Given**: Application has 2 tasks (IDs 1 and 2)
**When**: User selects option 2 (View All Tasks)
**Then**: System displays:
```
=== All Tasks ===

[ ] #1: Buy groceries
    Description: milk, eggs, bread

[ ] #2: Call dentist
    Description: (none)

Total: 2 tasks (0 completed, 2 incomplete)
```

---

## User Story 2: Mark Tasks Complete (Priority: P2)

### Scenario 2.1: Mark Incomplete Task as Complete
**Given**: Task with ID 1 exists and is incomplete
**When**: User selects option 5, enters task ID 1
**Then**: System displays "✓ Task marked as complete!"

### Scenario 2.2: View Task After Marking Complete
**Given**: Task 1 has been marked complete
**When**: User selects option 2 (View All Tasks)
**Then**: Task 1 shows [✓] status symbol

### Scenario 2.3: Mark Complete Task as Incomplete
**Given**: Task with ID 1 is complete
**When**: User selects option 5, enters task ID 1
**Then**: System displays "✓ Task marked as incomplete!"

### Scenario 2.4: Toggle Completion for Non-Existent Task
**Given**: Application is running
**When**: User selects option 5, enters task ID 999
**Then**: System displays "✗ Error: Task with ID 999 not found."

---

## User Story 3: Update Task Details (Priority: P3)

### Scenario 3.1: Update Task Title
**Given**: Task with ID 1 has title "Buy groceries"
**When**: User selects option 3, enters ID 1, new title "Buy groceries and supplies", presses Enter for description
**Then**: System displays "✓ Task updated successfully!"

### Scenario 3.2: Update Task Description
**Given**: Task with ID 1 has description "milk, eggs, bread"
**When**: User selects option 3, enters ID 1, presses Enter for title, new description "milk, eggs, bread, coffee"
**Then**: System displays "✓ Task updated successfully!"

### Scenario 3.3: Update with Empty Title (Error Case)
**Given**: Application is running
**When**: User selects option 3, enters ID 1, enters empty string for title
**Then**: System displays "✗ Error: Title cannot be empty. Task not updated."

### Scenario 3.4: Update Non-Existent Task
**Given**: Application is running
**When**: User selects option 3, enters task ID 999
**Then**: System displays "✗ Error: Task with ID 999 not found."

---

## User Story 4: Delete Unwanted Tasks (Priority: P3)

### Scenario 4.1: Delete Existing Task
**Given**: Task with ID 2 exists
**When**: User selects option 4, enters task ID 2
**Then**: System displays "✓ Task deleted successfully!"

### Scenario 4.2: Verify ID Stability After Deletion
**Given**: Tasks 1, 2, 3 exist; task 2 was deleted
**When**: User views all tasks (option 2)
**Then**: Only tasks 1 and 3 are displayed (ID 2 is gone)

### Scenario 4.3: Add New Task After Deletion
**Given**: Tasks 1 and 3 exist (ID 2 was deleted)
**When**: User adds a new task
**Then**: New task receives ID 4 (not 2 - IDs are never reused)

### Scenario 4.4: Delete Non-Existent Task
**Given**: Application is running
**When**: User selects option 4, enters task ID 999
**Then**: System displays "✗ Error: Task with ID 999 not found."

---

## Edge Cases

### Edge Case 1: Invalid Menu Choice
**Given**: Application displays main menu
**When**: User enters "abc" or "7" or "0"
**Then**: System displays "Invalid choice. Please enter a number between 1 and 6." and redisplays menu

### Edge Case 2: Empty Title on Add
**Given**: User selects option 1 (Add Task)
**When**: User presses Enter without typing a title
**Then**: System displays "✗ Error: Title cannot be empty."

### Edge Case 3: Keyboard Interrupt (Ctrl+C)
**Given**: Application is running
**When**: User presses Ctrl+C
**Then**: System displays "Application interrupted. Goodbye!" and exits gracefully

### Edge Case 4: EOF Signal (Ctrl+D)
**Given**: Application is running at any prompt
**When**: User presses Ctrl+D
**Then**: System displays "Application terminated. Goodbye!" and exits gracefully

### Edge Case 5: Very Long Title
**Given**: User is adding a task
**When**: User enters a title longer than 1000 characters
**Then**: System accepts and truncates to 1000 characters silently

### Edge Case 6: Very Long Description
**Given**: User is adding a task
**When**: User enters a description longer than 5000 characters
**Then**: System accepts and truncates to 5000 characters silently

### Edge Case 7: Exit Application
**Given**: Application is running
**When**: User selects option 6 (Exit)
**Then**: System displays "Goodbye! Your tasks will be lost when you exit." and terminates

---

## Complete Integration Test

**Purpose**: Verify all operations work together correctly

**Steps**:
1. Start application → Empty list message
2. Add task "Buy groceries" with description "milk, eggs" → Confirm ID 1
3. Add task "Call dentist" without description → Confirm ID 2
4. Add task "Finish report" with description "Q4 sales" → Confirm ID 3
5. View all tasks → Verify all 3 displayed with correct details
6. Mark task 1 complete → Confirm success
7. View tasks → Verify task 1 shows [✓]
8. Update task 2 title to "Schedule dentist appointment" → Confirm success
9. Update task 2 description to "Annual checkup" → Confirm success
10. View tasks → Verify task 2 updated
11. Delete task 3 → Confirm success
12. View tasks → Verify only tasks 1 and 2 remain
13. Add new task "Review code" → Confirm ID 4 (not 3!)
14. Mark task 1 incomplete → Confirm success
15. View tasks → Verify task 1 shows [ ]
16. Try invalid menu choice "abc" → Verify error and recovery
17. Try updating non-existent task 999 → Verify error message
18. Exit application → Verify goodbye message

**Expected Result**: All operations work correctly, data persists during session, IDs remain stable

---

## Acceptance Checklist

After completing all test scenarios, verify:

- [ ] All user story acceptance scenarios pass
- [ ] All edge cases handled gracefully
- [ ] No application crashes occur
- [ ] Error messages are clear and user-friendly
- [ ] Task IDs remain stable after deletions
- [ ] Application runs in continuous loop until exit
- [ ] Data is lost after exit (in-memory only behavior)
- [ ] Console output matches interface contract specifications

---

## Notes

- All tests are manual (no automated framework in Phase I)
- Execute tests after each phase completion for incremental validation
- Document any discrepancies between expected and actual behavior
- Verify against console interface contract in `contracts/console-interface.md`
