# LeadForgeAI — Project Bible

Version: 2.0.0

Status: Active

Owner: LeadForgeAI Architecture

Priority: Highest

---

# Purpose

The Project Bible is the supreme document of LeadForgeAI.

Every document, task, module, API, workflow, database schema, user interface, AI integration and future feature must follow this document.

If two documents conflict,

The Project Bible always wins.

---

# What is LeadForgeAI?

LeadForgeAI is a Local-First Lead Intelligence Platform.

It is not:

• A Google Maps scraper

• A cold email sender

• An email finder

• A CRM

• An automation software

It is a platform capable of combining all of those capabilities through modular architecture.

---

# Long-Term Mission

Build the most powerful self-hosted Lead Intelligence Platform that allows anyone to discover, enrich, analyze and organize business intelligence without requiring programming knowledge.

---

# Long-Term Vision

The application should evolve into a complete ecosystem.

The user should never need to combine ten different tools.

Everything should exist inside one platform.

---

# Core Philosophy

LeadForgeAI solves problems.

It does not collect features.

Every feature must solve a real business problem.

No feature exists simply because competitors have it.

---

# Golden Rules

Rule 1

Architecture always comes before implementation.

---

Rule 2

Documentation always comes before coding.

---

Rule 3

Every module owns one responsibility.

---

Rule 4

Everything communicates through APIs.

---

Rule 5

No direct communication between modules.

---

Rule 6

The Backend owns business logic.

---

Rule 7

The Frontend owns presentation.

---

Rule 8

The Database owns persistence.

---

Rule 9

The Workflow Engine owns execution.

---

Rule 10

AI assists.

AI never owns business logic.

---

# Engineering Philosophy

Every engineering decision must satisfy at least one of the following:

Increase maintainability

Increase scalability

Reduce complexity

Improve reliability

Improve developer experience

Improve user experience

If none of these are true,

the decision should be rejected.

---

# Product Philosophy

Simple

Professional

Modular

Scalable

Reliable

Transparent

Predictable

Future Ready

---

# Software Philosophy

The application must continue working even when one module fails.

Graceful degradation is mandatory.

No single module should crash the entire platform.

---

# User Philosophy

The user should never need to understand:

Docker

FastAPI

Redis

PostgreSQL

n8n

Playwright

Internal APIs

The software hides technical complexity.

---

# Local First Philosophy

Everything should run locally whenever practical.

Internet access should only be required for:

AI Providers

Website Discovery

Business Discovery

Future Cloud Sync

Everything else should remain functional locally.

---

# Modular Philosophy

Every feature belongs to a module.

Every module owns its own responsibility.

Every module should be replaceable.

Every module should be independently testable.

---

# Development Philosophy

The project grows through small iterations.

Large rewrites are considered architectural failures.

Every sprint must produce a working application.

---

# Repository Philosophy

GitHub is the permanent memory.

Chat conversations are temporary.

Every architectural decision must exist inside GitHub.

Never depend on conversation history.

---

# Documentation Philosophy

Documentation explains WHY.

Code explains HOW.

Comments explain WHY NOT.

Never duplicate documentation inside code.

---

# Version Philosophy

Everything is versioned.

Documents

APIs

Database

Prompts

Tasks

Releases

Architecture

Nothing evolves without version tracking.

---

# Naming Philosophy

Names should describe purpose.

Avoid abbreviations unless universally understood.

Good

BusinessDiscoveryService

Bad

BDS

Good

CampaignManager

Bad

Manager2

Code should read like English.

---

# Simplicity Principle

Simple solutions are preferred.

Complexity requires justification.

Every unnecessary abstraction increases maintenance cost.

---

# Stability Principle

Breaking changes are expensive.

Backward compatibility should be preserved whenever practical.

---

# Reusability Principle

Never duplicate business logic.

Write once.

Reuse everywhere.

---

# Security Principle

Security is part of architecture.

Never add security later.

---

# Performance Principle

Correctness

↓

Maintainability

↓

Performance

Performance optimization happens only after measurement.

---

# AI Principle

AI is treated as a Junior Software Engineer.

AI never approves its own work.

Human review is mandatory.

---

# Project Success

LeadForgeAI succeeds when:

A beginner user can

Install

↓

Open

↓

Press Power

↓

Wait

↓

Generate Leads

Without opening a terminal.

