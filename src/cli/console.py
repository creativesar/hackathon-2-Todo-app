"""Console REPL - professional UI design."""

import cmd
from src.services.task_service import TaskService


class TodoConsole(cmd.Cmd):
    """Interactive todo console with clean design."""

    prompt = "todo> "

    def __init__(self):
        super().__init__()
        self.service = TaskService()

    def default(self, line):
        """Handle unknown commands with better error messages."""
        cmd_name = line.split()[0].lower() if line else ""

        # Check if it's a misspelled command
        suggestions = {
            'ad': 'add',
            'ads': 'add',
            'upate': 'update',
            'updaet': 'update',
            'udpate': 'update',
            'comp': 'complete',
            'complet': 'complete',
            'del': 'delete',
            'delet': 'delete',
            'lst': 'list',
            'ls': 'list',
            'ex': 'exit',
            'quit': 'exit',
            'q': 'exit'
        }

        if cmd_name in suggestions:
            self.print_header("⚠ SUGGESTION")
            print(f"║  Did you mean: {suggestions[cmd_name]}?".ljust(51) + "║")
            self.print_footer()
        else:
            self.print_header("✗ UNKNOWN COMMAND")
            print(f"║  Command '{cmd_name}' not recognized".ljust(51) + "║")
            print("║  Type 'help' to see available commands".ljust(51) + "║")
            self.print_footer()

    def onecmd(self, line):
        """Override to make commands case-insensitive and handle number shortcuts."""
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line

        # Handle number shortcuts (1-7)
        number_shortcuts = {
            '1': 'add',
            '2': 'update',
            '3': 'complete',
            '4': 'delete',
            '5': 'list',
            '6': 'help',
            '7': 'exit'
        }

        # Make command case-insensitive
        if cmd:
            cmd = cmd.lower()
            # Check if it's a number shortcut
            if cmd in number_shortcuts:
                cmd = number_shortcuts[cmd]

        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)

    def print_header(self, title):
        """Print formatted header."""
        print()
        print("╔" + "═" * 50 + "╗")
        print(f"║{title:^50}║")
        print("╠" + "═" * 50 + "╣")

    def print_footer(self, extra=""):
        """Print formatted footer."""
        print("╚" + "═" * 50 + "╝")
        if extra:
            print(f"  {extra}")
        print()

    # ========== ADD ==========
    def do_add(self, args):
        """Add task: add "title" "description" """
        # Interactive mode if no arguments
        if not args.strip():
            self.print_header("➕ ADD NEW TASK")
            print("║".ljust(51) + "║")

            # Get title
            print("║  Enter task title:".ljust(51) + "║")
            print("║".ljust(51) + "║")
            title = input("  > ").strip()

            if not title:
                print()
                self.print_header("✗ ERROR")
                print("║  Title cannot be empty".ljust(51) + "║")
                self.print_footer()
                return

            # Get description
            print()
            self.print_header("➕ ADD NEW TASK")
            print("║".ljust(51) + "║")
            print(f"║  Title: {title}".ljust(51) + "║")
            print("║".ljust(51) + "║")
            print("║  Enter task description (optional):".ljust(51) + "║")
            print("║".ljust(51) + "║")
            desc = input("  > ").strip()

            task = self.service.create(title, desc)
            print()
            self.print_header("✓ TASK CREATED SUCCESSFULLY")
            print(f"║  Task ID:     #{task.id}".ljust(51) + "║")
            print(f"║  Title:       {task.title}".ljust(51) + "║")
            if task.description:
                print(f"║  Description: {task.description}".ljust(51) + "║")
            self.print_footer()
            return

        # Non-interactive mode with arguments
        parts = args.split('"', 2)
        if len(parts) >= 2:
            title = parts[1]
            desc = parts[3].strip('"') if len(parts) > 3 else ""
        else:
            title = args.strip()
            desc = ""

        if not title.strip():
            self.print_header("ERROR")
            print("║  Title cannot be empty".ljust(51) + "║")
            self.print_footer()
            return

        task = self.service.create(title.strip(), desc.strip())
        self.print_header("✓ TASK CREATED")
        print(f"║  Task ID:     #{task.id}".ljust(51) + "║")
        print(f"║  Title:       {task.title}".ljust(51) + "║")
        if task.description:
            print(f"║  Description: {task.description}".ljust(51) + "║")
        self.print_footer()

    # ========== LIST ==========
    def do_list(self, args):
        """List all tasks: list"""
        tasks = self.service.read_all()

        self.print_header("📋 TODO LIST")

        if not tasks:
            print("║".ljust(51) + "║")
            print("║  No tasks found".ljust(51) + "║")
            print("║".ljust(51) + "║")
            self.print_footer("✓ 0 tasks")
            return

        pending = sum(1 for t in tasks if not t.completed)
        completed = len(tasks) - pending

        for t in tasks:
            status = "✓" if t.completed else "○"
            print("║".ljust(51) + "║")
            print(f"║  {status} Task #{t.id}".ljust(51) + "║")
            print(f"║    Title:       {t.title}".ljust(51) + "║")
            if t.description:
                print(f"║    Description: {t.description}".ljust(51) + "║")

        print("║".ljust(51) + "║")
        self.print_footer(f"✓ Total: {len(tasks)} tasks | Pending: {pending} | Done: {completed}")

    # ========== COMPLETE ==========
    def do_complete(self, args):
        """Complete task: complete <id>"""
        # Interactive mode if no arguments
        if not args.strip():
            tasks = self.service.read_all()
            pending_tasks = [t for t in tasks if not t.completed]

            if not pending_tasks:
                self.print_header("✗ NO PENDING TASKS")
                print("║  All tasks are completed or no tasks exist".ljust(51) + "║")
                self.print_footer()
                return

            # Show pending tasks
            self.print_header("✓ COMPLETE TASK - SELECT TASK")
            print("║".ljust(51) + "║")
            print("║  Pending Tasks:".ljust(51) + "║")
            print("║".ljust(51) + "║")
            for t in pending_tasks:
                print(f"║  ○ [{t.id}] {t.title}".ljust(51) + "║")
            print("║".ljust(51) + "║")
            print("║  Enter task ID to mark as complete:".ljust(51) + "║")
            print("║".ljust(51) + "║")

            try:
                task_id = int(input("  > ").strip())
            except ValueError:
                print()
                self.print_header("✗ ERROR")
                print("║  Invalid ID. Please enter a number".ljust(51) + "║")
                self.print_footer()
                return

            task = self.service.complete(task_id)
            if task:
                print()
                self.print_header("✓ TASK COMPLETED SUCCESSFULLY")
                print(f"║  Task #{task.id} marked as done".ljust(51) + "║")
                print(f"║  {task.title}".ljust(51) + "║")
                self.print_footer()
            else:
                print()
                self.print_header("✗ ERROR")
                print(f"║  Task #{task_id} not found".ljust(51) + "║")
                self.print_footer()
            return

        # Non-interactive mode with argument
        try:
            task_id = int(args.strip())
            task = self.service.complete(task_id)
            if task:
                self.print_header("✓ TASK COMPLETED")
                print(f"║  Task #{task.id} marked as done".ljust(51) + "║")
                print(f"║  {task.title}".ljust(51) + "║")
                self.print_footer()
            else:
                self.print_header("✗ ERROR")
                print(f"║  Task #{task_id} not found".ljust(51) + "║")
                self.print_footer()
        except ValueError:
            self.print_header("USAGE: Complete Task")
            print("║  Command: complete <task_id>".ljust(51) + "║")
            print("║  Example: complete 1".ljust(51) + "║")
            self.print_footer()

    # ========== UPDATE ==========
    def do_update(self, args):
        """Update task: update <id> "new title" "new description" """
        # Interactive mode if no arguments
        if not args.strip():
            tasks = self.service.read_all()

            if not tasks:
                self.print_header("✗ NO TASKS")
                print("║  No tasks available to update".ljust(51) + "║")
                print("║  Create a task first using option 1".ljust(51) + "║")
                self.print_footer()
                return

            # Show available tasks
            self.print_header("🔄 UPDATE TASK - SELECT TASK")
            print("║".ljust(51) + "║")
            for t in tasks:
                status = "✓" if t.completed else "○"
                print(f"║  {status} [{t.id}] {t.title}".ljust(51) + "║")
            print("║".ljust(51) + "║")
            print("║  Enter task ID to update:".ljust(51) + "║")
            print("║".ljust(51) + "║")

            try:
                task_id = int(input("  > ").strip())
            except ValueError:
                print()
                self.print_header("✗ ERROR")
                print("║  Invalid ID. Please enter a number".ljust(51) + "║")
                self.print_footer()
                return

            # Find the task
            task_to_update = None
            for t in tasks:
                if t.id == task_id:
                    task_to_update = t
                    break

            if not task_to_update:
                print()
                self.print_header("✗ ERROR")
                print(f"║  Task #{task_id} not found".ljust(51) + "║")
                self.print_footer()
                return

            # Get new title
            print()
            self.print_header("🔄 UPDATE TASK")
            print("║".ljust(51) + "║")
            print(f"║  Current Title: {task_to_update.title}".ljust(51) + "║")
            print("║".ljust(51) + "║")
            print("║  Enter new title (or press Enter to keep):".ljust(51) + "║")
            print("║".ljust(51) + "║")
            new_title = input("  > ").strip()

            # Get new description
            print()
            self.print_header("🔄 UPDATE TASK")
            print("║".ljust(51) + "║")
            print(f"║  Current Description: {task_to_update.description}".ljust(51) + "║")
            print("║".ljust(51) + "║")
            print("║  Enter new description (or press Enter to keep):".ljust(51) + "║")
            print("║".ljust(51) + "║")
            new_desc = input("  > ").strip()

            # Update with new values or keep old ones
            final_title = new_title if new_title else None
            final_desc = new_desc if new_desc else None

            if not final_title and not final_desc:
                print()
                self.print_header("⚠ NO CHANGES")
                print("║  No changes made to the task".ljust(51) + "║")
                self.print_footer()
                return

            task = self.service.update(task_id, final_title, final_desc)
            print()
            self.print_header("✓ TASK UPDATED SUCCESSFULLY")
            print(f"║  Task #{task.id} has been updated".ljust(51) + "║")
            print(f"║  Title:       {task.title}".ljust(51) + "║")
            if task.description:
                print(f"║  Description: {task.description}".ljust(51) + "║")
            self.print_footer()
            return

        # Non-interactive mode with arguments
        try:
            parts = args.split('"', 3)
            task_id = int(parts[0].strip())
            new_title = parts[1] if len(parts) > 1 else None
            new_desc = parts[3].strip('"') if len(parts) > 3 else None

            task = self.service.update(task_id, new_title, new_desc)
            if task:
                self.print_header("✓ TASK UPDATED")
                print(f"║  Task #{task.id} updated successfully".ljust(51) + "║")
                self.print_footer()
            else:
                self.print_header("✗ ERROR")
                print(f"║  Task #{task_id} not found".ljust(51) + "║")
                self.print_footer()
        except (ValueError, IndexError):
            self.print_header("USAGE: Update Task")
            print("║  Command: update <id> \"title\" \"description\"".ljust(51) + "║")
            print("║  Example: update 1 \"New title\" \"New desc\"".ljust(51) + "║")
            self.print_footer()

    # ========== DELETE ==========
    def do_delete(self, args):
        """Delete task: delete <id>"""
        # Interactive mode if no arguments
        if not args.strip():
            tasks = self.service.read_all()

            if not tasks:
                self.print_header("✗ NO TASKS")
                print("║  No tasks available to delete".ljust(51) + "║")
                self.print_footer()
                return

            # Show all tasks
            self.print_header("🗑 DELETE TASK - SELECT TASK")
            print("║".ljust(51) + "║")
            for t in tasks:
                status = "✓" if t.completed else "○"
                print(f"║  {status} [{t.id}] {t.title}".ljust(51) + "║")
            print("║".ljust(51) + "║")
            print("║  Enter task ID to delete:".ljust(51) + "║")
            print("║".ljust(51) + "║")

            try:
                task_id = int(input("  > ").strip())
            except ValueError:
                print()
                self.print_header("✗ ERROR")
                print("║  Invalid ID. Please enter a number".ljust(51) + "║")
                self.print_footer()
                return

            # Confirmation
            print()
            self.print_header("⚠ CONFIRM DELETE")
            print("║".ljust(51) + "║")
            print(f"║  Are you sure you want to delete Task #{task_id}?".ljust(51) + "║")
            print("║  Type 'yes' to confirm or 'no' to cancel:".ljust(51) + "║")
            print("║".ljust(51) + "║")
            confirm = input("  > ").strip().lower()

            if confirm != 'yes':
                print()
                self.print_header("⚠ CANCELLED")
                print("║  Delete operation cancelled".ljust(51) + "║")
                self.print_footer()
                return

            if self.service.delete(task_id):
                print()
                self.print_header("✓ TASK DELETED SUCCESSFULLY")
                print(f"║  Task #{task_id} has been deleted".ljust(51) + "║")
                self.print_footer()
            else:
                print()
                self.print_header("✗ ERROR")
                print(f"║  Task #{task_id} not found".ljust(51) + "║")
                self.print_footer()
            return

        # Non-interactive mode with argument
        try:
            task_id = int(args.strip())
            if self.service.delete(task_id):
                self.print_header("✓ TASK DELETED")
                print(f"║  Task #{task_id} deleted successfully".ljust(51) + "║")
                self.print_footer()
            else:
                self.print_header("✗ ERROR")
                print(f"║  Task #{task_id} not found".ljust(51) + "║")
                self.print_footer()
        except ValueError:
            self.print_header("USAGE: Delete Task")
            print("║  Command: delete <task_id>".ljust(51) + "║")
            print("║  Example: delete 1".ljust(51) + "║")
            self.print_footer()

    # ========== HELP ==========
    def do_help(self, args):
        """Show help: help"""
        self.print_header("📖 HELP - AVAILABLE COMMANDS")
        print("║".ljust(51) + "║")
        print("║  1. Add Task".ljust(51) + "║")
        print("║     add \"title\" \"description\"".ljust(51) + "║")
        print("║     Example: add \"Buy milk\" \"From store\"".ljust(51) + "║")
        print("║".ljust(51) + "║")
        print("║  2. Update Task".ljust(51) + "║")
        print("║     update <id> \"title\" \"description\"".ljust(51) + "║")
        print("║     Example: update 1 \"New title\" \"New desc\"".ljust(51) + "║")
        print("║".ljust(51) + "║")
        print("║  3. Complete Task".ljust(51) + "║")
        print("║     complete <id>".ljust(51) + "║")
        print("║     Example: complete 1".ljust(51) + "║")
        print("║".ljust(51) + "║")
        print("║  4. Delete Task".ljust(51) + "║")
        print("║     delete <id>".ljust(51) + "║")
        print("║     Example: delete 1".ljust(51) + "║")
        print("║".ljust(51) + "║")
        print("║  5. List Tasks".ljust(51) + "║")
        print("║     list".ljust(51) + "║")
        print("║".ljust(51) + "║")
        print("║  6. Help".ljust(51) + "║")
        print("║     help".ljust(51) + "║")
        print("║".ljust(51) + "║")
        print("║  7. Exit".ljust(51) + "║")
        print("║     exit or quit".ljust(51) + "║")
        print("║".ljust(51) + "║")
        self.print_footer()

    # ========== EXIT ==========
    def do_exit(self, args):
        """Exit: exit"""
        print()
        print("╔" + "═" * 50 + "╗")
        print("║" + " Thank you for using Todo Console App! ".center(50) + "║")
        print("║" + " Goodbye! ".center(50) + "║")
        print("╚" + "═" * 50 + "╝")
        print()
        return True

    def do_quit(self, args):
        """Quit: quit"""
        return self.do_exit(args)
