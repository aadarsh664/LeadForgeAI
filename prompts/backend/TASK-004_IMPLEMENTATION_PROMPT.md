# LeadForgeAI

## AI Implementation Prompt

Implement TASK-004.

Read:

docs/003_PROJECT_BIBLE.md

docs/005_ARCHITECTURE.md

docs/008_API.md

tasks/TASK-004.md

Follow the architecture exactly.

---

Objective

Implement the Health Module.

No Business Module.

No AI.

No Campaigns.

No Workflows.

Only Health.

---

Implement

Health Service

Health Checker

Health API

Schemas

Dependencies

Version Reader

---

Health Checks

Backend

Database

Docker

n8n

Application

Workspace

Future checks must be easy to add.

---

API

GET /api/v1/health

Return

Application

Version

Backend

Database

Docker

n8n

Timestamp

Overall Status

---

Docker

Detect whether Docker Engine is available.

Do not start Docker.

Only report health.

---

n8n

Detect whether n8n API is reachable.

Do not create workflows.

Only report health.

---

Database

Verify active connection.

---

Architecture

API

↓

Service

↓

Health Checker

No business logic inside API.

---

Code Rules

Python 3.13

FastAPI

Async

PEP8

Type Hints

Reusable Components

No placeholder code

No TODO comments

---

Output

Generate all required files.

Update routers.

Update dependencies.

Provide verification commands.

Provide created file list.

Provide expected output.
