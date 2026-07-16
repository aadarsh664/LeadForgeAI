import time
from typing import AsyncGenerator, Dict, Any, List
from app.schemas.search import SearchRequest
from app.services.search.provider import BaseSearchProvider
from .config import ProviderConfig
from .health import ProviderHealth, HealthStatus
from .logger import ProviderLogger
from .rate_limiter import RateLimiter
from .retry import RetryManager
from .adapter import ProviderAdapter
from .normalizer import GoogleMapsNormalizer

class GoogleMapsProvider(BaseSearchProvider):
    def __init__(self, adapter: ProviderAdapter = None):
        self.config = ProviderConfig()
        self.health_status = ProviderHealth(status=HealthStatus.READY)
        self.rate_limiter = RateLimiter(self.config.rate_limit_rpm)
        self.retry_manager = RetryManager(self.config.retries)
        self.normalizer = GoogleMapsNormalizer()
        self.adapter = adapter
        self._is_cancelled = False

    async def initialize(self) -> None:
        if self.adapter:
            await self.adapter.initialize(self.config)

    async def validate(self, request: SearchRequest) -> bool:
        return True

    async def search(self, request: SearchRequest) -> AsyncGenerator[List[Dict[str, Any]], None]:
        self._is_cancelled = False
        self.health_status.status = HealthStatus.BUSY
        query = f"{request.category} in {request.location}"
        ProviderLogger.log_started(query)
        
        start_time = time.time()
        count = 0
        
        try:
            if not self.adapter:
                # No adapter, return empty
                yield []
                return

            async def fetch_next():
                batch = []
                async for item in self.adapter.execute_search(request):
                    if self._is_cancelled:
                        break
                    normalized = self.normalizer.normalize(item)
                    batch.append(normalized)
                    count += 1
                return batch

            await self.rate_limiter.wait()
            batch = await self.retry_manager.execute(fetch_next)
            
            if batch:
                yield batch
                
        except Exception as e:
            ProviderLogger.log_error(str(e))
            self.health_status.status = HealthStatus.UNKNOWN
            self.health_status.error_message = str(e)
            raise e
        finally:
            ProviderLogger.log_finished(query, time.time() - start_time, count)
            if not self._is_cancelled:
                self.health_status.status = HealthStatus.READY

    async def cancel(self) -> None:
        self._is_cancelled = True
        self.health_status.status = HealthStatus.READY

    async def health(self) -> bool:
        return self.health_status.status == HealthStatus.READY

    def metadata(self) -> Dict[str, Any]:
        return {
            "provider": "google_maps",
            "version": "1.0",
            "capabilities": ["search", "pagination"],
            "config": self.config.model_dump(),
            "health": self.health_status.model_dump()
        }

    async def cleanup(self) -> None:
        if self.adapter:
            await self.adapter.cleanup()
