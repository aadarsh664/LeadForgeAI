import os

# Create directories
os.makedirs("backend/app/schemas", exist_ok=True)
os.makedirs("backend/app/services/search", exist_ok=True)

# 1. Schemas (Models)
schemas_search_py = """from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class SearchFilters(BaseModel):
    has_website: bool = False
    has_email: bool = False
    has_phone: bool = False
    min_rating: Optional[float] = None
    min_reviews: Optional[int] = None
    open_now: bool = False
    verified: bool = False
    hide_closed: bool = False

class SearchRequest(BaseModel):
    category: str = Field(..., description="Business category to search for")
    location: str = Field(..., description="Location to search in")
    keywords: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    radius: Optional[int] = Field(10, description="Radius in km")
    max_results: Optional[int] = Field(500, description="Maximum number of results to fetch")
    language: Optional[str] = Field("en", description="Language code")
    filters: Optional[SearchFilters] = None

class NormalizedBusiness(BaseModel):
    business_id: str
    name: str
    category: str
    rating: Optional[float] = None
    reviews: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_open: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_closed: Optional[bool] = None
    provider_source: str
    discovery_date: datetime
    raw_data: Dict[str, Any]

class SearchResponse(BaseModel):
    search_id: str
    status: str
    progress: int
    provider: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    result_count: int = 0
    duration: Optional[float] = None
    results: List[NormalizedBusiness] = []
    error: Optional[str] = None
"""

with open("backend/app/schemas/search.py", "w") as f:
    f.write(schemas_search_py)

# 2. Exceptions
exceptions_py = """class SearchException(Exception):
    pass

class SearchValidationError(SearchException):
    pass

class ProviderNotFoundError(SearchException):
    pass

class ProviderExecutionError(SearchException):
    pass
"""

with open("backend/app/services/search/exceptions.py", "w") as f:
    f.write(exceptions_py)

# 3. Provider Interface
provider_py = """from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List
from app.schemas.search import SearchRequest

class BaseSearchProvider(ABC):
    
    @abstractmethod
    async def initialize(self) -> None:
        pass

    @abstractmethod
    async def validate(self, request: SearchRequest) -> bool:
        pass

    @abstractmethod
    async def search(self, request: SearchRequest) -> AsyncGenerator[List[Dict[str, Any]], None]:
        \"\"\"
        Yields batches of raw provider data.
        \"\"\"
        yield []

    @abstractmethod
    async def cancel(self) -> None:
        pass

    @abstractmethod
    async def health(self) -> bool:
        pass

    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        pass
"""

with open("backend/app/services/search/provider.py", "w") as f:
    f.write(provider_py)

# 4. Registry
registry_py = """from typing import Dict, List, Type
from app.services.search.provider import BaseSearchProvider
from app.services.search.exceptions import ProviderNotFoundError

class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, BaseSearchProvider] = {}

    def register(self, name: str, provider: BaseSearchProvider) -> None:
        self._providers[name] = provider

    def get_provider(self, name: str) -> BaseSearchProvider:
        if name not in self._providers:
            raise ProviderNotFoundError(f"Provider '{name}' not found in registry.")
        return self._providers[name]

    def list_providers(self) -> List[str]:
        return list(self._providers.keys())

    def get_default_provider(self) -> BaseSearchProvider:
        if not self._providers:
            raise ProviderNotFoundError("No providers registered.")
        return list(self._providers.values())[0]
"""

with open("backend/app/services/search/registry.py", "w") as f:
    f.write(registry_py)

# 5. Normalizer
normalizer_py = """from typing import Any, Dict, List
from datetime import datetime, timezone
from app.schemas.search import NormalizedBusiness
import uuid

class SearchNormalizer:
    def normalize(self, raw_data: Dict[str, Any], provider_name: str) -> NormalizedBusiness:
        \"\"\"
        Base normalization logic. 
        In the future, providers will have specific normalizers or pass their mapping.
        For now, this assumes the provider tries to give somewhat standardized raw data.
        \"\"\"
        return NormalizedBusiness(
            business_id=raw_data.get("id", str(uuid.uuid4())),
            name=raw_data.get("name", "Unknown Business"),
            category=raw_data.get("category", "Unknown"),
            rating=raw_data.get("rating"),
            reviews=raw_data.get("reviews"),
            address=raw_data.get("address"),
            city=raw_data.get("city"),
            state=raw_data.get("state"),
            country=raw_data.get("country"),
            phone=raw_data.get("phone"),
            email=raw_data.get("email"),
            website=raw_data.get("website"),
            latitude=raw_data.get("latitude"),
            longitude=raw_data.get("longitude"),
            is_open=raw_data.get("is_open"),
            is_verified=raw_data.get("is_verified"),
            is_closed=raw_data.get("is_closed"),
            provider_source=provider_name,
            discovery_date=datetime.now(timezone.utc),
            raw_data=raw_data
        )

    def normalize_batch(self, raw_batch: List[Dict[str, Any]], provider_name: str) -> List[NormalizedBusiness]:
        return [self.normalize(item, provider_name) for item in raw_batch]
"""

with open("backend/app/services/search/normalizer.py", "w") as f:
    f.write(normalizer_py)

# 6. Validator
validator_py = """from app.schemas.search import SearchRequest
from app.services.search.exceptions import SearchValidationError

class SearchValidator:
    def validate(self, request: SearchRequest) -> None:
        if not request.category or not request.category.strip():
            raise SearchValidationError("Category is required.")
        if not request.location or not request.location.strip():
            raise SearchValidationError("Location is required.")
        if request.max_results and request.max_results <= 0:
            raise SearchValidationError("Maximum results must be greater than 0.")
        if request.radius and request.radius <= 0:
            raise SearchValidationError("Radius must be greater than 0.")
"""

with open("backend/app/services/search/validator.py", "w") as f:
    f.write(validator_py)

# 7. Pipeline
pipeline_py = """import time
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
"""

with open("backend/app/services/search/pipeline.py", "w") as f:
    f.write(pipeline_py)

# 8. Engine
engine_py = """from typing import Optional
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
"""

with open("backend/app/services/search/engine.py", "w") as f:
    f.write(engine_py)

# 9. Init
init_py = """from .engine import SearchEngine
from .registry import ProviderRegistry
from .provider import BaseSearchProvider
from .exceptions import SearchException

__all__ = [
    "SearchEngine",
    "ProviderRegistry",
    "BaseSearchProvider",
    "SearchException"
]
"""

with open("backend/app/services/search/__init__.py", "w") as f:
    f.write(init_py)

print("Architecture generation complete.")