That is the primary success metric.

---

END OF PART 1

---

# Engineering Constitution

The following rules are mandatory.

Every developer, AI assistant, automation system and future contributor must follow these rules.

These rules are permanent.

---

# Backend Constitution

The Backend owns:

Business Logic

Validation

Permissions

Database Access

Workflow Coordination

AI Coordination

Logging

Error Handling

The Backend never renders user interface.

The Backend never contains frontend logic.

---

# Frontend Constitution

The Frontend owns:

Presentation

User Interaction

Forms

Charts

Tables

Notifications

Progress Indicators

Theme

The Frontend never contains business logic.

The Frontend never accesses the database directly.

The Frontend communicates only through Backend APIs.

---

# Database Constitution

The Database stores information.

It never contains business rules.

It never contains presentation logic.

Every database modification must pass through the Backend.

No external system may write directly into the database.

---

# API Constitution

Every feature must expose a documented API.

Every API must be versioned.

Every API must return consistent responses.

Every API must validate input.

Every API must validate output.

Undocumented APIs are prohibited.

---

# Workflow Constitution

Workflows automate tasks.

Workflows never own business rules.

Business rules always belong inside Backend Services.

Changing workflow engines must never require changing business logic.

---

# AI Constitution

AI generates suggestions.

AI generates summaries.

AI generates recommendations.

AI generates structured output.

AI never changes the application state directly.

Every AI response must be validated before storage.

---

# Service Constitution

Every service owns one responsibility.

Every service exposes one public interface.

Services never access another service's private implementation.

Services communicate through contracts.

---

# Module Constitution

Every module must be:

Independent

Replaceable

Documented

Versioned

Testable

Recoverable

Observable

---

# Repository Constitution

Repositories only communicate with databases.

Repositories never contain business logic.

Repositories never communicate with APIs.

Repositories never call AI.

Repositories never call workflows.

---

# Validation Constitution

All user input must be validated.

All API input must be validated.

All AI output must be validated.

All workflow output must be validated.

Never trust external input.

---

# Logging Constitution

Every important action must create a log entry.

Logs must include:

Timestamp

Module

Event

Severity

Reference ID

Logs should explain what happened.

Logs should never expose secrets.

---

# Error Constitution

Errors are expected.

Applications must recover whenever possible.

Every error must include:

Meaningful Message

Error Code

Recovery Suggestion

Internal Log Reference

Never expose stack traces to users.

---

# Configuration Constitution

Configuration belongs inside configuration files.

Never hardcode configuration values.

Future configuration changes should not require recompiling the application.

---

# Environment Constitution

Development

Testing

Production

Future environments must remain isolated.

Environment variables must never be committed to Git.

---

# Dependency Constitution

Every dependency must satisfy:

Actively Maintained

Open Source (preferred)

Reliable

Documented

Production Ready

Unused dependencies must be removed.

---

# Performance Constitution

Performance improvements require measurement.

Never optimize blindly.

Correctness is always more important than speed.

---

# Security Constitution

Security belongs inside architecture.

Never implement security as an afterthought.

Every external communication must be validated.

Every secret must remain protected.

---

# Backup Constitution

Every important user asset should be recoverable.

The application should support:

Workspace Backup

Workspace Restore

Export

Import

Future automatic backups.

---

# Plugin Constitution

Plugins extend functionality.

Plugins never modify the Core.

Plugins communicate only through approved APIs.

Removing a plugin must never break the application.

---

# Workspace Constitution

Every workspace is isolated.

No workspace may access another workspace's data.

Deleting one workspace must never affect another.

---

# File Constitution

Large binary files belong in storage.

Only metadata belongs in the database.

The application must never store unnecessary binary data inside PostgreSQL.

---

# Development Constitution

No feature starts with code.

Every feature starts with:

Specification

↓

Task

↓

Implementation

↓

Testing

↓

Review

↓

Merge

---

# Documentation Constitution

Every architectural change updates documentation.

Every database change updates documentation.

Every API change updates documentation.

Every release updates documentation.

Documentation is part of the product.

---

# Future Constitution

LeadForgeAI should continue evolving without breaking its core architecture.

Future growth should happen through:

Modules

Plugins

New APIs

New Providers

New Integrations

The Core should remain stable.

---

END OF PART 2

---

# Governance

LeadForgeAI is developed using engineering governance.

