# Task Operations Subagent

**Version**: 1.0.0
**Purpose**: Reusable intelligence for CRUD operations on todo tasks
**Compatibility**: Phase I-V of Todo App Hackathon
**Bonus Points**: +200 (Reusable Intelligence)

## Overview

This subagent encapsulates all knowledge and patterns for performing CRUD (Create, Read, Update, Delete) operations on todo tasks. It can be invoked by Claude Code or other agents to handle task management operations consistently across all phases of the project.

## Capabilities

### 1. Create Task
- Add new tasks with title (required) and description (optional)
- Validate input (non-empty title, max 200 chars)
- Auto-generate unique IDs
- Set default values (completed=false, created_at=now)

### 2. Read Tasks
- List all tasks
- Filter by status (pending/completed)
- Search by title or description (Phase II+)
- Sort by various criteria (Phase II+)

### 3. Update Task
- Modify task title and/or description
- Partial updates supported (update only specified fields)
- Validate task existence before update
- Preserve non-updated fields

### 4. Delete Task
- Remove tasks by ID
- Validate task existence
- Never reuse deleted IDs
- Optional confirmation prompt (interactive mode)

### 5. Complete Task
- Mark tasks as done
- Toggle completion status
- Validate task existence

## Data Model

```python
@dataclass
class Task:
    id: int              # Unique, auto-incrementing, never reused
    title: str           # Required, 1-200 characters
    description: str     # Optional, max 1000 characters
    completed: bool      # Default: False
    created_at: datetime # Auto-set on creation
```

## Architecture Patterns

### Service Layer Pattern

**Location**: `src/services/task_service.py`

```python
class TaskService:
    """
    Central service for all task operations.
    Uses in-memory storage (Phase I) or database (Phase II+).
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create(title: str, description: str = "") -> Task
    def read_all() -> List[Task]
    def read_by_id(id: int) -> Optional[Task]
    def update(id: int, title: Optional[str], description: Optional[str]) -> Optional[Task]
    def delete(id: int) -> bool
    def complete(id: int) -> Optional[Task]
```

### CLI Interface Pattern

**Location**: `src/cli/console.py`

```python
class TodoConsole(cmd.Cmd):
    """
    Interactive REPL console using Python's cmd module.
    Provides both command-line and interactive modes.
    """

    prompt = "todo> "

    # Command handlers
    def do_add(args: str) -> None
    def do_list(args: str) -> None
    def do_update(args: str) -> None
    def do_delete(args: str) -> None
    def do_complete(args: str) -> None
    def do_help(args: str) -> None
    def do_exit(args: str) -> bool
```

## Usage Patterns

### Pattern 1: Add Task (Command Mode)
```python
# Direct command with arguments
todo> add "Buy groceries" "Milk, eggs, bread"
# Result: Task created with ID=1
```

### Pattern 2: Add Task (Interactive Mode)
```python
# No arguments triggers interactive prompts
todo> add
# Prompt: Enter task title:
> Buy groceries
# Prompt: Enter task description (optional):
> Milk, eggs, bread
# Result: Task created with ID=1
```

### Pattern 3: List All Tasks
```python
todo> list
# Output:
# ○ Task #1
#   Title: Buy groceries
#   Description: Milk, eggs, bread
#
# ✓ Task #2
#   Title: Call dentist
#   Description: Schedule appointment
```

### Pattern 4: Update Task (Interactive)
```python
todo> update
# Shows all tasks with IDs
# Prompt: Enter task ID to update:
> 1
# Prompt: Enter new title (or press Enter to keep):
> Buy groceries and fruits
# Prompt: Enter new description (or press Enter to keep):
> Milk, eggs, bread, apples, bananas
```

### Pattern 5: Complete Task
```python
todo> complete
# Shows pending tasks only
# Prompt: Enter task ID to mark as complete:
> 1
# Result: Task #1 marked as done
```

