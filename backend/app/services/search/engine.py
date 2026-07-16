from typing import Optional
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search.registry import ProviderRegistry
from app.services.search.validator import SearchValidator
from app.services.search.pipeline import SearchPipeline

class SearchEngine:
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry
        self.validator = SearchValidator()

    async def run_search(self, request: SearchRequest, provider_name: Optional[str] = None) -> SearchResponse:
        # 1. Validate the universal rules
        self.validator.validate(request)
        
        # 2. Get the requested provider or default
        if provider_name:
            provider = self.registry.get_provider(provider_name)
        else:
            provider = self.registry.get_default_provider()
            provider_name = self.registry.list_providers()[0]
            
        # 3. Create pipeline and execute
        pipeline = SearchPipeline(provider=provider, provider_name=provider_name)
        return await pipeline.execute(request)

    async def stream_search(self, request: SearchRequest, provider_name: Optional[str] = None):
        self.validator.validate(request)
        if provider_name:
            provider = self.registry.get_provider(provider_name)
        else:
            provider = self.registry.get_default_provider()
            provider_name = self.registry.list_providers()[0]
            
        pipeline = SearchPipeline(provider=provider, provider_name=provider_name)
        async for partial_response in pipeline.execute_stream(request):
            yield partial_response
