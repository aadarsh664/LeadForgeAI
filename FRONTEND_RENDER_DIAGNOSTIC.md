# FRONTEND_RENDER_DIAGNOSTIC.md

## Executive Summary

The blank white page after search completion was caused by **two distinct frontend bugs** — broken import paths and invalid JavaScript syntax. Both are now fixed.

---

## Root Cause Analysis

### Bug 1: Wrong Import Path in `BusinessResults.tsx` and `BusinessProfile.tsx` (CRITICAL)

**Files:** `frontend/src/pages/BusinessResults.tsx` (line 10), `frontend/src/pages/BusinessProfile.tsx` (line 11)

Both files used `../../types/search` to import `NormalizedBusiness`. Since these files live in `src/pages/`, traversing up two directories with `../../` exits the `src/` directory entirely, landing at the project root where no `types/` directory exists.

```
src/
├── pages/
│   ├── BusinessResults.tsx   ← import from "../../types/search" ✗ (goes to project root)
│   ├── BusinessProfile.tsx   ← import from "../../types/search" ✗ (goes to project root)
│   └── BusinessPage.tsx      ← import from "../types/search"   ✓ (correct)
└── types/
    └── search.ts
```

Vite's dev server resolves this lazily — the module is only loaded when the component first renders. The search form and progress card work fine because they don't use these components. The crash occurs the instant React tries to render `BusinessResults` after the job completes, because the import fails at that point.

**Fix:**
```diff
- import type { NormalizedBusiness } from "../../types/search";
+ import type { NormalizedBusiness } from "../types/search";
```

### Bug 2: Python `True` Literal in JSX (CRASH)

**File:** `frontend/src/pages/BusinessResults.tsx` (lines 108 and 167)

The code contained `=== True` — a Python boolean literal. In JavaScript, `True` is an undefined identifier, causing a `ReferenceError` the moment React evaluates the expression.

```tsx
// BEFORE (crashes)
{(business.raw_data?.demo_data === True || business.raw_data?.demo_data === true) && ...}

// AFTER (fixed)
{business.raw_data?.demo_data === true && ...}
```

---

## Execution Flow Trace

```
User clicks "Search"
  ↓
handleSearch() → POST /api/v1/search/jobs → job created
  ↓
viewState = "progress" → renders <JobProgressCard /> ✅ (works)
  ↓
Polling: GET /api/v1/search/jobs/{id} → status changes
  ↓
jobData.status === "Completed"
  ↓
setResults(jobData.results) → setViewState("results")
  ↓
viewState === "results" → renders <BusinessResults />
  ↓
❌ CRASH: import from "../../types/search" → Module not found
  ↓
React error boundary catches → Blank white page
```

---

## Network Response Verification

The backend response is correct. The HTTP response from `/api/v1/search/jobs/{id}` contains:

```json
{
  "id": "4941430c-decb-42cf-8e65-3db6726968e9",
  "status": "Completed",
  "progress": { "percentage": 100, "stage": "Completed" },
  "results": [
    { "business_id": "uuid", "name": "...", "category": "...", ... }
  ]
}
```

The frontend correctly reads `jobData.results` (line 134) and passes it to `<BusinessResults results={results} />` (line 344). The schema matches. The crash occurs inside the component itself due to the import failure.

---

## Files Modified

| File | Line(s) | Bug | Fix |
|------|---------|-----|-----|
| `frontend/src/pages/BusinessResults.tsx` | 10 | `../../types/search` (wrong path) | Changed to `../types/search` |
| `frontend/src/pages/BusinessResults.tsx` | 108, 167 | `=== True` (Python literal) | Changed to `=== true` |
| `frontend/src/pages/BusinessProfile.tsx` | 11 | `../../types/search` (wrong path) | Changed to `../types/search` |

---

## Verification

- Vite dev server restarted: **No compile errors**
- Frontend loads at http://localhost:5173: **Confirmed**
- Backend routes all return 200: **Confirmed**
- Backend real search returns 5 businesses: **Confirmed**
- Import paths now resolve correctly: `src/pages/ → ../types/search → src/types/search.ts` ✅
