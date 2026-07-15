from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    application_name: str = "LeadForgeAI"
    backend_port: int = 8000
    frontend_port: int = 5173
    cors_allowed_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(extra="ignore")

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
