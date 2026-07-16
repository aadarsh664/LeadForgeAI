from app.services.search.engine import SearchEngine
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
