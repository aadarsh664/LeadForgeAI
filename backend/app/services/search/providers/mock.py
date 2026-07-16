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
        # Yield 4 batches of 5 to simulate progression
        for batch_num in range(4):
            await asyncio.sleep(1.0) # simulate processing time
            batch = []
            for i in range(1, 6):
                idx = batch_num * 5 + i
                batch.append({
                    "id": str(uuid.uuid4()),
                    "name": f"Demo Business {idx}",
                    "category": request.category,
                    "rating": 4.5,
                    "reviews": 100 + idx,
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
                    "demo_data": True
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
