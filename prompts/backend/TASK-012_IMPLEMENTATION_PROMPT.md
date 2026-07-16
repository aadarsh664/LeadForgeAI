# LeadForgeAI

## AI Implementation Prompt

Read:

1. prompts/MASTER_IMPLEMENTATION_PROMPT.md

2. CONTEXT.md

3. tasks/TASK-012.md

Implement TASK-012 only.

---

Objective

Create a provider-based Search Engine Architecture.

Do NOT implement scraping.

Do NOT implement Google Maps.

Do NOT implement external APIs.

Only architecture.

---

Backend

Implement

Search Engine

Provider Interface

Provider Registry

Search Validator

Search Models

Search Exceptions

Search Normalizer

Search Pipeline

---

Rules

Search Engine orchestrates everything.

Providers never know about UI.

Providers never know about Database.

Providers only return raw provider data.

Normalizer converts raw data into LeadForgeAI format.

---

Future Providers

Google Maps

OpenStreetMap

Yelp

Yellow Pages

Custom Providers

---

No Placeholder Code

Do not leave TODO.

Implement production-ready architecture.

---

Business Rules

Never hardcode provider names inside the engine.

Use dependency injection where appropriate.

Provider registration must be extensible.

---

Output

Generate

TASK_COMPLETION_REPORT.md

GIT_DIFF_SUMMARY.md

Created Files

Modified Files

Architecture Diagram

Verification Steps

Stop after implementation.

Wait for review.