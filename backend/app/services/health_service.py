from app.core.config import get_settings
from app.core.exceptions import DatabaseUnavailableError
from app.schemas.health import HealthResponse
from app.services.database_health_service import DatabaseHealthService


class HealthService:
    """Application health service for bootstrap checks."""

    def __init__(
        self,
        database_health_service: DatabaseHealthService | None = None,
    ) -> None:
        self.database_health_service = (
            database_health_service or DatabaseHealthService()
        )

    async def get_health_status(self) -> HealthResponse:
        settings = get_settings()
        is_database_connected = await self.database_health_service.is_connected()

        if not is_database_connected:
            raise DatabaseUnavailableError(
                {
                    "success": False,
                    "status": "unhealthy",
                    "application": settings.application_name,
                    "database": "disconnected",
                }
            )

        return HealthResponse(
            success=True,
            status="healthy",
            application=settings.application_name,
            database="connected",
        )
