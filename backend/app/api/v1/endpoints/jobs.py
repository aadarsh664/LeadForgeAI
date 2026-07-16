from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.job import SearchJob
from app.schemas.search import SearchRequest
from app.services.job.repository import JobRepository
from app.services.job.worker import SearchWorker
from app.core.dependencies import get_job_repository, get_search_worker

router = APIRouter()

@router.post("", response_model=SearchJob)
async def create_job(request: SearchRequest, worker: SearchWorker = Depends(get_search_worker)):
    return await worker.enqueue_job(request, provider="mock")

@router.get("", response_model=List[SearchJob])
async def list_jobs(repo: JobRepository = Depends(get_job_repository)):
    return repo.get_all()

@router.get("/{job_id}", response_model=SearchJob)
async def get_job(job_id: str, repo: JobRepository = Depends(get_job_repository)):
    job = repo.get_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job

@router.post("/{job_id}/cancel", response_model=SearchJob)
async def cancel_job(job_id: str, worker: SearchWorker = Depends(get_search_worker)):
    try:
        return await worker.cancel_job(job_id)
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.post("/{job_id}/retry", response_model=SearchJob)
async def retry_job(job_id: str, worker: SearchWorker = Depends(get_search_worker)):
    try:
        return await worker.retry_job(job_id)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{job_id}/progress")
async def get_progress(job_id: str, repo: JobRepository = Depends(get_job_repository)):
    job = repo.get_by_id(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {
        "id": job.id,
        "state": job.state,
        "progress": job.progress,
        "result_count": len(job.results) if job.results else 0
    }
