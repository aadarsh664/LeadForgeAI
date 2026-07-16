import json
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from app.schemas.job import SearchJob, JobState, JobProgress

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
        return [SearchJob(**j) for j in self._read_file()]

    def get_by_id(self, job_id: str) -> Optional[SearchJob]:
        for j in self._read_file():
            if j.get("id") == job_id:
                return SearchJob(**j)
        return None

    def save(self, job: SearchJob) -> SearchJob:
        jobs = self._read_file()
        job.updated_at = datetime.now(timezone.utc)
        
        # update if exists
        updated = False
        for i, j in enumerate(jobs):
            if j.get("id") == job.id:
                jobs[i] = job.model_dump(mode='json')
                updated = True
                break
        
        if not updated:
            jobs.insert(0, job.model_dump(mode='json'))
            
        self._write_file(jobs)
        return job