### Pattern 6: Delete Task
```python
todo> delete
# Shows all tasks
# Prompt: Enter task ID to delete:
> 1
# Prompt: Are you sure? Type 'yes' to confirm:
> yes
# Result: Task #1 deleted successfully
```

## Validation Rules

### Title Validation
- **Required**: Cannot be empty
- **Max Length**: 200 characters
- **Allowed**: Any UTF-8 characters

### Description Validation
- **Optional**: Can be empty
- **Max Length**: 1000 characters
- **Allowed**: Any UTF-8 characters

### ID Validation
- **Type**: Integer only
- **Range**: Positive numbers (1+)
- **Existence**: Must exist in task list for update/delete/complete

## Error Handling

### User Errors
- Empty title → Show error: "Title cannot be empty"
- Invalid ID → Show error: "Task #X not found"
- Non-numeric ID → Show usage example

### System Errors
- Storage failure → Log error, show user-friendly message
- Validation failure → Show specific validation error

## Testing Patterns

### Unit Tests (Service Layer)
```python
def test_create_task():
    service = TaskService()
    task = service.create("Test Task", "Test Desc")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.completed is False

def test_create_with_empty_title():
    service = TaskService()
    with pytest.raises(ValueError):
        service.create("", "Description")
```

### Integration Tests (CLI Layer)
```python
def test_add_command():
    console = TodoConsole()
    console.do_add('"Test Task" "Test Description"')
    tasks = console.service.read_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
```

## Extension Points (Future Phases)

### Phase II Extensions
- Add priority field (High/Medium/Low)
- Add tags/categories
- Add search and filter methods
- Add sorting capabilities
- Add user authentication

### Phase III Extensions
- Add due dates and reminders
- Add recurring tasks
- Add AI chatbot integration
- Add voice command support

### Phase IV-V Extensions
- Add cloud storage backend
- Add REST API endpoints
- Add Kubernetes deployment
- Add multi-user support

## Invocation Examples

### Example 1: Add Multiple Tasks
```
User: "Add three tasks: buy milk, call dentist, finish report"

Agent Action:
1. Parse user intent
2. Call service.create() three times:
   - service.create("Buy milk", "")
   - service.create("Call dentist", "")
   - service.create("Finish report", "")
3. Confirm all tasks created
```

### Example 2: Complete All Pending Tasks
```
User: "Mark all pending tasks as complete"

Agent Action:
1. Call service.read_all()
2. Filter for pending tasks (completed=False)
3. For each pending task:
   - Call service.complete(task.id)
4. Confirm completion count
```

### Example 3: Delete Completed Tasks
```
User: "Delete all completed tasks"

Agent Action:
1. Call service.read_all()
2. Filter for completed tasks (completed=True)
3. For each completed task:
   - Call service.delete(task.id)
4. Confirm deletion count
```

## Best Practices

### DO:
✅ Always validate inputs before operations
✅ Provide clear, user-friendly error messages
✅ Use service layer for all data operations
✅ Test both valid and invalid inputs
✅ Handle edge cases (empty lists, invalid IDs)
✅ Support both interactive and command modes

### DON'T:
❌ Reuse deleted task IDs
❌ Skip validation to "save time"
❌ Access storage directly (bypass service layer)
❌ Ignore error handling
❌ Assume inputs are always valid
❌ Mix business logic with presentation

## References

- **Specification**: `specs/phase1-console/spec.md`
- **Implementation Plan**: `specs/phase1-console/plan.md`
- **Task Breakdown**: `specs/phase1-console/tasks.md`
- **Service Implementation**: `src/services/task_service.py`
- **CLI Implementation**: `src/cli/console.py`
- **Tests**: `tests/test_task_service.py`, `tests/test_cli.py`

## Version History

- **1.0.0** (2025-12-28): Initial subagent creation for Phase I
  - Core CRUD operations
  - Interactive and command modes
  - Comprehensive validation
  - Error handling patterns
