# LeadForgeAI

## AI Implementation Prompt

Read and follow:

1. prompts/MASTER_IMPLEMENTATION_PROMPT.md
2. CONTEXT.md
3. tasks/TASK-006.md

Implement TASK-006 only.

---

Objective

Implement the complete Power Button System.

Reuse the existing Health Module.

Do not duplicate health checks.

---

Implement

Startup Service

Startup State Manager

Startup API

Progress Manager

Startup Schemas

Startup Models (if required)

Frontend Startup Screen

Desktop Integration

---

Backend Flow

Receive Startup Request

↓

Run Health Checks Sequentially

↓

Track Current Step

↓

Track Progress

↓

Return Live Status

↓

Return Ready State

---

Startup Order

Backend

↓

Database

↓

Docker

↓

n8n

↓

Workspace

↓

Ready

---

Rules

Do not use fake loading.

Do not use sleep().

Every state must be real.

Every step must be reusable.

---

Frontend

Replace the existing bootstrap page.

Create:

Large Power Button

Startup Progress

Current Step

Progress Bar

Ready Screen

Retry Button

---

When Ready

Display

"LeadForgeAI is Ready"

with a Continue button.

Do not navigate yet.

Navigation will be implemented in future tasks.

---

Code Quality

FastAPI

React

TypeScript

Async

Reusable Components

No duplicated logic

No placeholder code

No TODO comments

---

Output

Generate:

TASK_COMPLETION_REPORT.md

GIT_DIFF_SUMMARY.md

Include:

Created Files

Modified Files

Commands

Verification Steps

Architecture Deviations (if any)

Stop after implementation and wait for review.