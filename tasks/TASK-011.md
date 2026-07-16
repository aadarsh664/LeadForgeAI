# TASK-011

Title

Business Search UI

---

Status

Ready

---

Priority

Critical

---

Sprint

Sprint 3

---

Estimated Time

8-10 Hours

---

Objective

Build the first real Business Search interface.

This is the beginning of Lead Discovery.

The user should feel that LeadForgeAI is now becoming a usable application.

---

Problem

Currently the Dashboard contains placeholder Quick Actions.

There is no actual search experience.

---

Goal

Create a premium Business Search page.

Do not implement scraping.

Do not implement backend search logic.

Implement only the production-ready UI and interaction flow.

---

Sections

Search Header

Search Form

Recent Searches

Saved Search Templates

Search Filters

Search Preview

Search Tips

---

Search Form

Business Category

Location

Radius

Language

Maximum Results

Country

State

City

Keywords

Exclude Keywords

---

Advanced Filters

Has Website

Has Email

Has Phone

Minimum Rating

Minimum Reviews

Open Now

Verified Business

Hide Permanently Closed

---

Search Header

Title

Subtitle

Search Button

Reset Button

---

Search Preview

Display a live summary.

Example

Dentists

↓

Patna

↓

India

↓

Maximum 500 Results

No backend request.

Only frontend preview.

---

Saved Templates

Placeholder.

Display

Local Businesses

Restaurants

Hospitals

Schools

Gyms

Real Estate

Lawyers

Hotels

Clinics

---

Recent Searches

Initially

"No searches yet"

Do not invent searches.

---

Search Tips

Show 5 professional search recommendations.

---

Validation

Disable Search Button until

Category

and

Location

are filled.

---

Backend

No backend changes.

---

Frontend

Create

BusinessSearchPage

SearchForm

SearchFilters

SearchPreview

TemplateCards

RecentSearchList

SearchTips

---

Persistence

Remember the user's last search form locally.

Restore it after restart.

---

Animation

Fade

Hover

150–250ms

---

Acceptance Criteria

Professional Search UI

Responsive Layout

Form Validation

Search Preview

State Persistence

Design System Used

No fake business data

---

Definition of Done

Business Search UI Complete.

Desktop Integrated.

Committed.

---

Next Task

TASK-012

Business Search Engine Architecture

---

End of Task