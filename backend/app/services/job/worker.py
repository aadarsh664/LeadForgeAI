import asyncio
import time
from datetime import datetime, timezone
from app.schemas.job import SearchJob, JobState
from app.services.job.repository import JobRepository
from app.services.search.engine import SearchEngine
from app.schemas.search import SearchRequest
from app.services.search.exceptions import ProviderExecutionError
import uuid

class SearchWorker:
    def __init__(self, repository: JobRepository, search_engine: SearchEngine):
        self.repository = repository
        self.search_engine = search_engine
        self.queue = asyncio.Queue()
        self.active_jobs = {} # job_id -> task
        self.is_running = False
        self._worker_task = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._worker_task = asyncio.create_task(self._process_queue())

    def stop(self):
        self.is_running = False
        if self._worker_task:
            self._worker_task.cancel()

    async def enqueue_job(self, request: SearchRequest, provider: str = "mock") -> SearchJob:
        job = SearchJob(
            id=str(uuid.uuid4()),
            state=JobState.QUEUED,
            request=request,
            provider=provider,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.repository.save(job)
        await self.queue.put(job.id)
        return job

    async def cancel_job(self, job_id: str):
        job = self.repository.get_by_id(job_id)
        if not job:
            raise ValueError("Job not found")
        
        if job.state in [JobState.COMPLETED, JobState.FAILED, JobState.CANCELLED]:
            return job # Already finished
            
        job.state = JobState.CANCELLED
        job.progress.stage = "Cancelled by user"
        job.progress.finished_at = datetime.now(timezone.utc)
        self.repository.save(job)
        
        if job_id in self.active_jobs:
            self.active_jobs[job_id].cancel()
        
        return job

    async def retry_job(self, job_id: str):
        job = self.repository.get_by_id(job_id)
        if not job:
            raise ValueError("Job not found")
        
        if job.retries >= job.max_retries:
            raise ValueError("Max retries reached")
            
        job.state = JobState.RETRYING
        job.retries += 1
        job.progress.stage = f"Retrying ({job.retries}/{job.max_retries})"
        job.progress.logs.append(f"Retry {job.retries} initiated.")
        self.repository.save(job)
        
        await self.queue.put(job.id)
        return job

    async def _process_queue(self):
        while self.is_running:
            try:
                job_id = await self.queue.get()
                
                job = self.repository.get_by_id(job_id)
                if not job or job.state == JobState.CANCELLED:
                    self.queue.task_done()
                    continue
                
                # Execute in background task so we don't block the queue completely
                # Wait, if we want single concurrency, we await here.
                # Let's await for FIFO strictness.
                
                task = asyncio.create_task(self._execute_job(job))
                self.active_jobs[job_id] = task
                
                try:
                    await task
                except asyncio.CancelledError:
                    pass # Handled in cancel_job
                finally:
                    if job_id in self.active_jobs:
                        del self.active_jobs[job_id]
                    self.queue.task_done()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Worker queue error: {e}")
                await asyncio.sleep(1)

    async def _execute_job(self, job: SearchJob):
        job.state = JobState.RUNNING
        job.progress.started_at = datetime.now(timezone.utc)
        job.progress.stage = "Initializing Provider"
        job.progress.percent = 5
        job.progress.logs.append("Job started.")
        self.repository.save(job)
        
        start_time = time.time()
        
        try:
            # We bypass the SearchPipeline here and implement chunked execution directly to update progress
            # Wait, SearchEngine has run_search, but run_search is monolithic.
            # Let's use the provider directly for background updates.
            provider = self.search_engine.registry.get_provider(job.provider)
            await provider.initialize()
            
            job.progress.percent = 20
            job.progress.stage = "Searching"
            job.progress.logs.append("Provider initialized, searching...")
            self.repository.save(job)
            
            all_results = []
            async for raw_batch in provider.search(job.request):
                # Check for cancellation
                if self.repository.get_by_id(job.id).state == JobState.CANCELLED:
                    raise asyncio.CancelledError()
                    
                normalized_batch = self.search_engine.registry.get_default_provider()._normalize_batch(raw_batch, job.provider) if hasattr(provider, '_normalize_batch') else [
                    # If normalizer is decoupled, use it. But in our arch, normalizer is separate.
                    # Let's import normalizer.
                ]
                
                from app.services.search.normalizer import SearchNormalizer
                normalizer = SearchNormalizer()
                normalized_batch = normalizer.normalize_batch(raw_batch, job.provider)
                
                all_results.extend(normalized_batch)
                job.progress.processed_count = len(all_results)
                job.progress.percent = min(90, 20 + len(all_results))
                job.progress.logs.append(f"Fetched {len(raw_batch)} results.")
                
                # To simulate longer searches and check cancellation
                await asyncio.sleep(1) 
                self.repository.save(job)
            
            job.results = all_results
            job.progress.percent = 100
            job.progress.stage = "Completed"
            job.progress.logs.append(f"Completed with {len(all_results)} results.")
            job.state = JobState.COMPLETED
            
        except asyncio.CancelledError:
            # Already set in cancel_job
            pass
        except Exception as e:
            job.state = JobState.FAILED
            job.error = str(e)
            job.progress.stage = "Failed"
            job.progress.logs.append(f"Error: {str(e)}")
        finally:
            if job.state != JobState.CANCELLED:
                job.progress.finished_at = datetime.now(timezone.utc)
                job.progress.duration = time.time() - start_time
                self.repository.save(job)
