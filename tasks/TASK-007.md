# TASK-007

Title

Developer Mode & User Mode

---

Status

Ready

---

Priority

High

---

Sprint

Sprint 2

---

Estimated Time

4-6 Hours

---

Objective

Separate the application into two experiences:

Developer Mode

User Mode

The application should no longer expose technical information to normal users.

---

Problem

Currently the Health Screen is useful only for developers.

Normal users should see a clean welcome experience.

---

Goal

Create Developer Mode.

Create User Mode.

Persist the selected mode.

---

Requirements

Default Mode

User Mode

Developer Mode should be accessible from Settings or a hidden Developer option.

---

User Mode

Show

LeadForgeAI Logo

Welcome Screen

Application Ready

Start Button

Recent Workspace

Current Workspace

No Backend Status

No Docker Status

No Database Status

No Technical Information

---

Developer Mode

Show

Backend Status

Database Status

Docker Status

n8n Status

Application Version

Logs

Startup Information

Future Debug Tools

---

Persistence

Remember the selected mode.

When the application restarts,

restore the previously selected mode.

---

Backend

Expose

GET

/api/v1/system/mode

PATCH

/api/v1/system/mode

---

Frontend

Create

Developer View

User View

Mode Switch

Smooth Transition

---

Acceptance Criteria

User Mode hides technical information.

Developer Mode exposes technical information.

Mode persists after restart.

No duplicated UI.

---

Definition of Done

Developer Mode Complete.

User Mode Complete.

Persistence Complete.

Desktop Integration Complete.

Committed.

---

Next Task

TASK-008

Application Layout System

---

End of Task