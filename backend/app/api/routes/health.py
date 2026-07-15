from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.exceptions import DatabaseUnavailableError
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService


router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthResponse}},
)
@router.get(
    "/api/v1/health",
    response_model=HealthResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthResponse}},
)
async def get_health() -> HealthResponse | JSONResponse:
    try:
        return await HealthService().get_health_status()
    except DatabaseUnavailableError as error:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=error.payload,
        )
