import os

# Create providers directory
os.makedirs("backend/app/services/search/providers", exist_ok=True)

# 1. Mock Provider
mock_py = """import asyncio
import uuid
from typing import Any, AsyncGenerator, Dict, List
from app.schemas.search import SearchRequest
from app.services.search.provider import BaseSearchProvider

class MockSearchProvider(BaseSearchProvider):
    async def initialize(self) -> None:
        # Simulate initialization delay
        await asyncio.sleep(0.5)

    async def validate(self, request: SearchRequest) -> bool:
        return True

    async def search(self, request: SearchRequest) -> AsyncGenerator[List[Dict[str, Any]], None]:
        # Yield one batch of 20 mock results
        await asyncio.sleep(1.5) # Simulate search delay
        
        batch = []
        for i in range(1, 21):
            batch.append({
                "id": str(uuid.uuid4()),
                "name": f"Demo Business {i}",
                "category": request.category,
                "rating": 4.5,
                "reviews": 100 + i,
                "address": "Example Street",
                "city": request.city or "Sample City",
                "state": request.state or "Example State",
                "country": request.country or "Example Country",
                "phone": "+1-000-000-0000",
                "email": "demo@example.com",
                "website": "https://example.com",
                "latitude": 0.0,
                "longitude": 0.0,
                "is_open": True,
                "is_verified": True,
                "is_closed": False,
                "demo_data": True # special flag for frontend
            })
        
        yield batch

    async def cancel(self) -> None:
        pass

    async def health(self) -> bool:
        return True

    def metadata(self) -> Dict[str, Any]:
        return {
            "name": "Mock Provider",
            "version": "1.0",
            "capabilities": ["demo"]
        }
"""
with open("backend/app/services/search/providers/mock.py", "w") as f:
    f.write(mock_py)

with open("backend/app/services/search/providers/__init__.py", "w") as f:
    f.write("from .mock import MockSearchProvider\n")

# 2. Dependencies
deps_py = """from fastapi import Request
from app.services.search.engine import SearchEngine
from app.services.search.registry import ProviderRegistry
from app.services.search.providers.mock import MockSearchProvider

# Initialize singleton registry and engine
_registry = ProviderRegistry()
_registry.register("mock", MockSearchProvider())
_search_engine = SearchEngine(_registry)

def get_search_engine() -> SearchEngine:
    return _search_engine
"""
with open("backend/app/core/dependencies.py", "w") as f:
    f.write(deps_py)

# 3. Search Endpoints
os.makedirs("backend/app/api/v1/endpoints", exist_ok=True)
search_endpoint_py = """from fastapi import APIRouter, Depends
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search.engine import SearchEngine
from app.core.dependencies import get_search_engine

router = APIRouter()

@router.post("/businesses", response_model=SearchResponse)
async def search_businesses(
    request: SearchRequest,
    engine: SearchEngine = Depends(get_search_engine)
):
    # Always use mock provider for now
    return await engine.run_search(request, provider_name="mock")
"""
with open("backend/app/api/v1/endpoints/search.py", "w") as f:
    f.write(search_endpoint_py)

# 4. Include router in main.py
with open("backend/app/main.py", "r") as f:
    main_content = f.read()

if "from app.api.v1.endpoints import search" not in main_content:
    # We need to add the router
    main_content = main_content.replace(
        "from app.api.v1.endpoints import health",
        "from app.api.v1.endpoints import health\nfrom app.api.v1.endpoints import search"
    )
    main_content = main_content.replace(
        'api_router.include_router(health.router, tags=["health"])',
        'api_router.include_router(health.router, tags=["health"])\napi_router.include_router(search.router, prefix="/search", tags=["search"])'
    )
    with open("backend/app/main.py", "w") as f:
        f.write(main_content)

print("Backend for TASK-013 generated successfully.")
