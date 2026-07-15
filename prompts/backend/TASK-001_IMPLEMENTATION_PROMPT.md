# LeadForgeAI

## AI Implementation Prompt

You are a Senior Software Engineer responsible for implementing TASK-001 of LeadForgeAI.

Read and strictly follow the project documentation before generating any code.

Required reading order:

docs/003_PROJECT_BIBLE.md

docs/005_ARCHITECTURE.md

docs/006_TECH_STACK.md

docs/008_API.md

tasks/TASK-001.md

Do not ignore these documents.

Architecture always takes priority over implementation.

---

# Objective

Bootstrap the LeadForgeAI project.

This task only creates the project foundation.

Do NOT implement business features.

Do NOT implement scraping.

Do NOT implement AI.

Do NOT implement authentication.

Do NOT implement database models.

Do NOT implement n8n integration.

---

# Backend

Create a FastAPI application.

Requirements

Python 3.13

FastAPI

Uvicorn

Environment configuration

Health endpoint

Project structure

Use clean architecture.

Suggested folders

app/

api/

core/

services/

repositories/

models/

schemas/

config/

utils/

main.py

The structure should remain extensible.

---

# Health Endpoint

GET

/health

Response

{
    "success": true,
    "status": "healthy",
    "application": "LeadForgeAI"
}

---

# Frontend

Create a React + TypeScript + Vite application.

The home page should contain:

Application Name

Application Status

Backend Status

Health Check Button

No routing.

No authentication.

No dashboard.

No business pages.

---

# Docker

Create Docker support.

docker-compose.yml

Backend

Frontend

The compose file should be ready for future PostgreSQL and Redis services.

Do not include PostgreSQL yet.

---

# Environment

Create

.env.example

Include placeholders for

Backend Port

Frontend Port

Future Database URL

Future OpenAI Key

Future Gemini Key

Future n8n URL

---

# README

Update README.

Include

Installation

Development

Running

Folder Structure

Requirements

---

# Code Quality

Use type hints.

Write clean code.

Avoid unnecessary abstraction.

Avoid duplicated logic.

Follow PEP8.

Use modern TypeScript.

---

# Output

Generate the complete implementation.

Create every required file.

Do not skip any configuration.

Do not leave TODO comments unless absolutely necessary.

At the end provide:

Created Files

Commands to Run

Expected Output

Possible Errors

Verification Steps