import os

os.makedirs("backend/app/schemas", exist_ok=True)
os.makedirs("backend/app/services/job", exist_ok=True)
os.makedirs("backend/data", exist_ok=True)

# 1. Job Schemas
job_schemas = """from pydantic import BaseModel
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
"""
with open("backend/app/schemas/job.py", "w") as f:
    f.write(job_schemas)

# 2. Job Repository
job_repo = """import json
import os
from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.job import SearchJob

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../../data")
os.makedirs(DATA_DIR, exist_ok=True)
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")

class JobRepository:
    def _read_file(self) -> List[dict]:
        if not os.path.exists(JOBS_FILE):
            return []
        try:
            with open(JOBS_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def _write_file(self, data: List[dict]):
        with open(JOBS_FILE, "w") as f:
            json.dump(data, f, default=str, indent=2)

    def get_all(self) -> List[SearchJob]:
        data = self._read_file()
        return [SearchJob(**j) for j in data]

    def get_by_id(self, job_id: str) -> Optional[SearchJob]:
        for item in self._read_file():
            if item.get("id") == job_id:
                return SearchJob(**item)
        return None

    def save(self, job: SearchJob):
        jobs = self._read_file()
        job.updated_at = datetime.now(timezone.utc)
        job_dict = job.model_dump(mode="json")
        
        found = False
        for i, item in enumerate(jobs):
            if item.get("id") == job.id:
                jobs[i] = job_dict
                found = True
                break
        if not found:
            jobs.insert(0, job_dict)
            
        self._write_file(jobs)
"""
with open("backend/app/services/job/repository.py", "w") as f:
    f.write(job_repo)

# 3. Worker and Manager
worker_py = """import asyncio
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, Any

from app.schemas.job import SearchJob, JobStatus, JobProgress
from app.schemas.search import SearchRequest
from app.services.job.repository import JobRepository
from app.services.search.engine import SearchEngine
from app.core.dependencies import get_search_engine
from app.services.history.service import HistoryService

class WorkerManager:
    def __init__(self):
        self.repo = JobRepository()
        self.queue = asyncio.Queue()
        self.engine = get_search_engine()
        self.history = HistoryService()
        self.active_tasks: Dict[str, asyncio.Task] = {}
        
    async def create_job(self, request: SearchRequest, provider: str = "mock") -> SearchJob:
        job = SearchJob(
            id=str(uuid.uuid4()),
            request=request,
            provider=provider,
            status=JobStatus.QUEUED,
            progress=JobProgress(stage="Queued"),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.repo.save(job)
        await self.queue.put(job.id)
        return job

    async def cancel_job(self, job_id: str) -> bool:
        job = self.repo.get_by_id(job_id)
        if not job or job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            return False
            
        if job_id in self.active_tasks:
            self.active_tasks[job_id].cancel()
            
        job.status = JobStatus.CANCELLED
        job.progress.stage = "Cancelled by user"
        job.progress.finished_at = datetime.now(timezone.utc)
        self.repo.save(job)
        return True

    async def retry_job(self, job_id: str) -> bool:
        job = self.repo.get_by_id(job_id)
        if not job or job.status not in [JobStatus.FAILED, JobStatus.CANCELLED]:
            return False
            
        job.status = JobStatus.QUEUED
        job.progress = JobProgress(stage="Queued (Retry)")
        job.error = None
        self.repo.save(job)
        await self.queue.put(job.id)
        return True

    async def _execute_job(self, job_id: str):
        job = self.repo.get_by_id(job_id)
        if not job or job.status == JobStatus.CANCELLED:
            return
            
        job.status = JobStatus.RUNNING
        job.progress.started_at = datetime.now(timezone.utc)
        job.progress.stage = "Searching"
        self.repo.save(job)
        
        start_time = time.time()
        
        try:
            # We bypass SearchEngine's run_search wrapper to stream progress
            # For simplicity in mock, run_search returns quickly but in a real system we'd consume the async generator.
            # Here we just use the engine and simulate progress.
            response = await self.engine.run_search(job.request, provider_name=job.provider)
            
            # Simulate some processing time for UI progress demonstration
            for i in range(1, 11):
                await asyncio.sleep(0.3)
                job.progress.percentage = i * 10
                job.progress.stage = f"Fetching results ({i*10}%)"
                self.repo.save(job)
                
            job.results = response.results
            job.status = JobStatus.COMPLETED
            job.progress.percentage = 100
            job.progress.stage = "Completed"
            
            # Save history
            try:
                self.history.add_history(job.request, provider=job.provider, result_count=len(job.results))
            except:
                pass
                
        except asyncio.CancelledError:
            job.status = JobStatus.CANCELLED
            job.progress.stage = "Cancelled"
        except Exception as e:
            job.status = JobStatus.FAILED
            job.progress.stage = "Failed"
            job.error = str(e)
        finally:
            job.progress.finished_at = datetime.now(timezone.utc)
            job.progress.duration_seconds = time.time() - start_time
            self.repo.save(job)
            if job_id in self.active_tasks:
                del self.active_tasks[job_id]

    async def worker_loop(self):
        while True:
            job_id = await self.queue.get()
            # Start execution task
            task = asyncio.create_task(self._execute_job(job_id))
            self.active_tasks[job_id] = task
            self.queue.task_done()

# Singleton instance
worker_manager = WorkerManager()
"""
with open("backend/app/services/job/worker.py", "w") as f:
    f.write(worker_py)

