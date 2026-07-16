import os

base_dir = "backend/app/services/search/providers/google_maps"
os.makedirs(base_dir, exist_ok=True)

# 1. Config
config_py = """from pydantic import BaseModel
from typing import Optional, Dict

class ProviderConfig(BaseModel):
    country: str = "US"
    language: str = "en"
    search_delay: float = 2.0
    concurrency: int = 1
    timeout: int = 30
    retries: int = 3
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    headless_mode: bool = True
    proxy: Optional[str] = None
    cookies: Optional[Dict[str, str]] = None
    rate_limit_rpm: int = 60
"""
with open(f"{base_dir}/config.py", "w") as f: f.write(config_py)

# 2. Health
health_py = """from enum import Enum
from pydantic import BaseModel
from typing import Optional

class HealthStatus(str, Enum):
    READY = "Ready"
    BUSY = "Busy"
    OFFLINE = "Offline"
    RATE_LIMITED = "Rate Limited"
    AUTH_REQUIRED = "Authentication Required"
    BLOCKED = "Blocked"
    UNKNOWN = "Unknown"

class ProviderHealth(BaseModel):
    status: HealthStatus = HealthStatus.UNKNOWN
    last_check: Optional[str] = None
    error_message: Optional[str] = None
"""
with open(f"{base_dir}/health.py", "w") as f: f.write(health_py)

# 3. Logger
logger_py = """import logging

logger = logging.getLogger("google_maps_provider")
logger.setLevel(logging.INFO)

class ProviderLogger:
    @staticmethod
    def log_started(query: str):
        logger.info(f"Search Started: {query}")

    @staticmethod
    def log_finished(query: str, duration: float, count: int):
        logger.info(f"Search Finished: {query} in {duration:.2f}s, found {count}")

    @staticmethod
    def log_error(error: str):
        logger.error(f"Provider Error: {error}")

    @staticmethod
    def log_retry(attempt: int, error: str):
        logger.warning(f"Retry {attempt} due to: {error}")

    @staticmethod
    def log_rate_limit():
        logger.warning("Rate limit hit.")
"""
with open(f"{base_dir}/logger.py", "w") as f: f.write(logger_py)

# 4. Rate Limiter
rate_limiter_py = """import time
import asyncio
from typing import Optional

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.interval = 60.0 / self.rpm if self.rpm > 0 else 0
        self.last_request: float = 0.0

    async def wait(self):
        if self.rpm <= 0:
            return
            
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.interval:
            wait_time = self.interval - elapsed
            await asyncio.sleep(wait_time)
            
        self.last_request = time.time()
"""
with open(f"{base_dir}/rate_limiter.py", "w") as f: f.write(rate_limiter_py)

# 5. Retry Manager
retry_py = """import asyncio
from typing import Callable, Any, Awaitable
from .logger import ProviderLogger

class RetryManager:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    async def execute(self, func: Callable[[], Awaitable[Any]]) -> Any:
        attempt = 0
        while attempt <= self.max_retries:
            try:
                return await func()
            except Exception as e:
                attempt += 1
                if attempt > self.max_retries:
                    ProviderLogger.log_error(f"Max retries exceeded. Last error: {str(e)}")
                    raise e
                
                ProviderLogger.log_retry(attempt, str(e))
                await asyncio.sleep(self.backoff_factor ** attempt)
"""
with open(f"{base_dir}/retry.py", "w") as f: f.write(retry_py)

# 6. Adapter Base
adapter_py = """from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any
from app.schemas.search import SearchRequest
from .config import ProviderConfig

class ProviderAdapter(ABC):
    @abstractmethod
    async def initialize(self, config: ProviderConfig) -> None:
        pass

    @abstractmethod
    async def execute_search(self, request: SearchRequest) -> AsyncGenerator[Dict[str, Any], None]:
        yield {}

    @abstractmethod
    async def cleanup(self) -> None:
        pass
"""
with open(f"{base_dir}/adapter.py", "w") as f: f.write(adapter_py)

# 7. Normalizer
normalizer_py = """from typing import Dict, Any

class GoogleMapsNormalizer:
    @staticmethod
    def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
        # Converts Google Maps specific raw schema into the common schema
        # For now, it just passes through as we haven't implemented the scraper
        return {
            "name": raw.get("name", "Unknown Business"),
            "category": raw.get("category", "Uncategorized"),
            "phone": raw.get("phone", ""),
            "website": raw.get("website", ""),
            "address": raw.get("address", ""),
            "city": raw.get("city", ""),
            "rating": float(raw.get("rating", 0.0)),
            "reviews": int(raw.get("reviews", 0)),
            "raw_data": raw
        }
"""
with open(f"{base_dir}/normalizer.py", "w") as f: f.write(normalizer_py)

# 8. Provider
provider_py = """import time
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
"""
with open(f"{base_dir}/provider.py", "w") as f: f.write(provider_py)
with open(f"{base_dir}/__init__.py", "w") as f: f.write("from .provider import GoogleMapsProvider\n")

# Need to expose the mock provider and google maps provider configs to frontend?
# Let's add a diagnostics endpoint
diagnostics_api = """from fastapi import APIRouter
from app.services.search.providers.google_maps.provider import GoogleMapsProvider
from app.services.search.providers.google_maps.config import ProviderConfig

router = APIRouter()

# Temporary mock instance just for diagnostics
temp_provider = GoogleMapsProvider()

@router.get("/diagnostics")
async def get_provider_diagnostics():
    return temp_provider.metadata()
"""
with open("backend/app/api/v1/endpoints/diagnostics.py", "w") as f: f.write(diagnostics_api)

with open("backend/app/main.py", "r") as f:
    main_content = f.read()

if "from app.api.v1.endpoints import diagnostics" not in main_content:
    main_content = main_content.replace(
        "from app.api.v1.endpoints import jobs",
        "from app.api.v1.endpoints import jobs\nfrom app.api.v1.endpoints import diagnostics"
    )
    main_content = main_content.replace(
        'api_router.include_router(jobs.router, prefix="/search", tags=["search-jobs"])',
        'api_router.include_router(jobs.router, prefix="/search", tags=["search-jobs"])\napi_router.include_router(diagnostics.router, prefix="/diagnostics", tags=["diagnostics"])'
    )
    with open("backend/app/main.py", "w") as f:
        f.write(main_content)

print("Backend for TASK-017 generated successfully.")
