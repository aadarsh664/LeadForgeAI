from pydantic import BaseModel

class StartupStatusResponse(BaseModel):
    current_step: str
    completed_steps: list[str]
    progress_percentage: int
    overall_status: str
    is_ready: bool
    message: str

class ModeResponse(BaseModel):
    mode: str

class ModeRequest(BaseModel):
    mode: str

