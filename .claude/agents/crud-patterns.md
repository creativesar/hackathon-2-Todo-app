# CRUD Patterns Documentation

**Purpose**: Comprehensive documentation of Create, Read, Update, Delete patterns for todo tasks
**For**: Reusable Intelligence Subagent
**Version**: 1.0.0

## Overview

This document captures all CRUD patterns used in the Todo App, enabling consistent implementation across all phases and features.

---

## CREATE Pattern

### Pattern Name: **Create Task with Validation**

**Purpose**: Add new tasks with proper validation and default values

**When to Use**:
- User adds a new task via CLI
- Bulk import of tasks (Phase II+)
- API endpoint receives create request (Phase II+)

**Implementation Steps**:
1. Validate title (non-empty, max 200 chars)
2. Validate description (optional, max 1000 chars)
3. Generate unique auto-incrementing ID
4. Set default values (completed=False, created_at=now)
5. Store task in data structure
6. Return created task object

**Code Example**:
```python
def create(self, title: str, description: str = "") -> Task:
    """Create a new task with validation."""
    # Step 1: Validate title
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    if len(title) > 200:
        raise ValueError("Title cannot exceed 200 characters")

    # Step 2: Validate description
    if len(description) > 1000:
        raise ValueError("Description cannot exceed 1000 characters")

    # Step 3: Generate ID
    task_id = self._next_id
    self._next_id += 1

    # Step 4: Create task with defaults
    task = Task(
        id=task_id,
        title=title.strip(),
        description=description.strip(),
        completed=False,
        created_at=datetime.now()
    )

    # Step 5: Store task
    self._tasks[task_id] = task

    # Step 6: Return created task
    return task
```

**Edge Cases**:
- Empty string → Raise ValueError
- Whitespace only → Raise ValueError
- Very long title → Raise ValueError
- None as title → Raise ValueError
- Description can be empty (valid)

**Testing Strategy**:
```python
# Happy path
test_create_task_with_title_and_description()
test_create_task_with_title_only()

# Validation
test_create_with_empty_title_raises_error()
test_create_with_whitespace_title_raises_error()
test_create_with_too_long_title_raises_error()

# Edge cases
test_create_with_special_characters()
test_create_with_unicode_characters()
test_create_multiple_tasks_have_unique_ids()
```

---

## READ Pattern

### Pattern Name: **Read All Tasks**

**Purpose**: Retrieve all tasks from storage

**When to Use**:
- User requests task list via `list` command
- Dashboard needs to display all tasks
- Filter/search operations need full dataset

**Implementation Steps**:
1. Access storage
2. Retrieve all task objects
3. Return as list (sorted by ID or creation date)

**Code Example**:
```python
def read_all(self) -> List[Task]:
    """Retrieve all tasks."""
    # Return tasks sorted by ID
    return [self._tasks[task_id] for task_id in sorted(self._tasks.keys())]
```

**Variants**:
- **Read by ID**: Get single task
- **Read by Status**: Filter pending or completed
- **Read by Category**: Filter by tags (Phase II+)

**Testing Strategy**:
```python
test_read_all_returns_empty_list_when_no_tasks()
test_read_all_returns_all_tasks()
test_read_all_preserves_task_order()
```

---

### Pattern Name: **Read by ID**

**Purpose**: Get a specific task by its unique identifier

**When to Use**:
- Before updating a task
- Before deleting a task
- Before marking as complete
- Display task details

**Implementation Steps**:
1. Validate ID is integer
2. Check if ID exists
3. Return task or None

**Code Example**:
```python
def read_by_id(self, task_id: int) -> Optional[Task]:
    """Retrieve task by ID."""
    return self._tasks.get(task_id)
```

**Edge Cases**:
- ID doesn't exist → Return None
- Negative ID → Return None
- ID of deleted task → Return None

**Testing Strategy**:
```python
test_read_by_id_returns_task_when_exists()
test_read_by_id_returns_none_when_not_exists()
test_read_by_id_with_invalid_id_returns_none()
```

---

## UPDATE Pattern

### Pattern Name: **Partial Update Task**

**Purpose**: Modify task fields while preserving non-updated fields

**When to Use**:
- User updates task title only
- User updates description only
- User updates both title and description

**Implementation Steps**:
1. Validate ID exists
2. Get existing task
3. Update only provided fields (None means "don't change")
4. Validate new values
5. Update task in storage
6. Return updated task

**Code Example**:
```python
def update(
    self,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[Task]:
    """Update task with partial updates supported."""
    # Step 1: Get existing task
    task = self.read_by_id(task_id)
    if not task:
        return None

    # Step 2: Update title if provided
    if title is not None:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        task.title = title.strip()

    # Step 3: Update description if provided
    if description is not None:
        if len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        task.description = description.strip()

    # Step 4: Return updated task
    return task
```

**Key Design Decision**: Use `None` to indicate "don't change this field"
- `title=""` → Set title to empty (invalid, will raise error)
- `title=None` → Don't change title
- `title="New"` → Change title to "New"

**Edge Cases**:
- ID doesn't exist → Return None
- Both fields None → No changes made (valid)
- Empty string for title → Raise ValueError
- Empty string for description → Set to empty (valid)

**Testing Strategy**:
```python
test_update_title_only()
test_update_description_only()
test_update_both_fields()
test_update_with_none_values_preserves_fields()
test_update_invalid_id_returns_none()
test_update_with_empty_title_raises_error()
```

