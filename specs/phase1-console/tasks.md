# Tasks: Phase I - Todo Console App

**Input**: Design documents from `specs/phase1-console/`
**Prerequisites**: plan.md ✓, spec.md ✓

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `pyproject.toml` with project metadata and dependencies
- [x] T002 Create `src/__init__.py` package marker
- [x] T003 Create `tests/__init__.py` package marker
- [x] T004 Create `.claude/CLAUDE.md` with project instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create `src/models/task.py` with Task dataclass
- [x] T006 Create `src/services/task_service.py` with TaskService class
- [x] T007 [P] Create `tests/test_task_service.py` with pytest fixtures

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks with title and optional description

**Independent Test**: `add "Test"` creates a task visible in `list`

### Tests for User Story 1

- [x] T008 [P] [US1] Test `add_task()` creates task with correct fields in `tests/test_task_service.py`
- [x] T009 [P] [US1] Test `add_task()` rejects empty title in `tests/test_task_service.py`

### Implementation for User Story 1

- [x] T010 [US1] Implement `add_task()` method in `src/services/task_service.py`
- [x] T011 [US1] Add task title validation (non-empty, max 200 chars)

**Checkpoint**: User Story 1 should be fully functional

---

## Phase 4: User Story 2 - View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can see all tasks with their status

**Independent Test**: `list` shows all created tasks with status

### Tests for User Story 2

- [x] T012 [P] [US2] Test `list_tasks()` returns empty list when no tasks in `tests/test_task_service.py`
- [x] T013 [P] [US2] Test `list_tasks()` returns all tasks in `tests/test_task_service.py`
- [x] T014 [P] [US2] Test task display format (ID, title, status)

### Implementation for User Story 2

- [x] T015 [US2] Implement `list_tasks()` method in `src/services/task_service.py`
- [x] T016 [US2] Create formatted output with status indicators ([ ] / [x])

**Checkpoint**: User Stories 1 AND 2 should both work

---

## Phase 5: User Story 3 - Mark Task Complete (Priority: P1) 🎯 MVP

**Goal**: Users can mark tasks as done

**Independent Test**: `complete 1` changes task status

### Tests for User Story 3

- [x] T017 [P] [US3] Test `complete_task()` changes status to True in `tests/test_task_service.py`
- [x] T018 [P] [US3] Test `complete_task()` raises error for invalid ID in `tests/test_task_service.py`

### Implementation for User Story 3

- [x] T019 [US3] Implement `complete_task()` method in `src/services/task_service.py`
- [x] T020 [US3] Add ID validation and task existence check

**Checkpoint**: Core CRUD operations are functional

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Users can modify task title and/or description

**Independent Test**: `update 1 "New Title"` changes the task

### Tests for User Story 4

- [x] T021 [P] [US4] Test `update_task()` changes title in `tests/test_task_service.py`
- [x] T022 [P] [US4] Test `update_task()` changes description in `tests/test_task_service.py`
- [x] T023 [P] [US4] Test `update_task()` raises error for invalid ID

### Implementation for User Story 4

- [x] T024 [US4] Implement `update_task()` method in `src/services/task_service.py`
- [x] T025 [US4] Add partial update support (update only title OR description)

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Users can remove tasks from the list

**Independent Test**: `delete 1` removes the task from list

### Tests for User Story 5

- [x] T026 [P] [US5] Test `delete_task()` removes task from list in `tests/test_task_service.py`
- [x] T027 [P] [US5] Test `delete_task()` raises error for invalid ID

### Implementation for User Story 5

- [x] T028 [US5] Implement `delete_task()` method in `src/services/task_service.py`
- [x] T029 [US5] Add ID validation and task existence check

---

## Phase 8: User Story 6 - CLI Interface (Priority: P2)

**Goal**: Provide console interface for all commands

**Independent Test**: All commands work from command line

### Tests for CLI

- [ ] T030 [P] [US6] Test CLI help command output
- [ ] T031 [P] [US6] Test CLI add command integration
- [ ] T032 [P] [US6] Test CLI list command integration
- [ ] T033 [P] [US6] Test CLI complete command integration

### Implementation for CLI

- [x] T034 [US6] Create `src/cli/console.py` with cmd.Cmd-based REPL
- [x] T035 [US6] Implement `do_add()` command handler (for: `> add "Title" ["Description"]`)
- [x] T036 [US6] Implement `do_list()` command handler (for: `> list`)
- [x] T037 [US6] Implement `do_complete()` command handler (for: `> complete <id>`)
- [x] T038 [US6] Implement `do_update()` command handler (for: `> update <id> ["Title"] ["Description"]`)
- [x] T039 [US6] Implement `do_delete()` command handler (for: `> delete <id>`)
- [x] T040 [US6] Implement `do_help()` command handler (for: `> help`)
- [x] T041 [US6] Add custom prompt with `> ` prefix using cmd.Cmd.prompt

---

## Phase 9: Entry Point & Integration (Priority: P2)

**Goal**: Connect CLI to service layer

- [x] T042 Create `src/main.py` entry point that runs REPL
- [x] T043 Wire up TaskService to CLI commands
- [x] T044 Add error handling at top level

---

## Phase 10: Bonus - Reusable Intelligence (Priority: BONUS)

**Goal**: Create Claude Code subagent for task operations (+200 points)

**Purpose**: Reusable intelligence that can be used across phases

### Bonus Tasks

- [ ] TB001 Create `.claude/agents/task-operations.md` subagent definition
- [ ] TB002 Document all task CRUD patterns for reuse
- [ ] TB003 Create example prompts for the subagent

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational
- **CLI Interface (Phase 8)**: Depends on service layer completion
- **Entry Point (Phase 9)**: Depends on CLI completion
- **Bonus (Phase 10)**: Independent, can be done anytime

### User Story Dependencies

| Story | Can Start After | Dependencies |
|-------|-----------------|--------------|
| US1 (Add) | Phase 2 | None |
| US2 (List) | Phase 2 | None |
| US3 (Complete) | Phase 2 | None |
| US4 (Update) | Phase 2 | None |
| US5 (Delete) | Phase 2 | None |
| US6 (CLI) | Phases 3-5 | Service layer |

### Parallel Opportunities

- T005, T006, T007 can run in parallel
- T008-T011 can run in parallel (different files)
- T012-T016 can run in parallel
- All CLI commands (T035-T040) can run in parallel
- Bonus tasks (TB001-TB003) can run in parallel

---

## Notes

- **[P]** tasks = different files, no dependencies
- **[Story]** label maps task to specific user story
- Each user story should be independently completable
- Verify tests fail before implementing
- Commit after each task or logical group

## Clarifications

### Session 2025-12-28

- Q: CLI library for REPL? → A: Use Python's built-in `cmd` module with `Cmd.prompt = "> "` for REPL style. Not argparse (which is for one-shot CLI arguments).
