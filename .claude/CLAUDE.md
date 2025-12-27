@specs/phase1-console/spec.md
@specs/phase1-console/plan.md
@specs/phase1-console/tasks.md

# Todo Console App - Phase I

## Spec-Driven Development

This project follows Spec-Driven Development with Claude Code:
1. Read relevant spec files before implementing
2. Reference spec/plan/tasks in implementation decisions
3. Update artifacts if requirements change

## Project Structure

- `src/` - Python source code
  - `models/` - Data structures (Task dataclass)
  - `services/` - Business logic (TaskService)
  - `cli/` - Console interface (cmd-based REPL)
- `tests/` - Unit tests with pytest
- `specs/phase1-console/` - Design documents (spec, plan, tasks)

## Commands

- Run app: `python -m src.main` or `todo`
- Run tests: `pytest`
