# LeadForgeAI

## AI Implementation Prompt

Implement TASK-002.

Read first:

docs/003_PROJECT_BIBLE.md

docs/005_ARCHITECTURE.md

docs/006_TECH_STACK.md

docs/007_DATABASE.md

tasks/TASK-002.md

Architecture takes priority over implementation.

---

Objective

Bootstrap the database layer.

No business logic.

No business tables.

No AI.

No authentication.

---

Requirements

Python 3.13

SQLAlchemy 2.x

Alembic

PostgreSQL

AsyncPG

Environment variables

Clean Architecture

---

Implement

Database Configuration

Database Session

Base ORM Model

Alembic Initialization

Health Database Service

Database Dependency Injection

---

Health Endpoint

GET /health

Response Example

{
    "success": true,
    "status": "healthy",
    "database": "connected"
}

If the database is unavailable

Return

{
    "success": false,
    "database": "disconnected"
}

with appropriate HTTP status.

---

Folder Structure

app/

core/

database.py

session.py

models/

base.py

dependencies/

database.py

---

Code Rules

PEP8

Type Hints

Async First

No TODO comments

No placeholder code

No fake implementations

---

Output

Generate every required file.

Generate Alembic configuration.

Generate Docker changes.

Generate .env.example updates.

Generate startup instructions.

List every created file.

List commands.

List verification steps.
