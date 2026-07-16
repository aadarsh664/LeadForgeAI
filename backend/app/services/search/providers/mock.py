import asyncio
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
