# TASK-018

Title

Real Scraper Adapter (Playwright)

---

Status

Ready

---

Priority

Critical

---

Sprint

Sprint 4

---

Estimated Time

24–36 Hours

---

Objective

Implement the first real scraping adapter using Playwright.

This is the first component that will collect real Google Maps business data.

The adapter must plug into the existing Provider Framework and Search Execution Engine without modifying their architecture.

---

Goal

Create a production-ready Playwright Adapter.

Implement browser lifecycle.

Implement Google Maps navigation.

Implement search execution.

Implement business card extraction.

Implement pagination (scroll loading).

Implement basic error handling.

Return normalized business objects.

---

Scope

The adapter must support:

Launch Browser

Create Context

Open Google Maps

Search Query

Wait for Results

Scroll Results Panel

Extract Business Cards

Normalize Results

Return Results

Close Browser

---

Extract Fields

Business Name

Category

Rating

Review Count

Address

Phone (if visible)

Website (if visible)

Google Maps URL

Status

Latitude (if available)

Longitude (if available)

---

Rules

Use Playwright.

No Apify.

No Puppeteer.

No Selenium.

No external scraping services.

The adapter must use the existing Provider Interface.

The Search Engine must remain unchanged.

---

Limits

Initial maximum:

100 businesses per search.

Pagination architecture must support larger limits later.

---

Error Handling

Timeout

Google Layout Changed

Blocked

Captcha Detected

No Results

Unexpected Exception

---

Backend

Implement

PlaywrightAdapter

BrowserManager

MapsNavigator

BusinessExtractor

ScrollManager

ExtractionValidator

GoogleMapsParser

---

Frontend

Replace Demo Data when real provider is enabled.

Display

Real Provider

Demo Provider

Provider Status

Search Duration

Businesses Found

---

Developer Mode

Display

Browser Status

Current Page

Current Query

Extraction Count

---

Acceptance Criteria

Real Google Maps search works.

Business list returned.

Integrated with Search Engine.

Integrated with Execution Engine.

No architecture changes required.

---

Definition of Done

Real Playwright Adapter Complete.

Google Maps Search Functional.

Committed.

---

Next Task

TASK-019

Business Data Enrichment