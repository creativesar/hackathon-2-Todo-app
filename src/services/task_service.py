"""Task service - all CRUD operations."""

from src.models.task import Task


class TaskService:
    """Service for managing tasks in memory."""

    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def create(self, title, description=""):
        """Add new task."""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False
        )
        self.next_id += 1
        self.tasks.append(task)
        return task

    def read_all(self):
        """Get all tasks."""
        return self.tasks

    def read(self, task_id):
        """Get single task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task_id, title=None, description=None):
        """Update task title and/or description."""
        task = self.read(task_id)
        if task is None:
            return None
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        return task

    def complete(self, task_id):
        """Mark task as complete."""
        task = self.read(task_id)
        if task:
            task.completed = True
        return task

    def delete(self, task_id):
        """Delete task by ID."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False
