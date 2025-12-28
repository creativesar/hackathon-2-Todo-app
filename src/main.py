"""Main entry point."""

from src.cli.console import TodoConsole


def main():
    print()
    print("╔" + "═" * 50 + "╗")
    print("║" + " TODO CONSOLE APP ".center(50) + "║")
    print("╠" + "═" * 50 + "╣")
    print("║" + "".ljust(50) + "║")
    print("║" + "  AVAILABLE COMMANDS:".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("║" + "  1. Add Task".ljust(50) + "║")
    print("║" + "     Command: add \"title\" \"description\"".ljust(50) + "║")
    print("║" + "     Description: Create a new todo task with".ljust(50) + "║")
    print("║" + "                  title and description".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("║" + "  2. Update Task".ljust(50) + "║")
    print("║" + "     Command: update <id> \"title\" \"description\"".ljust(50) + "║")
    print("║" + "     Description: Modify an existing task by".ljust(50) + "║")
    print("║" + "                  providing task ID".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("║" + "  3. Complete Task".ljust(50) + "║")
    print("║" + "     Command: complete <id>".ljust(50) + "║")
    print("║" + "     Description: Mark a task as completed".ljust(50) + "║")
    print("║" + "                  by its ID".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("║" + "  4. Delete Task".ljust(50) + "║")
    print("║" + "     Command: delete <id>".ljust(50) + "║")
    print("║" + "     Description: Permanently remove a task".ljust(50) + "║")
    print("║" + "                  by its ID".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("║" + "  5. List All Tasks".ljust(50) + "║")
    print("║" + "     Command: list".ljust(50) + "║")
    print("║" + "     Description: Display all tasks with their".ljust(50) + "║")
    print("║" + "                  status (pending/completed)".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("║" + "  6. Help".ljust(50) + "║")
    print("║" + "     Command: help".ljust(50) + "║")
    print("║" + "     Description: Show detailed help menu with".ljust(50) + "║")
    print("║" + "                  examples".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("║" + "  7. Exit".ljust(50) + "║")
    print("║" + "     Command: exit".ljust(50) + "║")
    print("║" + "     Description: Quit the application".ljust(50) + "║")
    print("║" + "".ljust(50) + "║")
    print("╠" + "═" * 50 + "╣")
    print("║" + " 👉 Press a number (1-7) to continue... ".ljust(50) + "║")
    print("╚" + "═" * 50 + "╝")
    print()

    console = TodoConsole()
    try:
        console.cmdloop()
    except KeyboardInterrupt:
        print("\n  Goodbye!\n")


if __name__ == "__main__":
    main()
