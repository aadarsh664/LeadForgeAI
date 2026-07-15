from fastapi import APIRouter

from app.schemas.health import ComponentHealthResponse, HealthResponse
from app.services.health_service import HealthService

router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def get_overall_health() -> HealthResponse:
    return await HealthService.get_overall_health()


@router.get("/backend", response_model=ComponentHealthResponse)
async def get_backend_health() -> ComponentHealthResponse:
    return await HealthService.get_backend_health()


@router.get("/database", response_model=ComponentHealthResponse)
async def get_database_health() -> ComponentHealthResponse:
    return await HealthService.get_database_health()


@router.get("/docker", response_model=ComponentHealthResponse)
async def get_docker_health() -> ComponentHealthResponse:
    return await HealthService.get_docker_health()


@router.get("/n8n", response_model=ComponentHealthResponse)
async def get_n8n_health() -> ComponentHealthResponse:
    return await HealthService.get_n8n_health()
