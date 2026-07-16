from fastapi import APIRouter, HTTPException, BackgroundTasks
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
