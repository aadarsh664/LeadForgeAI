# PLAYWRIGHT_DIAGNOSTIC_REPORT.md

## Executive Summary

The Playwright Adapter is now **fully operational**. Real business data is being extracted from Google Maps through the complete pipeline. All 7 steps have been verified.

---

## Root Cause Analysis

There were **3 distinct root causes** preventing the adapter from functioning:

### Root Cause 1: Diagnostics Endpoint Created a Phantom Provider (CRITICAL)

**File:** `backend/app/api/v1/endpoints/diagnostics.py`

The diagnostics endpoint was creating its own standalone `GoogleMapsProvider()` instance **without** passing an adapter:

```python
# BEFORE (broken)
temp_provider = GoogleMapsProvider()  # ← No adapter! Always reports "No active adapter"

@router.get("/diagnostics")
async def get_provider_diagnostics():
    return temp_provider.metadata()
```

This phantom instance had `adapter=None`, so the Developer Mode page always displayed *"No active adapter"* — even though the **real** provider in the registry had the adapter correctly injected.

**Fix:** Changed the endpoint to query the actual registered provider from the SearchEngine registry:

```python
# AFTER (fixed)
@router.get("/diagnostics")
async def get_provider_diagnostics(engine: SearchEngine = Depends(get_search_engine)):
    provider = engine.registry.get_provider("google_maps")
    meta = provider.metadata()
    meta["adapter"] = "Connected" if getattr(provider, "adapter", None) else "No active adapter"
    return meta
```

### Root Cause 2: Google Maps Navigation Failure — Search Box Selector Mismatch

**File:** `backend/app/services/search/providers/google_maps/playwright_adapter.py`

The original adapter navigated to `https://www.google.com/maps` and then tried to find the search box via `input#searchboxinput`. Inside a headless Docker container, Google Maps sometimes serves a different page structure or a consent screen first, causing this selector to time out after 10 seconds.

**Fix:** Changed navigation to use a **direct search URL** that bypasses the search box entirely:

```python
# BEFORE (broken)
await page.goto("https://www.google.com/maps")
search_box = page.locator("input#searchboxinput")
await search_box.wait_for(state="visible", timeout=10000)  # ← TIMEOUT!

# AFTER (fixed)
encoded_query = urllib.parse.quote_plus(query)
await page.goto(f"https://www.google.com/maps/search/{encoded_query}")
```

Also added consent button handling and a screenshot-on-failure diagnostic.

### Root Cause 3: `nonlocal` Variable Bug in Provider

**File:** `backend/app/services/search/providers/google_maps/provider.py`

The `fetch_next()` closure inside `search()` tried to increment `count` — a variable in the outer scope — without declaring `nonlocal count`. This caused `UnboundLocalError` on every search, which triggered the retry manager 3 times before failing.

```python
# BEFORE (broken)
async def fetch_next():
    batch = []
    async for item in self.adapter.execute_search(request):
        count += 1  # ← UnboundLocalError!

# AFTER (fixed)
async def fetch_next():
    nonlocal count
    batch = []
    async for item in self.adapter.execute_search(request):
        count += 1
```

---

## Files Modified

| File | Change |
|------|--------|
| `backend/app/api/v1/endpoints/diagnostics.py` | Replaced phantom provider with real registry lookup |
| `backend/app/services/search/providers/google_maps/playwright_adapter.py` | Direct URL navigation, consent handling, error screenshots |
| `backend/app/services/search/providers/google_maps/provider.py` | Added `nonlocal count` to fix closure variable bug |
| `frontend/src/pages/DeveloperPage.tsx` | Dynamic adapter status display from API response |

---

## Execution Trace (Verified)

```
[STEP-1] Registered providers: ['mock', 'google_maps']
[STEP-2] Provider: GoogleMapsProvider
[STEP-2] Adapter: PlaywrightAdapter
[STEP-2] Adapter is not None: True

[STEP-3] Running full pipeline: SearchEngine.run_search()...
[STEP-3] Response status: completed
[STEP-3] Result count: 5
[STEP-3] Duration: 5.1s

[RESULTS]
  ✓ BIRLA OPEN MINDS PRESCHOOL - BEST PRESCHOOL IN KANKARBAGH PATNA | School | Patna
  ✓ Holy Mission Senior Secondary school | School | Patna
  ✓ ALLEN JOSEPH'S PUBLIC SCHOOL | School | Patna
  ✓ Modern convent school | School | Patna
  ✓ Vatsalya Niketan School | School | Patna

[CLEANUP] Done
```

