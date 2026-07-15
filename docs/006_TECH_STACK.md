# LeadForgeAI — Technology Stack

Version: 1.0.0

Status: Approved

---

# Purpose

This document defines the official technology stack used throughout LeadForgeAI.

No technology should be replaced without updating this document.

---

# Design Principles

The technology stack must satisfy the following goals:

• Free and Open Source whenever possible

• Cross Platform

• Local First

• Beginner Friendly

• High Performance

• Long Term Support

• Large Community

• Easy to Maintain

---

# Desktop Application

Framework

Tauri

Reason

Lightweight

Native Performance

Small Installer

Lower RAM Usage

Better than Electron for this project.

---

# Frontend

Framework

React

Language

TypeScript

Reason

Large ecosystem

Component based

Excellent developer experience

Long-term maintainability

---

# Styling

Tailwind CSS

Reason

Fast UI development

Reusable components

Easy theme support

---

# Backend

Framework

FastAPI

Language

Python

Reason

High Performance

Excellent documentation

Async support

Easy AI integration

---

# Automation

n8n

Deployment

Docker

Reason

Visual workflow builder

API support

Huge integration ecosystem

---

# Database

PostgreSQL

Reason

Reliable

Scalable

Powerful filtering

Production ready

---

# Cache

Redis

Reason

Fast temporary storage

Queue support

Future background jobs

---

# Browser Automation

Playwright

Reason

Reliable

Modern

Cross-browser

Better than Selenium

---

# AI Layer

Provider Agnostic

Supported Providers

OpenAI

Google Gemini

OpenRouter

Local Models (Future)

The backend should support multiple providers through a unified interface.

---

# API Style

REST API

JSON

Future Support

WebSockets

---

# Package Managers

Frontend

npm

Backend

pip

Future

uv may be evaluated later.

---

# Version Control

Git

GitHub

Main Branch

main

Development Branch

develop (Future)

---

# Code Editor

Visual Studio Code

Recommended Extensions

Python

ESLint

Prettier

Tailwind CSS

Markdown All in One

Docker

GitHub Pull Requests

---

# Containerization

Docker Desktop

Docker Compose

Every required service should run inside containers whenever practical.

---

# Logging

Structured Logging

Human-readable

Future support for centralized logging.

---

# Testing

Backend

pytest

Frontend

Vitest

End-to-End

Playwright

---

# Documentation

Markdown

GitHub

Architecture First

Documentation Before Code

---

# Coding Standards

Python

PEP8

Type Hints Required

Async First

---

TypeScript

Strict Mode Enabled

Reusable Components

Avoid Large Files

---

# Future Technologies

Qdrant

MinIO

RabbitMQ

Elasticsearch

These are optional and should only be introduced when genuinely required.

---

END OF DOCUMENT