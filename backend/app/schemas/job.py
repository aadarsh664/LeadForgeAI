from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.schemas.search import SearchRequest, NormalizedBusiness

class JobState:
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    RETRYING = "retrying"

class JobProgress(BaseModel):
    percent: int = 0
    stage: str = "Initializing"
    processed_count: int = 0
    estimated_remaining_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration: Optional[float] = None
    logs: List[str] = []

class SearchJob(BaseModel):
    id: str
    state: str = JobState.PENDING
    request: SearchRequest
    provider: str
    progress: JobProgress = Field(default_factory=JobProgress)
    results: List[NormalizedBusiness] = []
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    retries: int = 0
    max_retries: int = 3
