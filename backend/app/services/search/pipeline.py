import time
import uuid
from datetime import datetime, timezone
from typing import Optional

from app.schemas.search import SearchRequest, SearchResponse
from app.services.search.provider import BaseSearchProvider
from app.services.search.normalizer import SearchNormalizer
from app.services.search.exceptions import ProviderExecutionError

class SearchPipeline:
    def __init__(self, provider: BaseSearchProvider, provider_name: str):
        self.provider = provider
        self.provider_name = provider_name
        self.normalizer = SearchNormalizer()

    async def execute(self, request: SearchRequest) -> SearchResponse:
        search_id = str(uuid.uuid4())
        started_at = datetime.now(timezone.utc)
        start_time = time.time()
        
        response = SearchResponse(
            search_id=search_id,
            status="running",
            progress=0,
            provider=self.provider_name,
            started_at=started_at
        )

        try:
            await self.provider.initialize()
            is_valid = await self.provider.validate(request)
            if not is_valid:
                raise ProviderExecutionError("Provider rejected the search request.")
            
            all_results = []
            async for raw_batch in self.provider.search(request):
                normalized_batch = self.normalizer.normalize_batch(raw_batch, self.provider_name)
                all_results.extend(normalized_batch)
                
            response.results = all_results
            response.result_count = len(all_results)
            response.status = "completed"
            response.progress = 100
        except Exception as e:
            response.status = "failed"
            response.error = str(e)
        finally:
            response.finished_at = datetime.now(timezone.utc)
            response.duration = time.time() - start_time

        return response
