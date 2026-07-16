from fastapi import Request
from app.services.search.engine import SearchEngine
from app.services.search.registry import ProviderRegistry
from app.services.search.providers.mock import MockSearchProvider

# Initialize singleton registry and engine
_registry = ProviderRegistry()
_registry.register("mock", MockSearchProvider())
_search_engine = SearchEngine(_registry)

def get_search_engine() -> SearchEngine:
    return _search_engine
