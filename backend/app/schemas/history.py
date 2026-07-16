from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.schemas.search import SearchRequest

class SearchHistoryItem(BaseModel):
    id: str
    request: SearchRequest
    provider: str
    result_count: int
    created_at: datetime

class SavedSearch(BaseModel):
    id: str
    name: str
    request: SearchRequest
    is_favorite: bool = False
    created_at: datetime
    last_used: Optional[datetime] = None
