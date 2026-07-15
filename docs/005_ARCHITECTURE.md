# LeadForgeAI — System Architecture

Version: 1.0.0

Status: Draft

---

# Purpose

This document defines the complete technical architecture of LeadForgeAI.

Every service, module, API and workflow must follow this architecture.

No implementation may violate this document.

---

# Architecture Philosophy

LeadForgeAI is a modular desktop application.

Every major feature is an independent service.

No service should directly depend on another service's internal implementation.

Every communication must happen through APIs.

This allows services to be replaced without affecting the rest of the platform.

---

# High Level Architecture

                    User
                      │
                      ▼
          ┌────────────────────┐
          │ LeadForge Desktop  │
          │   (Tauri + React)  │
          └─────────┬──────────┘
                    │
            Local REST API
                    │
                    ▼
          ┌────────────────────┐
          │ FastAPI Backend    │
          └─────────┬──────────┘
                    │
      ┌─────────────┼──────────────┐
      │             │              │
      ▼             ▼              ▼
 PostgreSQL       n8n          AI Engine
      │             │              │
      ▼             ▼              ▼
 Scrapers      Workflows      Analysis

---

# Why This Architecture

The desktop application should never perform heavy processing.

Its responsibilities are:

- User Interface
- Authentication (future)
- Settings
- API Requests
- Status Monitoring

All business logic belongs inside the backend.

---

# Backend Responsibilities

The backend is the brain of LeadForgeAI.

Responsibilities include:

- Business Logic
- Database Operations
- Queue Management
- AI Communication
- Scraper Management
- Workflow Execution
- File Processing
- Export Management

The backend should never contain frontend code.

---

# Frontend Responsibilities

The frontend is responsible only for presentation.

Responsibilities:

- UI Rendering
- User Interaction
- API Calls
- Notifications
- Progress Indicators
- Dashboard
- Forms
- Charts

The frontend must never directly communicate with databases.

The frontend must never execute scraping logic.

---

# n8n Responsibilities

n8n is the automation engine.

Responsibilities:

- Workflow Execution
- Scheduling
- Integrations
- Notifications
- Automation

n8n should never contain business logic.

Business logic always belongs inside FastAPI.

---

# Database Responsibilities

PostgreSQL is the single source of truth.

Every module stores its data inside PostgreSQL.

No module should maintain its own independent database.

---

# AI Responsibilities

AI never accesses databases directly.

AI communicates only through backend APIs.

The backend prepares structured context before sending data to AI.

AI returns structured responses.

The backend validates AI output before storing it.

---

# Scraper Responsibilities

Scrapers never modify the database directly.

Flow:

Scraper

↓

Backend Validation

↓

Database

This prevents invalid data from entering the system.

---

# Core Rule

Desktop

↓

Backend

↓

Database

Never:

Desktop

↓

Database

---

END OF PART 1

---

# Module Architecture

LeadForgeAI is built using independent modules.

A module is a self-contained feature that performs one primary responsibility.

Every module must be able to evolve independently.

Modules communicate only through the Backend API.

Modules must never communicate directly with each other.

Example:

Maps Module

↓

Backend API

↓

Website Module

NOT

Maps Module

↓

Website Module

---

# Core Modules

The first stable version of LeadForgeAI will contain the following modules.

1. Dashboard

Displays application status and quick actions.

---

2. System Manager

Responsible for:

- Docker Health
- Service Status
- Startup
- Shutdown
- Health Monitoring

---

3. Business Discovery

Responsible for discovering businesses from supported public sources.

Output:

Business Records

---

4. People Discovery

Responsible for discovering publicly listed professionals associated with businesses.

Output:

People Records

---

5. Website Intelligence

Responsible for:

- Website Crawling
- Contact Pages
- About Pages
- Email Discovery
- Phone Discovery
- Social Links
- Basic Website Information

---

6. AI Intelligence

Responsible for:

Business Analysis

Lead Summary

Pain Points

Personalized Outreach

Lead Scoring

Suggestions

---

7. Campaign Manager

Responsible for:

Campaign Creation

Campaign Tracking

Campaign History

Campaign Statistics

---

8. Workflow Manager

