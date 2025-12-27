---
id: "003"
title: "Clarify tasks.md CLI library"
stage: "clarify"
date: "2025-12-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "phase1-console"
branch: "main"
user: "user"
command: "/sp.clarify tasks.md"
labels: ["spec-driven-development", "clarification", "tasks", "todo-app"]
links:
  spec: "specs/phase1-console/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/phase1-console/tasks.md"
tests:
  - "null"
---

## Prompt

/sp.clarify tasks.md

## Response snapshot

Found mismatch: tasks.md specified argparse-based CLI but spec clarified REPL with session. Resolved with:

- Clarified: Use Python's built-in `cmd` module for REPL (not argparse)
- Updated CLI implementation tasks to use `do_add()`, `do_list()`, etc. naming convention
- Added T041 for custom prompt with `> ` prefix
- Renumbered entry point tasks to avoid ID collision

## Outcome

- ✅ Impact: Tasks now aligned with spec for REPL-style interaction
- 📁 Files: Updated specs/phase1-console/tasks.md
- 🔁 Next prompts: /sp.implement to execute tasks
- 🧠 Reflection: Caught inconsistency before implementation - using wrong library would have required full rewrite

## Evaluation notes (flywheel)

- Failure modes observed: N/A - clarification completed successfully
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
