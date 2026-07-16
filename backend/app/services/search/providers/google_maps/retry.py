import asyncio
from typing import Callable, Any, Awaitable
from .logger import ProviderLogger

class RetryManager:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    async def execute(self, func: Callable[[], Awaitable[Any]]) -> Any:
        attempt = 0
        while attempt <= self.max_retries:
            try:
                return await func()
            except Exception as e:
                attempt += 1
                if attempt > self.max_retries:
                    ProviderLogger.log_error(f"Max retries exceeded. Last error: {str(e)}")
                    raise e
                
                ProviderLogger.log_retry(attempt, str(e))
                await asyncio.sleep(self.backoff_factor ** attempt)
