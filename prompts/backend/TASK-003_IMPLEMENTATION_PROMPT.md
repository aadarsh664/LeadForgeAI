# LeadForgeAI

## AI Implementation Prompt

Implement TASK-003.

Read:

docs/003_PROJECT_BIBLE.md

docs/005_ARCHITECTURE.md

docs/007_DATABASE.md

docs/008_API.md

tasks/TASK-003.md

Follow architecture strictly.

---

Objective

Implement the Workspace module.

Do not implement Business.

Do not implement AI.

Do not implement Campaigns.

---

Implement

Workspace ORM Model

Workspace Repository

Workspace Service

Workspace API

Workspace Schemas

Alembic Migration

Validation

---

Architecture Rules

Repository Layer

↓

Service Layer

↓

API Layer

No business logic inside API.

No SQL inside Service.

---

Workspace Model

UUID Primary Key

Name

Description

Status

Created At

Updated At

Deleted At

---

Validation

Workspace Name Required

Workspace Name Unique

Description Optional

---

API

POST

GET

PATCH

DELETE

Return standard API responses.

---

Code Quality

SQLAlchemy 2.x

PEP8

Type Hints

Async

No duplicated code

No placeholder code

---

Output

Generate every required file.

Generate migration.

Update routers.

Update dependencies.

Update README if required.

List every generated file.

Provide commands.

Provide verification steps.