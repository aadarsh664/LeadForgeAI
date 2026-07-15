from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    application: str
    version: str
    backend: str
    database: str
    docker: str
    n8n: str
    timestamp: datetime
    overall_status: str


class ComponentHealthResponse(BaseModel):
    success: bool
    status: str
    message: str | None = None
