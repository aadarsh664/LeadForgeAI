from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIRECTORY = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIRECTORY.parent


class Settings(BaseSettings):
    application_name: str = "LeadForgeAI"
    backend_port: int = 8000
    frontend_port: int = 5173
    cors_allowed_origins: str = "http://localhost:5173"
    database_url: str = (
        "postgresql+asyncpg://leadforgeai:leadforgeai@localhost:5432/leadforgeai"
    )

    model_config = SettingsConfigDict(
        env_file=(BACKEND_DIRECTORY / ".env", PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
