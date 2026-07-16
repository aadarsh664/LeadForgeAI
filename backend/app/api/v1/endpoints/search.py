from fastapi import APIRouter, Depends
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search.engine import SearchEngine
from app.core.dependencies import get_search_engine

router = APIRouter()

@router.post("/businesses", response_model=SearchResponse)
async def search_businesses(
    request: SearchRequest,
    engine: SearchEngine = Depends(get_search_engine)
):
    # Always use mock provider for now
    return await engine.run_search(request, provider_name="mock")