---

## DELETE Pattern

### Pattern Name: **Delete Task by ID**

**Purpose**: Remove task from storage permanently

**When to Use**:
- User explicitly deletes a task
- Cleanup of old/completed tasks (Phase II+)
- Admin operations

**Implementation Steps**:
1. Validate ID exists
2. Remove task from storage
3. **DO NOT** reuse the ID
4. Return success/failure

**Code Example**:
```python
def delete(self, task_id: int) -> bool:
    """Delete task by ID."""
    if task_id in self._tasks:
        del self._tasks[task_id]
        return True
    return False
```

**Critical Rule**: **NEVER REUSE DELETED IDs**
- Deleted ID=5 means next task is ID=6, not ID=5
- This prevents confusion and maintains audit trail
- IDs may have gaps after deletions

**Edge Cases**:
- ID doesn't exist → Return False
- Delete same ID twice → Return False on second attempt
- Delete all tasks → Next task still gets next sequential ID

**Testing Strategy**:
```python
test_delete_removes_task()
test_delete_invalid_id_returns_false()
test_delete_twice_returns_false_second_time()
test_deleted_id_not_reused()
test_delete_doesnt_affect_other_tasks()
```

---

## COMPLETE Pattern

### Pattern Name: **Mark Task Complete**

**Purpose**: Change task status to completed

**When to Use**:
- User marks task as done
- Batch completion of tasks
- Auto-complete based on rules (Phase III+)

**Implementation Steps**:
1. Validate ID exists
2. Get task
3. Set completed=True
4. Return updated task

**Code Example**:
```python
def complete(self, task_id: int) -> Optional[Task]:
    """Mark task as completed."""
    task = self.read_by_id(task_id)
    if not task:
        return None

    task.completed = True
    return task
```

**Design Considerations**:
- Should we allow toggle (mark incomplete again)? → Phase II decision
- Should we track completion timestamp? → Add in Phase II
- Should completed tasks be hidden? → Filtering feature in Phase II

**Edge Cases**:
- ID doesn't exist → Return None
- Task already completed → Still set to True (idempotent)

**Testing Strategy**:
```python
test_complete_marks_task_as_done()
test_complete_invalid_id_returns_none()
test_complete_already_completed_task()
```

---

## Common Validation Patterns

### ID Validation
```python
def _validate_id(task_id: Any) -> bool:
    """Validate task ID."""
    if not isinstance(task_id, int):
        return False
    if task_id < 1:
        return False
    return True
```

### Title Validation
```python
def _validate_title(title: str) -> None:
    """Validate task title."""
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title exceeds 200 characters")
```

### Description Validation
```python
def _validate_description(description: str) -> None:
    """Validate task description."""
    if len(description) > 1000:
        raise ValueError("Description exceeds 1000 characters")
```

---

## Storage Patterns

### In-Memory Storage (Phase I)
```python
class TaskService:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
```

**Pros**: Fast, simple, no dependencies
**Cons**: Data lost on exit, no persistence

### File Storage (Phase II)
```python
class TaskService:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path
        self._load_from_file()

    def _save_to_file(self):
        with open(self.file_path, 'w') as f:
            json.dump(self._serialize(), f)

    def _load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self._deserialize(json.load(f))
```

### Database Storage (Phase II-III)
```python
class TaskService:
    def __init__(self, db_url: str):
        self.db = Database(db_url)

    def create(self, title: str, description: str) -> Task:
        task = Task(...)
        self.db.execute("INSERT INTO tasks ...")
        return task
```

---

## Error Handling Patterns

### User-Facing Errors
```python
try:
    service.create("", "Description")
except ValueError as e:
    print(f"Error: {e}")  # "Error: Title cannot be empty"
```

### System Errors
```python
try:
    service.save_to_file()
except IOError as e:
    logger.error(f"Failed to save: {e}")
    print("Failed to save tasks. Changes may be lost.")
```

---

## Performance Patterns

### Batch Operations (Phase II+)
```python
def create_batch(self, tasks: List[Tuple[str, str]]) -> List[Task]:
    """Create multiple tasks efficiently."""
    created_tasks = []
    for title, description in tasks:
        task = self.create(title, description)
        created_tasks.append(task)
    return created_tasks
```

### Lazy Loading (Phase III+)
```python
def read_all(self, limit: int = 100, offset: int = 0) -> List[Task]:
    """Retrieve tasks with pagination."""
    all_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
    return all_tasks[offset:offset + limit]
```

---

## Future Extensions

### Phase II Extensions
- Add priority field to Task model
- Add tags/categories
- Add search by title/description
- Add filter by status/priority/tags
- Add sort by various fields
- Add file persistence

### Phase III Extensions
- Add due_date field
- Add reminder functionality
- Add recurring tasks
- Add subtasks/dependencies
- Add collaboration features

### Phase IV-V Extensions
- Add cloud storage backend
- Add REST API
- Add authentication/authorization
- Add multi-tenancy
- Add audit logging

---

## References

- **Task Model**: `src/models/task.py`
- **Service Layer**: `src/services/task_service.py`
- **CLI Interface**: `src/cli/console.py`
- **Tests**: `tests/test_task_service.py`
- **Specification**: `specs/phase1-console/spec.md`
