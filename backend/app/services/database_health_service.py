from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.session import async_session_factory


class DatabaseHealthService:
    """Service responsible for checking database connectivity."""

    async def is_connected(self) -> bool:
        try:
            async with async_session_factory() as session:
                await session.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False
