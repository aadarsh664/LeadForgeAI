from datetime import datetime, timezone

from app.core.config import get_settings
from app.core.health import APP_VERSION
from app.schemas.health import ComponentHealthResponse, HealthResponse
from app.utils.health_checker import HealthChecker


class HealthService:
    @staticmethod
    async def get_overall_health() -> HealthResponse:
        settings = get_settings()

        db_ok, _ = await HealthChecker.check_database()
        docker_ok, _ = await HealthChecker.check_docker()
        n8n_ok, _ = await HealthChecker.check_n8n()

        overall_ok = db_ok and docker_ok

        return HealthResponse(
            application=settings.application_name,
            version=APP_VERSION,
            backend="connected",
            database="connected" if db_ok else "disconnected",
            docker="connected" if docker_ok else "disconnected",
            n8n="connected" if n8n_ok else "disconnected",
            timestamp=datetime.now(timezone.utc),
            overall_status="healthy" if overall_ok else "unhealthy",
        )

    @staticmethod
    async def get_backend_health() -> ComponentHealthResponse:
        return ComponentHealthResponse(
            success=True, status="healthy", message="connected"
        )

    @staticmethod
    async def get_database_health() -> ComponentHealthResponse:
        ok, msg = await HealthChecker.check_database()
        return ComponentHealthResponse(
            success=ok, status="healthy" if ok else "unhealthy", message=msg
        )

    @staticmethod
    async def get_docker_health() -> ComponentHealthResponse:
        ok, msg = await HealthChecker.check_docker()
        return ComponentHealthResponse(
            success=ok, status="healthy" if ok else "unhealthy", message=msg
        )

    @staticmethod
    async def get_n8n_health() -> ComponentHealthResponse:
        ok, msg = await HealthChecker.check_n8n()
        return ComponentHealthResponse(
            success=ok, status="healthy" if ok else "unhealthy", message=msg
        )
