import os
import httpx
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.core.session import async_session_factory
from app.core.config import get_settings


class HealthChecker:
    @staticmethod
    async def check_database() -> tuple[bool, str]:
        try:
            async with async_session_factory() as session:
                await session.execute(text("SELECT 1"))
            return True, "connected"
        except SQLAlchemyError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def check_docker() -> tuple[bool, str]:
        if os.path.exists("/.dockerenv"):
            return True, "connected"
        return False, "disconnected"

    @staticmethod
    async def check_n8n() -> tuple[bool, str]:
        settings = get_settings()
        n8n_url = getattr(settings, "n8n_base_url", "http://n8n:5678")
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(f"{n8n_url}/healthz")
                if response.status_code == 200:
                    return True, "connected"
                return False, f"HTTP {response.status_code}"
        except httpx.RequestError:
            return False, "disconnected"
        except Exception as e:
            return False, str(e)