Every contribution follows the same lifecycle.

Idea

↓

Specification

↓

Task

↓

Implementation

↓

Testing

↓

Review

↓

Merge

↓

Release

No contribution may bypass this process.

---

# Task Constitution

Every implementation begins with a Task document.

A Task must contain:

Task ID

Title

Objective

Context

Dependencies

Files

Acceptance Criteria

Definition of Done

Estimated Complexity

Implementation Notes

Review Checklist

No implementation begins without an approved Task.

---

# Git Constitution

Git history is permanent.

Every commit should represent one logical change.

Good commits are small.

Good commits are descriptive.

Examples

docs: add database architecture

feat: implement business discovery service

fix: resolve workspace loading bug

Avoid generic messages.

Example

update

changes

fixed

stuff

---

# Branch Strategy

Main

Production Ready

Develop

Integration Branch

Feature Branches

One feature

↓

One branch

↓

One Pull Request

Future contributors should never develop directly on main.

---

# Code Review Constitution

Every change requires review.

The reviewer verifies:

Architecture

Code Style

Naming

Performance

Security

Tests

Documentation

No code merges without review.

---

# Testing Constitution

Every feature should include testing.

Testing Levels

Unit

Integration

End-to-End

Regression (Future)

Manual testing alone is insufficient.

---

# Documentation Constitution

Documentation is part of development.

Documentation is never optional.

When implementation changes,

documentation changes.

When architecture changes,

documentation changes.

Documentation always remains synchronized.

---

# Release Constitution

A release is allowed only when:

Documentation Updated

Architecture Respected

Tests Passed

No Critical Errors

Version Updated

Changelog Updated

---

# AI Collaboration Constitution

Artificial Intelligence is treated as an engineering assistant.

AI may:

Generate

Refactor

Explain

Review

Suggest

AI may not:

Approve

Merge

Define Architecture

Modify Standards

Change Database Rules

AI suggestions require human approval.

---

# Engineering Quality

Every implementation should be:

Readable

Maintainable

Testable

Observable

Replaceable

Predictable

---

# Technical Debt

Technical debt should be recorded.

Never hide technical debt.

Every shortcut must be documented.

Future improvements belong inside roadmap items.

---

# Backward Compatibility

Avoid breaking existing behavior.

When breaking changes become necessary:

Document them.

Version them.

Provide migration guidance whenever practical.

---

# Open Source Philosophy

LeadForgeAI should remain understandable.

Future contributors should understand the project by reading documentation.

The architecture should encourage learning.

Complexity should never exist without purpose.

---

# Future SaaS Constitution

Future cloud versions must reuse the same architecture.

The Desktop edition remains the reference implementation.

Cloud functionality should extend the architecture,

never replace it.

---

# Plugin Constitution

Plugins extend the platform.

Plugins never modify the Core.

Plugins communicate through documented interfaces.

Removing a plugin must never damage existing functionality.

---

# Decision Constitution

Architectural decisions are permanent unless formally replaced.

Every replacement decision must explain:

Why

Benefits

Risks

Migration Strategy

---

# Principle of Stability

Stable architecture is more valuable than rapid feature growth.

The project should evolve through small, controlled improvements.

---

# Principle of Simplicity

When two solutions solve the same problem,

prefer the simpler one.

Complexity requires measurable justification.

---

# Principle of Ownership

Every module has one owner.

Every service has one responsibility.

Every document has one purpose.

Every task has one goal.

Ownership reduces confusion.

---

# Principle of Transparency

Users should understand:

What happened.

Why it happened.

What the application is doing.

The application should never behave mysteriously.

---

# Final Constitution

If uncertainty exists,

follow this order of authority.

1. Project Bible

2. Architecture

3. Database

4. API

5. Task

6. Source Code

Chat conversations never override GitHub documentation.

GitHub is the permanent memory of LeadForgeAI.

---

# LeadForgeAI Engineering Oath

We choose maintainability over shortcuts.

We choose architecture over chaos.

We choose documentation over assumptions.

We choose quality over speed.

We choose simplicity over unnecessary complexity.

We build software that survives years,
not demonstrations that survive one day.

Every line of code should make the project stronger.

Every decision should respect the architecture.

Every release should increase trust.

This is the engineering standard of LeadForgeAI.

---

END OF PROJECT BIBLE