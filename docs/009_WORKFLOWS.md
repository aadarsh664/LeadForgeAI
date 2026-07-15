# LeadForgeAI — Workflow Architecture

Version: 1.0.0

Status: Draft

---

# Purpose

This document defines how workflows operate inside LeadForgeAI.

Workflows represent business processes.

Business logic belongs to the Backend.

Workflow engines execute tasks.

---

# Workflow Philosophy

A workflow is a sequence of actions.

Every workflow has:

Input

↓

Validation

↓

Execution

↓

Result

↓

Logging

↓

Completion

---

# Workflow Engine

LeadForgeAI does not depend on a specific workflow engine.

The application communicates only with the internal Workflow Service.

Supported engines may include:

n8n

Windmill

Kestra

Temporal

Future engines

The workflow engine is replaceable.

---

# Workflow Lifecycle

Created

↓

Queued

↓

Running

↓

Paused

↓

Completed

↓

Failed

↓

Archived

---

# Business Discovery Workflow

Input

Business Category

Location

↓

Backend Validation

↓

Workflow Execution

↓

Business Discovery

↓

Deduplication

↓

Save Database

↓

Return Results

---

# Website Intelligence Workflow

Website URL

↓

Validation

↓

Crawler

↓

Email Discovery

↓

Phone Discovery

↓

Social Discovery

↓

Technology Detection

↓

Store Results

---

# AI Analysis Workflow

Business

↓

Website

↓

Context Builder

↓

AI Provider

↓

Response Validation

↓

Store AI Analysis

↓

Return Results

---

# Campaign Workflow

Create Campaign

↓

Select Leads

↓

AI Personalization

↓

Review

↓

Send

↓

Track

↓

Update Statistics

---

# Health Workflow

Application Starts

↓

Check Docker

↓

Check Backend

↓

Check Database

↓

Check Workflow Engine

↓

Load Workspace

↓

Ready

---

# Error Workflow

Detect Error

↓

Log Error

↓

Notify User

↓

Attempt Recovery

↓

Continue if Possible

---

# Workflow Principles

Every workflow must be:

Repeatable

Observable

Recoverable

Logged

Versioned

---

END OF DOCUMENT