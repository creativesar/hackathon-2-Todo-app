"""Main entry point."""

from src.cli.console import TodoConsole


def main():
    print()
    print("+" + "-" * 48 + "+")
    print("|" + " TODO CONSOLE APP ".center(48) + "|")
    print("+" + "-" * 48 + "+")
    print("|" + " Type 'help' for commands ".center(48) + "|")
    print("+" + "-" * 48 + "+")
    print()

    console = TodoConsole()
    try:
        console.cmdloop()
    except KeyboardInterrupt:
        print("\n  Goodbye!\n")


if __name__ == "__main__":
    main()
