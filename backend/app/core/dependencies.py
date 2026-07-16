from fastapi import Request
from app.services.search.engine import SearchEngine
from app.services.search.registry import ProviderRegistry
from app.services.search.providers.mock import MockSearchProvider
from app.services.job.repository import JobRepository
from app.services.job.worker import SearchWorker

# Initialize singleton registry and engine
_registry = ProviderRegistry()
_registry.register("mock", MockSearchProvider())
_search_engine = SearchEngine(_registry)

_job_repo = JobRepository()
_worker = SearchWorker(_job_repo, _search_engine)
# Start worker on import (simplistic, for FastAPI lifespan is better but this works for local)
_worker.start()

def get_search_engine() -> SearchEngine:
    return _search_engine

def get_job_repository() -> JobRepository:
    return _job_repo

def get_search_worker() -> SearchWorker:
    return _worker
