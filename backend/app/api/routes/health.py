from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.health_service import HealthService


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
@router.get("/api/v1/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    return HealthService().get_health_status()
