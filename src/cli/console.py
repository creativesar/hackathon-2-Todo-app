"""Console REPL - professional UI design."""

import cmd
from src.services.task_service import TaskService


class TodoConsole(cmd.Cmd):
    """Interactive todo console with clean design."""

    prompt = "> "

    def __init__(self):
        super().__init__()
        self.service = TaskService()

    def print_header(self, title):
        """Print formatted header."""
        print()
        print("+" + "-" * 48 + "+")
        print(f"|{title:^48}|")
        print("+" + "-" * 48 + "+")

    def print_footer(self, extra=""):
        """Print formatted footer."""
        print("+" + "-" * 48 + "+")
        if extra:
            print(f"|{extra:^48}|")
            print("+" + "-" * 48 + "+")
        print()

    # ========== ADD ==========
    def do_add(self, args):
        """Add task: add "title" "description" """
        if not args.strip():
            self.print_header("USAGE")
            print("|  Command: add \"title\" \"description\"")
            print("|  Example: add \"Buy groceries\" \"Milk, eggs\"")
            self.print_footer()
            return

        parts = args.split('"', 2)
        if len(parts) >= 2:
            title = parts[1]
            desc = parts[3].strip('"') if len(parts) > 3 else ""
        else:
            title = args.strip()
            desc = ""

        if not title.strip():
            self.print_header("ERROR")
            print("|  Title cannot be empty")
            self.print_footer()
            return

        task = self.service.create(title.strip(), desc.strip())
        self.print_header("TASK CREATED")
        print(f"|  Task ID:     {task.id}")
        print(f"|  Title:       {task.title}")
        if task.description:
            print(f"|  Description: {task.description}")
        self.print_footer()

    # ========== LIST ==========
    def do_list(self, args):
        """List all tasks: list"""
        tasks = self.service.read_all()

        self.print_header("TODO LIST")

        if not tasks:
            print("|")
            print("|  No tasks found")
            print("|")
            self.print_footer("0 tasks")
            return

        pending = sum(1 for t in tasks if not t.completed)
        completed = len(tasks) - pending

        for t in tasks:
            status = "[X]" if t.completed else "[ ]"
            print("|")
            print(f"|  Task #{t.id}  {status}")
            print(f"|  Title:       {t.title}")
            if t.description:
                print(f"|  Description: {t.description}")
            print("|")

        self.print_footer(f"{len(tasks)} tasks ({pending} pending, {completed} done)")

    # ========== COMPLETE ==========
    def do_complete(self, args):
        """Complete task: complete <id>"""
        try:
            task_id = int(args.strip())
            task = self.service.complete(task_id)
            if task:
                self.print_header("TASK COMPLETED")
                print(f"|  Task #{task.id} marked as done")
                print(f"|  {task.title}")
                self.print_footer()
            else:
                self.print_header("ERROR")
                print(f"|  Task #{task_id} not found")
                self.print_footer()
        except ValueError:
            self.print_header("USAGE")
            print("|  Command: complete <task_id>")
            print("|  Example: complete 1")
            self.print_footer()

    # ========== UPDATE ==========
    def do_update(self, args):
        """Update task: update <id> "new title" "new description" """
        try:
            parts = args.split('"', 3)
            task_id = int(parts[0].strip())
            new_title = parts[1] if len(parts) > 1 else None
            new_desc = parts[3].strip('"') if len(parts) > 3 else None

            task = self.service.update(task_id, new_title, new_desc)
            if task:
                self.print_header("TASK UPDATED")
                print(f"|  Task #{task.id} updated successfully")
                self.print_footer()
            else:
                self.print_header("ERROR")
                print(f"|  Task #{task_id} not found")
                self.print_footer()
        except (ValueError, IndexError):
            self.print_header("USAGE")
            print("|  Command: update <id> \"title\" \"description\"")
            print("|  Example: update 1 \"New title\" \"New description\"")
            self.print_footer()

    # ========== DELETE ==========
    def do_delete(self, args):
        """Delete task: delete <id>"""
        try:
            task_id = int(args.strip())
            if self.service.delete(task_id):
                self.print_header("TASK DELETED")
                print(f"|  Task #{task_id} deleted successfully")
                self.print_footer()
            else:
                self.print_header("ERROR")
                print(f"|  Task #{task_id} not found")
                self.print_footer()
        except ValueError:
            self.print_header("USAGE")
            print("|  Command: delete <task_id>")
            print("|  Example: delete 1")
            self.print_footer()

    # ========== HELP ==========
    def do_help(self, args):
        """Show help: help"""
        self.print_header("COMMANDS")
        print("|")
        print("|  add \"title\" \"desc\"      Add new task")
        print("|  list                     Show all tasks")
        print("|  complete <id>            Mark task complete")
        print("|  update <id> \"t\" \"d\"      Update task")
        print("|  delete <id>              Delete task")
        print("|  help                     Show this help")
        print("|  exit                     Quit application")
        print("|")
        self.print_footer()

    # ========== EXIT ==========
    def do_exit(self, args):
        """Exit: exit"""
        print("\n  Goodbye!\n")
        return True

    def do_quit(self, args):
        """Quit: quit"""
        return self.do_exit(args)
