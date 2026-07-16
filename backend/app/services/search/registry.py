from typing import Dict, List, Type
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
