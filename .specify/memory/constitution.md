# Todo Console App Constitution

**Phase**: In-Memory Python Console Application

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All code generation MUST follow the SDD-RI workflow:
- Constitution → Specify → Plan → Tasks → Implement
- No code written manually - Claude Code generates all implementation
- Specs must be refined until Claude Code produces correct output
- Every implementation task must reference a task ID from tasks.md

### II. Clean Architecture
- Separation of concerns: CLI interface, business logic, data layer
- Single responsibility: Each function/class does one thing well
- No boilerplate: Minimal, focused code that delivers value
- Follow Python best practices (PEP 8, type hints, docstrings)

### III. In-Memory Data Storage
- Task data stored in Python list/dict structure (no database for Phase I)
- Data persists only while application runs
- No external file I/O required for Phase I

### IV. Console UX Excellence
- Clear command descriptions and usage instructions
- Informative feedback for every action (success/error states)
- Input validation with helpful error messages
- Consistent output format

### V. Testable Design
- All core functions must be importable and testable independently
- No hardcoded stdin/stdout in business logic functions
- Business logic separated from CLI presentation layer

## Development Workflow

### Phase Execution Order
1. **Constitution** (this file) - Project principles and constraints
2. **Spec** (`specs/phase1-console/spec.md`) - Feature requirements and user stories
3. **Plan** (`specs/phase1-console/plan.md`) - Technical architecture
4. **Tasks** (`specs/phase1-console/tasks.md`) - Implementation checklist
5. **Implement** - Claude Code generates code from tasks

### Code Generation Rules
- Claude Code MUST reference task IDs from tasks.md
- Claude Code MUST cite file paths in code comments
- Claude Code MUST NOT invent APIs or features not in spec
- If spec is unclear, Claude Code MUST ask for clarification

## Quality Standards

### Code Requirements
- Type hints for all function signatures
- Docstrings for all public functions and classes
- Max 50 lines per function (split if longer)
- No linting errors

### Error Handling
- Graceful handling of invalid inputs
- Clear error messages that help user correct the issue
- No crashes - always provide feedback

### User Experience
- Commands: add, list, update, delete, complete, help, exit
- Consistent command structure across all operations
- Visual indicators for task status (e.g., [ ] pending, [x] complete)

## Bonus Points Strategy (Phase I Eligible)

### Reusable Intelligence (+200 points) - ELIGIBLE IN PHASE I
- Create Claude Code subagents for common operations
- Document reusable patterns in .claude/agents/
- Example: A "task-operations" subagent that handles all CRUD operations

### Cloud-Native Blueprints (+200 points) - NOT ELIGIBLE IN PHASE I
- Requires Kubernetes deployment (Phase IV/V)
- Skip for Phase I

### Multi-language Support (+100 points) - NOT ELIGIBLE IN PHASE I
- Requires chatbot interface (Phase III)
- Skip for Phase I

### Voice Commands (+200 points) - NOT ELIGIBLE IN PHASE I
- Requires chatbot interface (Phase III)
- Skip for Phase I

**Bonus Points Achievable in Phase I**: +200 (Reusable Intelligence only)

## Project Structure

```
hackathon-todo/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   └── task.py          # Task data model
│   ├── services/
│   │   └── task_service.py  # Business logic (in-memory storage)
│   ├── cli/
│   │   └── console.py       # CLI interface
│   └── main.py              # Entry point
├── tests/
│   ├── __init__.py
│   └── test_task_service.py # Core functionality tests
├── specs/
│   └── phase1-console/
│       ├── constitution.md
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── .claude/
│   ├── CLAUDE.md
│   └── agents/
│       └── task-operations.md  # Reusable subagent (bonus)
├── pyproject.toml
└── README.md
```

## Constitution Compliance

All PRs/reviews must verify:
- [ ] Code follows spec exactly (no invented features)
- [ ] Task IDs referenced in all implementations
- [ ] Type hints and docstrings present
- [ ] Error handling covers edge cases
- [ ] Tests verify core functionality

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
