# LeadForgeAI — Project Context

Version: 1.0.0

Status: Active

Purpose

This document provides a high-level overview of the LeadForgeAI project.

It is intended for AI coding assistants and new contributors.

Read this document before reading any Task.

For detailed rules, refer to the Project Bible.

---

# Project Summary

LeadForgeAI is a Local-First Lead Intelligence Platform.

It is designed to discover, enrich, organize, analyze and automate publicly available business information.

The application is self-hosted and beginner friendly.

The user should never need to understand Docker, PostgreSQL, FastAPI or n8n.

The software manages everything internally.

---

# Core Mission

Build a production-grade Lead Intelligence Platform that combines lead discovery, enrichment, AI analysis and automation into one desktop application.

---

# Long-Term Vision

LeadForgeAI should replace multiple lead generation tools with one modular platform.

Future modules include:

Business Discovery

People Discovery

Website Intelligence

AI Intelligence

Campaign Manager

Workflow Automation

Reporting

Plugin Marketplace

CRM

Cloud Sync

---

# Architecture Overview

Desktop (Tauri + React)

↓

FastAPI Backend

↓

Service Layer

↓

Repository Layer

↓

PostgreSQL

External services such as AI providers and Workflow Engines communicate only with the Backend.

No component communicates directly with the database except the Repository Layer.

---

# Core Technologies

Desktop

Tauri

Frontend

React

TypeScript

Vite

Backend

FastAPI

Python

Database

PostgreSQL

ORM

SQLAlchemy 2.x

Migration

Alembic

Workflow Engine

n8n (replaceable)

Browser Automation

Playwright

Containers

Docker Compose

Cache

Redis (future)

---

# Core Architecture Principles

Backend owns business logic.

Frontend owns presentation.

Database owns persistence.

Workflow Engine executes automation.

AI generates suggestions only.

Everything communicates through APIs.

Modules never communicate directly.

---

# Module Structure

Dashboard

Workspace

Business

People

Website

Campaign

Workflow

AI

Export

Settings

System

Each module has:

API

↓

Service

↓

Repository

↓

Database

---

# Development Rules

Architecture before implementation.

Documentation before code.

Tasks before implementation.

Small commits.

No direct database access from frontend.

No direct communication between modules.

No business logic inside API routes.

---

# Folder Structure

docs/

Architecture and documentation.

tasks/

Engineering tasks.

prompts/

Implementation prompts.

backend/

FastAPI application.

frontend/

React application.

docker/

Container configuration.

scripts/

Utility scripts.

specs/

Feature specifications.

contracts/

API contracts.

logs/

Development history.

---

# Current Development Phase

Sprint 1

Current Goal

Bootstrap the application.

Current Tasks

TASK-001

Project Bootstrap

TASK-002

Database Bootstrap

TASK-003

Workspace Foundation

TASK-004

System Health

TASK-005

Desktop Bootstrap

Future Tasks

Power Button

Workflow Engine

Business Discovery

Website Intelligence

People Discovery

AI

Campaigns

Plugins

---

# Coding Standards

Python

PEP8

Type Hints

Async First

TypeScript

Strict Mode

Reusable Components

Small Functions

Readable Code

No duplicate logic.

---

# Database Principles

UUID Primary Keys

Soft Delete

UTC Timestamps

Normalized Tables

Repository Pattern

No duplicated information.

---

# API Principles

REST

Versioned

JSON

Standard Responses

Validation Required

Documented Endpoints

---

# AI Principles

AI never modifies the database.

AI never changes architecture.

AI never bypasses validation.

AI responses are always validated.

---

# Workflow Principles

Workflow Engines execute automation.

Business logic belongs inside Backend.

Workflow Engines are replaceable.

---

# Security Principles

Local First

Secrets in Environment Variables

No hardcoded credentials.

Public information only.

No private account access.

---

# Git Rules

Small commits.

Meaningful commit messages.

Documentation updated with architecture changes.

Never commit secrets.

---

# Before Implementing Any Task

Read:

1. CONTEXT.md

2. tasks/TASK-XXX.md

3. prompts/.../TASK-XXX_IMPLEMENTATION_PROMPT.md

If additional architectural details are required, refer to the Project Bible and Architecture documents.

Do not modify the architecture without explicit approval.

---

# Success Criteria

Every Sprint must produce a runnable application.

Every Task must satisfy its acceptance criteria.

Every implementation must follow the documented architecture.

Maintainability is more important than speed.

Architecture is more important than shortcuts.

End of Context