---

## Adapter Registration (Verified)

```
adapter: <...playwright_adapter.PlaywrightAdapter object at 0x72719f24c460>
type: PlaywrightAdapter
```

---

## Browser Launch Status (Verified)

```
[STEP-4a] Starting Playwright...
[STEP-4b] Launching Chromium...
[STEP-4c] Browser connected: True
```

---

## Google Maps Navigation Status (Verified)

```
[STEP-4e] Navigating to: https://www.google.com/maps/search/School+in+Patna
[STEP-4f] Page loaded. URL: https://www.google.com/maps/search/School+in+Patna
[STEP-5a] Waiting for results feed...
[STEP-5b] Feed appeared!
[STEP-5c] Looking for business cards (a.hfpxzc)...
[STEP-5d] Found 9 business cards
```

---

## Businesses Extracted (Verified)

Playwright test (raw browser): **9 businesses** extracted
Pipeline test (full engine): **5 businesses** (capped by `max_results=5`)
HTTP Job API test: **5 businesses** (capped by `max_results=5`)

```
✓ BIRLA OPEN MINDS PRESCHOOL - BEST PRESCHOOL IN KANKARBAGH PATNA
✓ Holy Mission Senior Secondary school
✓ ALLEN JOSEPH'S PUBLIC SCHOOL
✓ Modern convent school
✓ Vatsalya Niketan School
✓ Bishop Public School
✓ St. Xavier's High School, Patna
✓ Hargovind singh senior secondary school patna
✓ Lohia Nagar Mount Carmel High School (Boys Wing)
```

---

## HTTP Job API End-to-End Trace (Verified)

```
Job created:
  ID: 4941430c-decb-42cf-8e65-3db6726968e9
  Status: Queued
  Poll 0 - Status: Running | Stage: Searching
  Poll 5 - Status: Running | Stage: Fetching results (20%)
  Poll 6 - Status: Running | Stage: Fetching results (60%)
  Poll 7 - Status: Running | Stage: Fetching results (90%)
  Poll 8 - Status: Completed | Stage: Completed

Results: 5 businesses
  - BIRLA OPEN MINDS PRESCHOOL - BEST PRESCHOOL IN KANKARBAGH PATNA | Patna
  - Holy Mission Senior Secondary school | Patna
  - ALLEN JOSEPH'S PUBLIC SCHOOL | Patna
  - Modern convent school | Patna
  - Vatsalya Niketan School | Patna
```

---

## Backend Route Verification (All 200 OK)

| Route | Status |
|-------|--------|
| `/api/v1/health` | 200 |
| `/api/v1/system/mode` | 200 |
| `/api/v1/diagnostics/diagnostics` | 200 |
| `/api/v1/history/history` | 200 |

---

## Diagnostics API Response (Verified)

```json
{
  "provider": "google_maps",
  "version": "1.0",
  "capabilities": ["search", "pagination"],
  "health": { "status": "Ready" },
  "adapter": "Connected"
}
```

---

## Developer Mode UI Status

The DeveloperPage.tsx now dynamically reads the `adapter` field from the diagnostics API:
- `"Connected"` → Displays: **Playwright Adapter** — Connected & Ready (green)
- Anything else → Displays: **Playwright Adapter** — {reason} (red)

---

## Verification Steps Summary

| Step | Description | Result |
|------|-------------|--------|
| STEP-1 | PlaywrightAdapter instantiation | ✅ Verified — object in registry |
| STEP-2 | GoogleMapsProvider receives adapter | ✅ Verified — `adapter is not None` |
| STEP-3 | SearchEngine calls adapter through pipeline | ✅ Verified — 5 results returned |
| STEP-4 | Playwright launches Chromium in Docker | ✅ Verified — `browser.is_connected() == True` |
| STEP-5 | Real search: "School in Patna" | ✅ Verified — 9 business cards detected |
| STEP-6 | Failure point identification | ✅ Three root causes found and fixed |
| STEP-7 | Developer Mode shows actual adapter status | ✅ Verified — "Connected" from live API |
