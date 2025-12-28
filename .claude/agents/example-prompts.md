# Example Prompts for Task Operations Subagent

**Purpose**: Sample prompts demonstrating how to invoke the task-operations subagent
**For**: Reusable Intelligence
**Version**: 1.0.0

---

## Basic CRUD Operations

### Example 1: Add Single Task
**Prompt**:
```
Add a task to buy groceries with description "Milk, eggs, bread, fruits"
```

**Expected Agent Action**:
1. Invoke task-operations subagent
2. Call `service.create("Buy groceries", "Milk, eggs, bread, fruits")`
3. Confirm task created with ID

**Expected Output**:
```
✓ Task Created
Task ID: #1
Title: Buy groceries
Description: Milk, eggs, bread, fruits
```

---

### Example 2: Add Multiple Tasks
**Prompt**:
```
Add three tasks:
1. Call dentist to schedule appointment
2. Finish project report by Friday
3. Pay electricity bill
```

**Expected Agent Action**:
1. Parse list of tasks
2. For each task:
   - Extract title and description
   - Call `service.create(title, description)`
3. Confirm all tasks created

**Expected Output**:
```
✓ 3 Tasks Created Successfully

Task #1: Call dentist
Task #2: Finish project report
Task #3: Pay electricity bill
```

---

### Example 3: List All Tasks
**Prompt**:
```
Show me all my tasks
```

**Expected Agent Action**:
1. Call `service.read_all()`
2. Format and display all tasks with status

**Expected Output**:
```
📋 TODO LIST

○ Task #1
  Title: Buy groceries
  Description: Milk, eggs, bread, fruits

✓ Task #2
  Title: Call dentist
  Description: Schedule appointment

○ Task #3
  Title: Finish project report
  Description: Due Friday

✓ Total: 3 tasks | Pending: 2 | Done: 1
```

---

### Example 4: Update Task
**Prompt**:
```
Update task 1 to change the title to "Buy groceries and household items"
```

**Expected Agent Action**:
1. Call `service.update(1, title="Buy groceries and household items", description=None)`
2. Confirm update

**Expected Output**:
```
✓ Task Updated Successfully
Task #1: Buy groceries and household items
```

---

### Example 5: Complete Task
**Prompt**:
```
Mark task 3 as complete
```

**Expected Agent Action**:
1. Call `service.complete(3)`
2. Confirm completion

**Expected Output**:
```
✓ Task Completed
Task #3: Finish project report
Status: Done
```

---

### Example 6: Delete Task
**Prompt**:
```
Delete task 2
```

**Expected Agent Action**:
1. Call `service.delete(2)`
2. Confirm deletion

**Expected Output**:
```
✓ Task Deleted
Task #2 has been removed
```

---

## Complex Operations

### Example 7: Bulk Complete
**Prompt**:
```
Mark all pending tasks as complete
```

**Expected Agent Action**:
1. Call `service.read_all()`
2. Filter tasks where `completed == False`
3. For each pending task:
   - Call `service.complete(task.id)`
4. Report count of completed tasks

**Expected Output**:
```
✓ 2 Tasks Marked Complete
- Task #1: Buy groceries
- Task #3: Pay electricity bill
```

---

### Example 8: Conditional Delete
**Prompt**:
```
Delete all completed tasks
```

**Expected Agent Action**:
1. Call `service.read_all()`
2. Filter tasks where `completed == True`
3. For each completed task:
   - Call `service.delete(task.id)`
4. Report count of deleted tasks

**Expected Output**:
```
✓ 2 Tasks Deleted
- Task #2: Call dentist
- Task #4: Finish project report
```

---

### Example 9: Summary Report
**Prompt**:
```
Give me a summary of my tasks
```

**Expected Agent Action**:
1. Call `service.read_all()`
2. Calculate statistics:
   - Total tasks
   - Pending count
   - Completed count
   - Completion percentage
3. Display summary

**Expected Output**:
```
📊 Task Summary

Total Tasks: 5
Pending: 2 (40%)
Completed: 3 (60%)

Pending Tasks:
- Task #1: Buy groceries
- Task #5: Pay electricity bill

Recently Completed:
- Task #2: Call dentist
- Task #3: Finish project report
- Task #4: Clean garage
```

---

### Example 10: Find and Update
**Prompt**:
```
Find the task about groceries and add "and cleaning supplies" to its description
```

**Expected Agent Action**:
1. Call `service.read_all()`
2. Search for tasks containing "groceries" in title
3. Get current description
4. Append new text to description
5. Call `service.update(task.id, title=None, description=updated_desc)`

**Expected Output**:
```
✓ Task Found and Updated

Task #1: Buy groceries
New Description: Milk, eggs, bread, fruits and cleaning supplies
```

---

## Error Handling Examples

### Example 11: Invalid Task ID
**Prompt**:
```
Complete task 999
```

**Expected Agent Action**:
1. Call `service.complete(999)`
2. Receive `None` (task not found)
3. Display error message

**Expected Output**:
```
✗ Error
Task #999 not found
```

---

### Example 12: Empty Title
**Prompt**:
```
Add a task with empty title
```

**Expected Agent Action**:
1. Attempt to call `service.create("", "")`
2. Catch `ValueError`
3. Display validation error

**Expected Output**:
```
✗ Error
Title cannot be empty
```

---

### Example 13: Validation Error
**Prompt**:
```
Add a task with a very long title (300 characters)
```

**Expected Agent Action**:
1. Attempt to call `service.create(long_title, "")`
2. Catch `ValueError` about length
3. Display validation error

