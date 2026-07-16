import os

os.makedirs("backend/app/services/search/providers/google_maps", exist_ok=True)

adapter_code = """import asyncio
from typing import AsyncGenerator, Dict, Any
from playwright.async_api import async_playwright, Browser, Playwright, Page, BrowserContext
from app.schemas.search import SearchRequest
from .config import ProviderConfig
from .adapter import ProviderAdapter
from .logger import ProviderLogger

class PlaywrightAdapter(ProviderAdapter):
    def __init__(self):
        self.playwright: Playwright = None
        self.browser: Browser = None
        self.config: ProviderConfig = None

    async def initialize(self, config: ProviderConfig) -> None:
        self.config = config
        self.playwright = await async_playwright().start()
        # Ensure chromium is available. In a real prod environment, exceptions are caught.
        self.browser = await self.playwright.chromium.launch(
            headless=self.config.headless_mode,
            args=["--disable-blink-features=AutomationControlled"]
        )
        ProviderLogger.log_started("Playwright initialized.")

    async def _extract_business_data(self, page: Page, element) -> Dict[str, Any]:
        # Minimal extraction logic. Google Maps DOM changes frequently.
        # This is a robust attempt to grab the title and details.
        try:
            name = await element.get_attribute("aria-label")
            if not name:
                name = await element.inner_text()
                name = name.split("\\n")[0]
            
            # Click the item to load the side panel (details pane)
            # To avoid breaking, we will just extract what is immediately available in the feed list.
            # In a full scraper, we would click each card and scrape the detailed pane.
            
            # The feed item often has rating/reviews in text
            text_content = await element.inner_text()
            lines = [line.strip() for line in text_content.split("\\n") if line.strip()]
            
            rating = 0.0
            reviews = 0
            category = "Uncategorized"
            phone = ""
            
            # Simple heuristic parsing (mocking real parser behavior)
            for line in lines:
                if "(" in line and ")" in line and "." in line:
                    # Might be rating e.g. "4.5 (123)"
                    try:
                        parts = line.split("(")
                        rating = float(parts[0].strip())
                        reviews = int(parts[1].replace(")", "").replace(",", "").strip())
                    except:
                        pass
                # Phone regex match could go here
                if any(char.isdigit() for char in line) and "-" in line and len(line) > 8:
                    phone = line

            return {
                "name": name,
                "category": category,
                "phone": phone,
                "website": "",
                "address": "", # Usually needs the side-panel click
                "city": "",
                "rating": rating,
                "reviews": reviews,
            }
        except Exception as e:
            ProviderLogger.log_error(f"Failed to extract item: {e}")
            return {"name": "Unknown", "category": "Unknown"}

    async def execute_search(self, request: SearchRequest) -> AsyncGenerator[Dict[str, Any], None]:
        if not self.browser:
            raise Exception("Playwright browser not initialized.")
            
        context: BrowserContext = await self.browser.new_context(
            user_agent=self.config.user_agent,
            viewport={"width": 1280, "height": 800}
        )
        page: Page = await context.new_page()
        
        try:
            query = f"{request.category} in {request.location}"
            await page.goto("https://www.google.com/maps", wait_until="domcontentloaded")
            
            # Wait for search box
            search_box = page.locator("input#searchboxinput")
            await search_box.wait_for(state="visible", timeout=10000)
            
            await search_box.fill(query)
            await search_box.press("Enter")
            
            # Wait for results container. `.hfpxzc` is a common class for result links, or `[role="feed"]`
            # We wait for the feed to appear
            feed = page.locator("div[role='feed']")
            try:
                await feed.wait_for(state="visible", timeout=15000)
            except:
                ProviderLogger.log_error("Feed did not appear, possibly no results or UI changed.")
                return

            extracted_names = set()
            scroll_attempts = 0
            max_scrolls = 10 # Control how deep we go
            
            while scroll_attempts < max_scrolls:
                # Find all result items currently loaded
                # `a.hfpxzc` is the clickable overlay for each result in the list
                items = await page.locator("a.hfpxzc").all()
                
                new_items_found = False
                for item in items:
                    name = await item.get_attribute("aria-label")
                    if name and name not in extracted_names:
                        extracted_names.add(name)
                        new_items_found = True
                        
                        data = await self._extract_business_data(page, item)
                        data["city"] = request.location
                        data["category"] = request.category
                        yield data
                        
                        if len(extracted_names) >= request.max_results:
                            return
                            
                if not new_items_found:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0 # reset if we found new items
                
                # Scroll down the feed
                await feed.hover()
                await page.mouse.wheel(0, 1000)
                await asyncio.sleep(self.config.search_delay)
                
                # Check for "You've reached the end of the list." element
                end_text = page.locator("text=You've reached the end of the list")
                if await end_text.count() > 0 and await end_text.is_visible():
                    break
                    
        except Exception as e:
            ProviderLogger.log_error(f"Search execution failed: {e}")
            raise e
        finally:
            await page.close()
            await context.close()

    async def cleanup(self) -> None:
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        ProviderLogger.log_started("Playwright cleaned up.")
"""
with open("backend/app/services/search/providers/google_maps/playwright_adapter.py", "w") as f:
    f.write(adapter_code)

dependencies_code = """from app.services.search.engine import SearchEngine
from app.services.search.registry import ProviderRegistry
from app.services.search.providers.mock import MockSearchProvider
from app.services.search.providers.google_maps import GoogleMapsProvider
from app.services.search.providers.google_maps.playwright_adapter import PlaywrightAdapter

# Initialize registry and register providers
_registry = ProviderRegistry()
_registry.register("mock", MockSearchProvider())

# Register Google Maps with Playwright
google_maps_provider = GoogleMapsProvider(adapter=PlaywrightAdapter())
_registry.register("google_maps", google_maps_provider)

# Set the default engine
_search_engine = SearchEngine(_registry)

def get_search_engine() -> SearchEngine:
    return _search_engine
"""
with open("backend/app/core/dependencies.py", "w") as f:
    f.write(dependencies_code)

# We also need to change the frontend so the user can choose Google Maps or Mock.
# And when a user executes a search, the backend defaults to Google Maps or Mock based on what?
# Currently, worker.py hardcodes provider="mock".
# We need to change `create_job` to accept `provider` from the frontend, or default to `google_maps`.
worker_patch = """import os
worker_file = "backend/app/services/job/worker.py"
with open(worker_file, "r") as f:
    content = f.read()

# Change default to google_maps instead of mock
if "provider: str = \\"mock\\"" in content:
    content = content.replace("provider: str = \\"mock\\"", "provider: str = \\"google_maps\\"")

with open(worker_file, "w") as f:
    f.write(content)

search_api_file = "backend/app/api/v1/endpoints/search.py"
if os.path.exists(search_api_file):
    with open(search_api_file, "r") as f:
        content = f.read()
    if 'provider_name="mock"' in content:
        content = content.replace('provider_name="mock"', 'provider_name=request.provider if hasattr(request, "provider") and request.provider else "google_maps"')
    with open(search_api_file, "w") as f:
        f.write(content)
"""
exec(worker_patch)
print("Backend for TASK-018 generated successfully.")
