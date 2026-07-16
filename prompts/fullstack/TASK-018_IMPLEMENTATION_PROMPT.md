# LeadForgeAI

Read

MASTER_IMPLEMENTATION_PROMPT.md

CONTEXT.md

TASK-018.md

Implement TASK-018 only.

---

Objective

Build the first production-ready Playwright Adapter.

This adapter must integrate with the existing Search Engine and Search Execution Engine.

Do not modify the architecture.

---

Implement

PlaywrightAdapter

BrowserManager

MapsNavigator

BusinessExtractor

ScrollManager

GoogleMapsParser

ExtractionValidator

Provider Registration

Provider Health Integration

---

Rules

Use Playwright.

No Apify.

No Puppeteer.

No Selenium.

No external APIs.

Do not hardcode business logic into the Search Engine.

Return only NormalizedBusiness objects.

---

Performance

Keep browser reuse in mind.

Minimize unnecessary page reloads.

Support future parallel execution.

---

UI

Reuse existing Progress UI.

Replace Demo Data with real data only when provider succeeds.

---

Code Quality

Production Ready.

SOLID.

Dependency Injection.

No duplicated logic.

No TODO comments.

---

Output

Generate

TASK_COMPLETION_REPORT.md

GIT_DIFF_SUMMARY.md

Performance Report

Created Files

Modified Files

Verification Steps

Known Limitations

Wait for review.