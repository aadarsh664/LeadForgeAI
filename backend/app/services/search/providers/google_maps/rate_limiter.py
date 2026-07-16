import time
import asyncio
from typing import Optional

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.interval = 60.0 / self.rpm if self.rpm > 0 else 0
        self.last_request: float = 0.0

    async def wait(self):
        if self.rpm <= 0:
            return
            
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.interval:
            wait_time = self.interval - elapsed
            await asyncio.sleep(wait_time)
            
        self.last_request = time.time()
