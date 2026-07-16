# LeadForgeAI

Read

MASTER_IMPLEMENTATION_PROMPT.md

CONTEXT.md

TASK-017.md

Implement TASK-017 only.

---

Objective

Build the production-ready Google Maps Provider Framework.

This is NOT scraping.

This is the provider infrastructure.

---

Implement

GoogleMapsProvider

Provider Adapter

Configuration

Lifecycle

Rate Limiter

Retry Manager

Health System

Provider Logger

Normalizer

Developer Diagnostics

Provider Status UI

---

Rules

Do NOT implement Playwright.

Do NOT implement Puppeteer.

Do NOT implement Apify.

Do NOT scrape Google Maps.

Do NOT parse HTML.

Everything must be interface-driven.

The Search Engine must never know how data is collected.

---

Architecture

UI

↓

Search Engine

↓

Execution Engine

↓

GoogleMapsProvider

↓

Provider Adapter

↓

Future Scraper

---

Developer Mode

Display

Provider Status

Provider Health

Current Adapter

Retry Count

Rate Limit

Current Delay

---

Code Quality

SOLID

Dependency Injection

Production Ready

No duplicated logic

No TODO comments

No placeholder architecture

---

UI Requirements

Inter

Helvetica Neue

Never Arial

Apple Human Interface

Linear

Raycast

Professional

Minimal

---

Output

Generate

TASK_COMPLETION_REPORT.md

GIT_DIFF_SUMMARY.md

Architecture Diagram

Created Files

Modified Files

Verification Steps

Performance Notes

Wait for review.