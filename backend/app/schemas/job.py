from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.search import SearchRequest, NormalizedBusiness

class JobStatus:
    PENDING = "Pending"
    QUEUED = "Queued"
    RUNNING = "Running"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    FAILED = "Failed"
    RETRYING = "Retrying"

class JobProgress(BaseModel):
    percentage: int = 0
    stage: str = "Initializing"
    processed_count: int = 0
    estimated_remaining_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None

class SearchJob(BaseModel):
    id: str
    request: SearchRequest
    provider: str
    status: str = JobStatus.PENDING
    progress: JobProgress
    results: List[NormalizedBusiness] = []
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
