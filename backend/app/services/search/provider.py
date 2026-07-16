from abc import ABC, abstractmethod
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
        """
        Yields batches of raw provider data.
        """
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
