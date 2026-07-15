# TASK-002

Title

Database Bootstrap

---

Status

Ready

---

Priority

Critical

---

Sprint

Sprint 1

---

Estimated Time

3-5 Hours

---

Objective

Bootstrap the database layer of LeadForgeAI.

The objective is to establish a production-ready database architecture without implementing business features.

---

Problem

The backend currently has no persistence layer.

Future modules require a stable database foundation.

---

Goal

Configure PostgreSQL.

Configure SQLAlchemy.

Configure Alembic.

Create Base Model.

Create Database Session.

Create Health Database Check.

No business tables.

---

Deliverables

Database Connection

SQLAlchemy Setup

Alembic Migration

Base Model

Database Session

Database Health Service

---

Files

backend/app/core/database.py

backend/app/core/session.py

backend/app/models/base.py

backend/alembic/

backend/alembic.ini

backend/.env.example

docker-compose.yml

---

Requirements

Use PostgreSQL.

Use SQLAlchemy 2.x.

Use Alembic.

Environment driven configuration.

Async architecture.

No ORM models except Base.

No tables except Alembic Version.

Health endpoint should verify database connectivity.

---

Acceptance Criteria

Database container starts.

Backend connects successfully.

Alembic initializes successfully.

Health endpoint returns database healthy.

No warnings.

No errors.

---

Definition of Done

Database running.

Migration successful.

Health API updated.

README updated.

Committed.

---

Output

Database URL configurable through .env

Migration system operational.

Ready for Task-003.

---

Next Task

TASK-003

Workspace Foundation

---

End of Task