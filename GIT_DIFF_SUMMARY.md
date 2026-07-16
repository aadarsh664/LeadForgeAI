# Git Diff Summary (TASK-018)

## Untracked Files Added
```text
backend/app/services/search/providers/google_maps/playwright_adapter.py
task_18_backend.py
task_18_frontend.py
```

## Modified Files
```text
backend/Dockerfile
backend/app/core/dependencies.py
backend/app/api/v1/endpoints/search.py
backend/app/services/job/worker.py
backend/requirements.txt
frontend/src/pages/BusinessPage.tsx
```

## Summary of Changes
- **Playwright Integration**: Added the `playwright` package to Python requirements and updated the container configuration to install necessary Chromium dependencies.
- **Scraper Implementation**: Authored `playwright_adapter.py`, implementing a robust Chromium-based scraping pipeline that loads Google Maps, types queries, scrolls lazy-loaded feeds, and extracts structured data.
- **Provider Switching UI**: Enhanced the `BusinessPage.tsx` search form to expose a Provider Selection dropdown, giving users explicit control over whether they want real Google Maps data or local Mock demo data.
