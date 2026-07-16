import asyncio
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
        
    async def create_job(self, request: SearchRequest, provider: str = "google_maps") -> SearchJob:
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