**Expected Output**:
```
✗ Error
Title cannot exceed 200 characters
Current length: 300 characters
```

---

## Interactive Mode Examples

### Example 14: Guided Task Creation
**Prompt**:
```
I want to add a new task
```

**Expected Agent Action**:
1. Detect intent to add task without details
2. Enter interactive mode
3. Prompt for title
4. Prompt for description
5. Create task

**Expected Interaction**:
```
➕ Add New Task

Enter task title:
> Buy groceries

Enter task description (optional):
> Milk, eggs, bread

✓ Task Created Successfully
Task ID: #1
Title: Buy groceries
Description: Milk, eggs, bread
```

---

### Example 15: Guided Update
**Prompt**:
```
I want to update a task
```

**Expected Agent Action**:
1. Show all tasks with IDs
2. Prompt for task ID
3. Show current details
4. Prompt for new title (optional)
5. Prompt for new description (optional)
6. Update task

**Expected Interaction**:
```
🔄 Update Task - Select Task

○ [1] Buy groceries
✓ [2] Call dentist
○ [3] Pay bill

Enter task ID to update:
> 1

Current Title: Buy groceries
Enter new title (or press Enter to keep):
> Buy groceries and fruits

Current Description: Milk, eggs, bread
Enter new description (or press Enter to keep):
> Milk, eggs, bread, apples, bananas

✓ Task Updated Successfully
Task #1: Buy groceries and fruits
Description: Milk, eggs, bread, apples, bananas
```

---

## Natural Language Examples

### Example 16: Conversational Add
**Prompt**:
```
I need to remember to call my dentist tomorrow morning
```

**Expected Agent Action**:
1. Parse natural language
2. Extract task: "Call dentist"
3. Extract description: "Tomorrow morning"
4. Call `service.create("Call dentist", "Tomorrow morning")`

**Expected Output**:
```
✓ Task Added
Task #4: Call dentist
When: Tomorrow morning
```

---

### Example 17: Status Query
**Prompt**:
```
What tasks do I have left to do?
```

**Expected Agent Action**:
1. Call `service.read_all()`
2. Filter for `completed == False`
3. Display pending tasks only

**Expected Output**:
```
📋 Pending Tasks (2)

○ Task #1: Buy groceries
  Description: Milk, eggs, bread, fruits

○ Task #3: Pay electricity bill
  Description: Due by end of month
```

---

### Example 18: Achievement Query
**Prompt**:
```
What have I completed today?
```

**Expected Agent Action**:
1. Call `service.read_all()`
2. Filter for `completed == True` and `created_at == today`
3. Display completed tasks

**Expected Output**:
```
✓ Completed Today (2 tasks)

✓ Task #2: Call dentist
✓ Task #4: Finish project report

Great progress! 🎉
```

---

## Advanced Scenarios (Phase II+)

### Example 19: Priority-Based Query
**Prompt**:
```
Show me all high priority tasks
```

**Expected Agent Action** (Phase II):
1. Call `service.read_all()`
2. Filter for `priority == "High"`
3. Display high priority tasks

**Note**: Requires priority field in Phase II

---

### Example 20: Search by Keyword
**Prompt**:
```
Find all tasks related to "groceries"
```

**Expected Agent Action** (Phase II):
1. Call `service.search("groceries")`
2. Search in both title and description
3. Display matching tasks

**Note**: Requires search functionality in Phase II

---

## Subagent Invocation Pattern

### General Pattern
```
When user asks to [operation] tasks:
1. Load task-operations subagent knowledge
2. Identify operation type (CREATE/READ/UPDATE/DELETE/COMPLETE)
3. Extract parameters from user prompt
4. Validate parameters using validation patterns
5. Call appropriate service method
6. Handle errors gracefully
7. Format and display result
8. Log operation for audit (Phase III+)
```

### Error Recovery Pattern
```
When operation fails:
1. Catch specific exception type
2. Map to user-friendly error message
3. Suggest corrective action
4. Preserve user's partial input
5. Offer to retry or cancel
```

### Confirmation Pattern
```
For destructive operations (delete, bulk complete):
1. Show what will be affected
2. Ask for explicit confirmation
3. Wait for "yes" or "no"
4. Proceed only on "yes"
5. Show summary of changes made
```

---

## Testing Prompts

### Test 1: Stress Test
```
Add 100 tasks with titles "Task 1" through "Task 100"
```

**Purpose**: Test performance and ID generation

---

### Test 2: Edge Case
```
Add a task with title containing special characters: "Buy @#$%^&* supplies"
```

**Purpose**: Test character handling

---

### Test 3: Unicode Test
```
Add a task with title in Chinese: "买菜"
```

**Purpose**: Test internationalization

---

### Test 4: Boundary Test
```
Add a task with exactly 200 character title and 1000 character description
```

**Purpose**: Test validation boundaries

---

## Best Practices for Prompt Engineering

### DO:
✅ Be specific about task details
✅ Use natural language
✅ Provide context when needed
✅ Ask for confirmation on destructive operations
✅ Request summaries for better UX

### DON'T:
❌ Assume IDs without checking
❌ Skip validation
❌ Use ambiguous references ("that task")
❌ Batch too many operations without feedback
❌ Ignore error messages

---

## References

- **Subagent Definition**: `.claude/agents/task-operations.md`
- **CRUD Patterns**: `.claude/agents/crud-patterns.md`
- **Service Layer**: `src/services/task_service.py`
- **CLI Interface**: `src/cli/console.py`
