from pydantic import BaseModel
from typing import Optional, Dict

class ProviderConfig(BaseModel):
    country: str = "US"
    language: str = "en"
    search_delay: float = 2.0
    concurrency: int = 1
    timeout: int = 30
    retries: int = 3
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    headless_mode: bool = True
    proxy: Optional[str] = None
    cookies: Optional[Dict[str, str]] = None
    rate_limit_rpm: int = 60
