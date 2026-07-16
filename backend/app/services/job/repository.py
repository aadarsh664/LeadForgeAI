import json
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
