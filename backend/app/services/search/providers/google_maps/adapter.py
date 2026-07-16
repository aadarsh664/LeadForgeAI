from abc import ABC, abstractmethod
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
