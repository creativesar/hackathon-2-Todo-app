"""Tests for TaskService."""

import pytest

from src.models.task import Task
from src.services.task_service import TaskNotFoundError, TaskService


@pytest.fixture
def service() -> TaskService:
    """Create a fresh TaskService for each test."""
    return TaskService()


class TestAddTask:
    """Tests for add_task method."""

    def test_creates_task_with_correct_fields(self, service: TaskService) -> None:
        """Task should be created with correct fields."""
        task = service.add_task("Buy groceries", "Milk and eggs")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk and eggs"
        assert task.completed is False
        assert task.created_at is not None

    def test_rejects_empty_title(self, service: TaskService) -> None:
        """Empty title should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.add_task("")

    def test_rejects_whitespace_only_title(self, service: TaskService) -> None:
        """Whitespace-only title should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.add_task("   ")

    def test_rejects_title_too_long(self, service: TaskService) -> None:
        """Title over 200 chars should raise ValueError."""
        long_title = "x" * 201
        with pytest.raises(ValueError, match="cannot exceed 200"):
            service.add_task(long_title)

    def test_allows_empty_description(self, service: TaskService) -> None:
        """Description should default to empty string."""
        task = service.add_task("Test task")
        assert task.description == ""

    def test_rejects_description_too_long(self, service: TaskService) -> None:
        """Description over 1000 chars should raise ValueError."""
        long_desc = "y" * 1001
        with pytest.raises(ValueError, match="cannot exceed 1000"):
            service.add_task("Test", long_desc)

    def test_assigns_unique_ids(self, service: TaskService) -> None:
        """Each task should get a unique auto-incrementing ID."""
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_id_never_reused_after_deletion(self, service: TaskService) -> None:
        """After deleting a task, the next task should get next ID (no reuse)."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)
        new_task = service.add_task("Task 3")

        assert new_task.id == 3  # Not 1


class TestListTasks:
    """Tests for list_tasks method."""

    def test_returns_empty_list_when_no_tasks(self, service: TaskService) -> None:
        """list_tasks should return empty list when no tasks exist."""
        assert service.list_tasks() == []

    def test_returns_all_tasks(self, service: TaskService) -> None:
        """list_tasks should return all tasks in creation order."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        tasks = service.list_tasks()
        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"


class TestCompleteTask:
    """Tests for complete_task method."""

    def test_changes_status_to_true(self, service: TaskService) -> None:
        """complete_task should mark task as completed."""
        service.add_task("Task 1")
        task = service.complete_task(1)

        assert task.completed is True

    def test_raises_error_for_invalid_id(self, service: TaskService) -> None:
        """Invalid task ID should raise TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            service.complete_task(999)

    def test_can_complete_already_completed_task(self, service: TaskService) -> None:
        """Completing an already complete task should not error."""
        service.add_task("Task 1")
        service.complete_task(1)
        task = service.complete_task(1)  # Should not raise

        assert task.completed is True


class TestUpdateTask:
    """Tests for update_task method."""

    def test_changes_title(self, service: TaskService) -> None:
        """update_task should change the title."""
        service.add_task("Old title")
        task = service.update_task(1, title="New title")

        assert task.title == "New title"

    def test_changes_description(self, service: TaskService) -> None:
        """update_task should change the description."""
        service.add_task("Task", "Old desc")
        task = service.update_task(1, description="New description")

        assert task.description == "New description"

    def test_updates_both_title_and_description(self, service: TaskService) -> None:
        """update_task should update both title and description."""
        service.add_task("Task", "Desc")
        task = service.update_task(1, title="New", description="New desc")

        assert task.title == "New"
        assert task.description == "New desc"

    def test_partial_update_preserves_other_fields(self, service: TaskService) -> None:
        """Updating only title should preserve description."""
        service.add_task("Title", "Description")
        task = service.update_task(1, title="New Title")

        assert task.title == "New Title"
        assert task.description == "Description"

    def test_raises_error_for_invalid_id(self, service: TaskService) -> None:
        """Invalid task ID should raise TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            service.update_task(999, title="New")

    def test_rejects_empty_title(self, service: TaskService) -> None:
        """Empty title in update should raise ValueError."""
        service.add_task("Task")
        with pytest.raises(ValueError, match="cannot be empty"):
            service.update_task(1, title="")


class TestDeleteTask:
    """Tests for delete_task method."""

    def test_removes_task_from_list(self, service: TaskService) -> None:
        """delete_task should remove task from the list."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)

        tasks = service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2

    def test_raises_error_for_invalid_id(self, service: TaskService) -> None:
        """Invalid task ID should raise TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)

    def test_deleting_one_does_not_affect_others(self, service: TaskService) -> None:
        """Deleting one task should not affect other tasks."""
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")
        service.delete_task(2)

        tasks = service.list_tasks()
        assert [t.id for t in tasks] == [1, 3]
