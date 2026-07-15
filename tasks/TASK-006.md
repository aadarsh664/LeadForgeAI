# TASK-006

Title

Power Button System

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

5-7 Hours

---

Objective

Implement the Power Button System.

The Power Button becomes the startup controller of LeadForgeAI.

Instead of immediately opening the application, the user presses one button and the application automatically verifies every required dependency before allowing access.

This is the heart of the startup experience.

---

Problem

Currently the application only displays system health.

The user cannot control the startup process.

There is no startup sequence.

---

Goal

Create a Startup Manager.

Create a Power Button.

Create Startup Pipeline.

Create Startup Progress UI.

Create Startup Validation.

---

Deliverables

Power Button

Startup Service

Startup State Manager

Startup Progress

Startup Result

Startup Logger

---

Requirements

When the user presses the Power Button:

Step 1

Verify Backend

↓

Step 2

Verify Database

↓

Step 3

Verify Docker

↓

Step 4

Verify n8n

↓

Step 5

Verify Workspace

↓

Step 6

Application Ready

Each step should update the UI in real time.

---

Rules

No fake loading.

No fixed timers.

Every status must come from real backend responses.

---

UI

Large Power Button

Progress Indicator

Current Step

Completed Steps

Failed Step

Retry Button

Ready Screen

---

Backend

Create Startup Service.

The service coordinates startup checks.

Do not duplicate health logic.

Reuse the Health Module.

---

Frontend

Create Startup Screen.

Display current startup step.

Display progress.

Disable button while startup is running.

Enable Retry if startup fails.

---

Endpoints

POST /api/v1/system/startup

GET /api/v1/system/startup/status

---

Response

Current Step

Completed Steps

Progress Percentage

Overall Status

Ready Boolean

Message

---

Acceptance Criteria

Power Button works.

Progress updates correctly.

No duplicated health logic.

Startup finishes successfully.

Application reaches Ready state.

---

Definition of Done

Startup Service Complete.

Power Button Complete.

Progress UI Complete.

API Complete.

Desktop Integration Complete.

Committed.

---

Next Task

TASK-007

Developer Mode

---

End of Task