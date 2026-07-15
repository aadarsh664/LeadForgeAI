from app.core.config import get_settings
from app.schemas.health import HealthResponse


class HealthService:
    """Application health service for bootstrap checks."""

    def get_health_status(self) -> HealthResponse:
        settings = get_settings()
        return HealthResponse(
            success=True,
            status="healthy",
            application=settings.application_name,
        )
