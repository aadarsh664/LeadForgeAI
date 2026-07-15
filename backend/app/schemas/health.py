from pydantic import BaseModel


class HealthResponse(BaseModel):
    success: bool
    status: str
    application: str
    database: str
