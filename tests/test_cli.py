"""Tests for CLI console interface."""

import pytest
from io import StringIO
from unittest.mock import patch
from src.cli.console import TodoConsole


class TestCLIHelp:
    """T030: Test CLI help command output."""

    def test_help_shows_all_commands(self):
        """Help command should display all available commands."""
        console = TodoConsole()

        # Capture output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.do_help("")
            output = mock_stdout.getvalue()

        # Verify all commands are shown
        assert "Add Task" in output or "add" in output.lower()
        assert "Update Task" in output or "update" in output.lower()
        assert "Complete Task" in output or "complete" in output.lower()
        assert "Delete Task" in output or "delete" in output.lower()
        assert "List" in output or "list" in output.lower()
        assert "Exit" in output or "exit" in output.lower()


class TestCLIAdd:
    """T031: Test CLI add command integration."""

    def test_add_command_creates_task(self):
        """Add command should create a new task."""
        console = TodoConsole()

        # Execute add command
        console.do_add('"Test Task" "Test Description"')

        # Verify task was created
        tasks = console.service.read_all()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"

    def test_add_command_with_empty_title_shows_error(self):
        """Add command with empty title should show error."""
        console = TodoConsole()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.do_add('""')
            output = mock_stdout.getvalue()

        # Verify error is shown
        assert "error" in output.lower() or "empty" in output.lower()

        # Verify no task was created
        tasks = console.service.read_all()
        assert len(tasks) == 0

    def test_add_command_title_only(self):
        """Add command with only title should work."""
        console = TodoConsole()

        console.do_add('"Just Title"')

        tasks = console.service.read_all()
        assert len(tasks) == 1
        assert tasks[0].title == "Just Title"
        assert tasks[0].description == ""


class TestCLIList:
    """T032: Test CLI list command integration."""

    def test_list_empty_shows_message(self):
        """List command with no tasks should show appropriate message."""
        console = TodoConsole()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.do_list("")
            output = mock_stdout.getvalue()

        # Verify message is shown
        assert "no task" in output.lower() or "0 task" in output.lower()

    def test_list_shows_all_tasks(self):
        """List command should display all created tasks."""
        console = TodoConsole()

        # Create multiple tasks
        console.service.create("Task 1", "Description 1")
        console.service.create("Task 2", "Description 2")
        console.service.create("Task 3", "Description 3")

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.do_list("")
            output = mock_stdout.getvalue()

        # Verify all tasks are shown
        assert "Task 1" in output
        assert "Task 2" in output
        assert "Task 3" in output

    def test_list_shows_status_indicators(self):
        """List command should show different indicators for pending/completed."""
        console = TodoConsole()

        # Create tasks with different statuses
        task1 = console.service.create("Pending Task", "")
        task2 = console.service.create("Completed Task", "")
        console.service.complete(task2.id)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.do_list("")
            output = mock_stdout.getvalue()

        # Verify status indicators are present
        # Looking for any kind of status markers (checkmarks, brackets, etc.)
        assert "Pending Task" in output
        assert "Completed Task" in output
        # Should have different markers for completed vs pending
        assert ("✓" in output or "[X]" in output or "[x]" in output)


class TestCLIComplete:
    """T033: Test CLI complete command integration."""

    def test_complete_command_marks_task_done(self):
        """Complete command should change task status."""
        console = TodoConsole()

        # Create a task
        task = console.service.create("Task to Complete", "")
        assert task.completed is False

        # Complete it via CLI
        console.do_complete(str(task.id))

        # Verify status changed
        tasks = console.service.read_all()
        assert tasks[0].completed is True

    def test_complete_invalid_id_shows_error(self):
        """Complete command with invalid ID should show error."""
        console = TodoConsole()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.do_complete("999")
            output = mock_stdout.getvalue()

        # Verify error message
        assert "error" in output.lower() or "not found" in output.lower()

    def test_complete_non_numeric_id_shows_error(self):
        """Complete command with non-numeric ID should show error."""
        console = TodoConsole()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.do_complete("abc")
            output = mock_stdout.getvalue()

        # Verify usage/error message
        assert "usage" in output.lower() or "example" in output.lower() or "error" in output.lower()


class TestCLIUpdate:
    """Additional test for update command."""

    def test_update_command_changes_task(self):
        """Update command should modify task details."""
        console = TodoConsole()

        # Create a task
        task = console.service.create("Original Title", "Original Desc")

        # Update via CLI
        console.do_update(f'{task.id} "New Title" "New Desc"')

        # Verify changes
        tasks = console.service.read_all()
        assert tasks[0].title == "New Title"
        assert tasks[0].description == "New Desc"


class TestCLIDelete:
    """Additional test for delete command."""

    def test_delete_command_removes_task(self):
        """Delete command should remove task from list."""
        console = TodoConsole()

        # Create a task
        task = console.service.create("Task to Delete", "")
        assert len(console.service.read_all()) == 1

        # Delete via CLI (mock confirmation for interactive mode)
        console.do_delete(str(task.id))

        # Verify task removed
        assert len(console.service.read_all()) == 0


class TestCLINumberShortcuts:
    """Additional test for number-based navigation."""

    def test_number_shortcuts_work(self):
        """Number shortcuts (1-7) should map to commands."""
        console = TodoConsole()

        # Test that onecmd handles number inputs
        # Number 5 should map to 'list'
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            console.onecmd("5")
            output = mock_stdout.getvalue()

        # Should show list output (even if empty)
        assert "task" in output.lower() or "TODO LIST" in output


class TestCLICaseInsensitive:
    """Additional test for case-insensitive commands."""

    def test_commands_are_case_insensitive(self):
        """Commands should work regardless of case."""
        console = TodoConsole()

        # Test uppercase command
        console.onecmd("ADD \"Test\" \"Desc\"")
        tasks = console.service.read_all()
        assert len(tasks) == 1

        # Test mixed case
        console.onecmd("LiSt")
        # Should not raise error

        # Test lowercase
        console.onecmd("help")
        # Should not raise error
