# LeadForgeAI

Read

MASTER_IMPLEMENTATION_PROMPT.md

CONTEXT.md

TASK-016.md

Implement TASK-016 only.

---

Objective

Build the complete Search Execution Engine.

This is the production execution infrastructure.

Do not implement Google Maps.

Do not implement scraping.

---

Implement

Search Jobs

Worker

Queue

Progress

Cancellation

Retry

Persistence

Events

Execution APIs

Frontend Progress UI

Running Jobs

Completed Jobs

Cancelled Jobs

---

Architecture

Every provider must execute through the Search Execution Engine.

Never call providers directly from the UI.

---

Rules

No polling loops with fake delays.

No sleep().

Use proper asynchronous architecture.

Keep UI synchronized with backend state.

Reuse existing Search Engine.

Reuse existing Provider Registry.

Reuse existing Design System.

---

Persistence

Local JSON only.

Future SQL compatible.

---

UI Requirements

Inter

Helvetica Neue

Never Arial

Apple Human Interface Guidelines

Linear

Raycast

Professional

Minimal

---

Code Quality

Production Ready

SOLID

Dependency Injection

No duplicated logic

No TODO comments

No placeholder code

---

Output

Generate

TASK_COMPLETION_REPORT.md

GIT_DIFF_SUMMARY.md

Architecture Diagram

API List

Created Files

Modified Files

Verification Steps

Performance Notes

Stop after implementation.

Wait for review.