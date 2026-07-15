# LeadForgeAI — AI Rules

Version: 1.0.0

Status: Draft

---

# Purpose

This document defines how Artificial Intelligence is used inside LeadForgeAI.

Every AI provider, model and future implementation must follow these rules.

These rules are permanent unless explicitly updated.

---

# AI Philosophy

AI is an assistant.

AI is not the decision maker.

The user always owns the final decision.

---

# AI Responsibilities

AI may:

Analyze businesses

Summarize websites

Generate outreach messages

Generate reports

Score leads

Generate recommendations

Explain errors

Answer user questions

Generate structured output

---

# AI Must Never

Modify the database directly.

Delete records.

Execute workflows.

Call APIs without backend approval.

Modify application settings.

Bypass validations.

Access private user data without permission.

Make irreversible changes.

---

# Backend Responsibility

The backend prepares all AI input.

The backend validates every AI response.

The backend stores AI output.

The AI never communicates directly with:

Database

Desktop Application

n8n

Docker

Redis

---

# Prompt Management

Every AI prompt must be version controlled.

Prompts belong inside the prompts directory.

No prompt should exist only inside source code.

---

# AI Providers

Version 1 supports provider abstraction.

Supported providers include:

OpenAI

Google Gemini

OpenRouter

Future Local Models

Future providers may be added without changing application architecture.

---

# Provider Independence

The application should never depend on a single AI provider.

Changing providers must require minimal code changes.

---

# Context Rules

AI should receive only the minimum required context.

Never send unnecessary information.

Never send unrelated records.

Smaller context improves performance and reduces cost.

---

# Structured Output

Whenever practical,

AI responses must use structured JSON.

Avoid free-form text when machine-readable output is required.

---

# AI Analysis

AI generated analysis must remain separate from raw business data.

Raw Data

↓

AI Processing

↓

AI Analysis Table

The original data must never be overwritten.

---

# AI Memory

AI should never permanently remember user information.

Persistent memory belongs to the application database.

---

# AI Errors

If AI fails,

The application must continue functioning.

Users should receive a meaningful error message.

Automatic retries may be attempted.

---

# AI Cost Awareness

Future versions should support:

Estimated Token Usage

Estimated Cost

Provider Comparison

Model Selection

Users should understand the cost before running expensive operations.

---

# Local AI

Future versions may support local AI models.

The architecture must allow switching between:

Cloud AI

↓

Local AI

Without major code changes.

---

# Prompt Versioning

Every prompt must include:

Version

Author

Purpose

Input Format

Expected Output

Supported Model

---

# AI Safety

AI should only process publicly available information.

AI must never attempt to infer private information.

AI should avoid generating misleading factual claims.

---

# Engineering Principle

AI is a tool.

Architecture owns AI.

AI never owns architecture.

---

END OF DOCUMENT