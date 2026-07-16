from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class SearchFilters(BaseModel):
    has_website: bool = False
    has_email: bool = False
    has_phone: bool = False
    min_rating: Optional[float] = None
    min_reviews: Optional[int] = None
    open_now: bool = False
    verified: bool = False
    hide_closed: bool = False

class SearchRequest(BaseModel):
    category: str = Field(..., description="Business category to search for")
    location: str = Field(..., description="Location to search in")
    keywords: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    radius: Optional[int] = Field(10, description="Radius in km")
    max_results: Optional[int] = Field(500, description="Maximum number of results to fetch")
    language: Optional[str] = Field("en", description="Language code")
    filters: Optional[SearchFilters] = None

class NormalizedBusiness(BaseModel):
    business_id: str
    name: str
    category: str
    rating: Optional[float] = None
    reviews: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_open: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_closed: Optional[bool] = None
    provider_source: str
    discovery_date: datetime
    raw_data: Dict[str, Any]

class SearchResponse(BaseModel):
    search_id: str
    status: str
    progress: int
    provider: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    result_count: int = 0
    duration: Optional[float] = None
    results: List[NormalizedBusiness] = []
    error: Optional[str] = None
