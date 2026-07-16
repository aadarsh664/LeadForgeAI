import asyncio
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
                name = name.split("\n")[0]
            
            # Click the item to load the side panel (details pane)
            # To avoid breaking, we will just extract what is immediately available in the feed list.
            # In a full scraper, we would click each card and scrape the detailed pane.
            
            # The feed item often has rating/reviews in text
            text_content = await element.inner_text()
            lines = [line.strip() for line in text_content.split("\n") if line.strip()]
            
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
            import urllib.parse
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/maps/search/{encoded_query}"
            
            await page.goto(search_url, wait_until="domcontentloaded")
            
            try:
                consent_btn = page.locator("button:has-text('Accept all'), button:has-text('I agree')")
                if await consent_btn.count() > 0:
                    await consent_btn.first.click()
            except:
                pass
            
            
            # Wait for results container. `.hfpxzc` is a common class for result links, or `[role="feed"]`
            # We wait for the feed to appear
            feed = page.locator("div[role='feed'], div[aria-label*='Results for']")
            try:
                await feed.first.wait_for(state="visible", timeout=15000)
                feed = feed.first
            except:
                ProviderLogger.log_error(f"Feed did not appear, possibly no results or UI changed. URL: {page.url}")
                await page.screenshot(path="playwright_error.png")
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