# 4. Endpoints
jobs_endpoints = """from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from app.schemas.job import SearchJob
from app.schemas.search import SearchRequest
from app.services.job.worker import worker_manager

router = APIRouter()

@router.post("/jobs", response_model=SearchJob)
async def create_job(request: SearchRequest):
    return await worker_manager.create_job(request)

@router.get("/jobs", response_model=List[SearchJob])
async def get_all_jobs():
    return worker_manager.repo.get_all()

@router.get("/jobs/{job_id}", response_model=SearchJob)
async def get_job(job_id: str):
    job = worker_manager.repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    if not await worker_manager.cancel_job(job_id):
        raise HTTPException(status_code=400, detail="Cannot cancel job")
    return {"status": "cancelled"}

@router.post("/jobs/{job_id}/retry")
async def retry_job(job_id: str):
    if not await worker_manager.retry_job(job_id):
        raise HTTPException(status_code=400, detail="Cannot retry job")
    return {"status": "retrying"}
"""
with open("backend/app/api/v1/endpoints/jobs.py", "w") as f:
    f.write(jobs_endpoints)

# 5. Modify main.py
with open("backend/app/main.py", "r") as f:
    main_content = f.read()

if "from app.api.v1.endpoints import jobs" not in main_content:
    main_content = main_content.replace(
        "from app.api.v1.endpoints import history",
        "from app.api.v1.endpoints import history\nfrom app.api.v1.endpoints import jobs"
    )
    main_content = main_content.replace(
        'api_router.include_router(history.router, prefix="/history", tags=["history"])',
        'api_router.include_router(history.router, prefix="/history", tags=["history"])\napi_router.include_router(jobs.router, prefix="/search", tags=["search-jobs"])'
    )
    
    # Add worker startup
    import_worker = "from app.services.job.worker import worker_manager\nimport asyncio\n"
    startup_hook = """
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker_manager.worker_loop())
"""
    if "from fastapi import FastAPI" in main_content:
        main_content = main_content.replace("from fastapi import FastAPI", "from fastapi import FastAPI\n" + import_worker)
        main_content = main_content.replace("app.include_router(api_router, prefix=settings.API_V1_STR)", "app.include_router(api_router, prefix=settings.API_V1_STR)\n" + startup_hook)
    
    with open("backend/app/main.py", "w") as f:
        f.write(main_content)

print("Backend for TASK-016 generated successfully.")