Responsible for communicating with n8n.

Responsibilities:

Start Workflow

Stop Workflow

Resume Workflow

Monitor Workflow

Receive Results

---

9. Export Manager

Responsible for exporting data.

Supported formats:

CSV

Excel

JSON

Future formats may be added.

---

10. Settings Manager

Responsible for:

Application Settings

API Keys

AI Providers

Workspace Settings

Backup Settings

Theme

---

# Module Independence

Every module must satisfy the following rules.

The module owns its own logic.

The module never owns another module's logic.

The module never accesses another module's internal files.

Every interaction must happen through Backend APIs.

---

# Module Lifecycle

Every module follows the same lifecycle.

Load

↓

Initialize

↓

Health Check

↓

Ready

↓

Execute

↓

Idle

↓

Shutdown

---

# Module Failure

If one module fails,

the application should continue working whenever possible.

Example:

AI Module fails.

Business Discovery should still work.

Website Intelligence fails.

Dashboard should continue working.

Campaign Manager fails.

Export Manager should still work.

The application must degrade gracefully.

---

# Plugin Ready Architecture

Future modules should be installable without changing the core application.

Future examples:

Instagram Intelligence

YouTube Intelligence

Google Search Intelligence

CRM Integration

WhatsApp Automation

Future AI Providers

Every future module must follow the same module interface.

---

# Core Engineering Rule

The Core Application should know that a module exists.

The Core Application should never need to know how the module works internally.

---

END OF PART 2

---

# Service Lifecycle

LeadForgeAI is designed as a service-oriented desktop application.

Every service follows a predictable startup and shutdown lifecycle.

The user should never manually start individual services.

The application manages everything automatically.

---

# Startup Sequence

When the user launches LeadForgeAI, the following sequence is executed.

Step 1

Application Starts

↓

Step 2

Load User Workspace

↓

Step 3

Check Docker Engine

↓

Step 4

Check PostgreSQL

↓

Step 5

Check Redis

↓

Step 6

Check FastAPI Backend

↓

Step 7

Check n8n

↓

Step 8

Load Installed Modules

↓

Step 9

Run Health Checks

↓

Step 10

Dashboard Ready

---

# Power Button

The Power Button is the main entry point of the application.

The user should never manually execute Docker commands.

Pressing the Power Button should automatically:

Start required containers

Wait for healthy status

Verify backend connection

Verify database connection

Verify workflow engine

Load modules

Unlock dashboard

If every required service becomes healthy, the application enters Ready Mode.

---

# Ready Mode

The application is considered ready only if:

Docker is running

Backend is healthy

Database is healthy

n8n is connected

Workspace is loaded

Module registry is loaded

Only then can the user start workflows.

---

# Health Monitoring

The application continuously monitors every service.

Health checks run periodically.

If a service stops unexpectedly:

Show warning

Log event

Attempt recovery when possible

Keep unaffected modules running

The application should never crash because one service failed.

---

# Recovery Strategy

If Backend stops:

Disable actions requiring Backend

Keep UI alive

Retry connection automatically

If n8n stops:

Disable workflow execution

Keep remaining features active

If Database stops:

Switch application to read-only mode

Notify user immediately

---

# Shutdown Sequence

When closing the application:

Finish active operations

Save user state

Store logs

Close database connections

Disconnect services safely

Exit application

The application must never terminate while a write operation is in progress.

---

# Logging

Every important event must be logged.

Examples:

Application Started

Workspace Loaded

Workflow Started

Workflow Finished

Backend Offline

n8n Connected

Export Completed

Error Detected

Logs should help diagnose problems without requiring technical knowledge.

---

# Workspace

A Workspace is the logical container of everything a user creates.

Each workspace contains:

Business Data

People Data

Campaigns

Templates

Exports

History

Settings

Logs

AI Context

Workflows

A user may create multiple workspaces.

Workspaces must remain isolated from each other.

---

# Engineering Principle

Users interact only with the Desktop Application.

The Desktop Application manages every internal service automatically.

The user should never need to understand Docker, FastAPI, PostgreSQL or n8n.

Technology should remain invisible.

---

END OF PART 3