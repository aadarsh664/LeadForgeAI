from fastapi import APIRouter, Depends
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search.engine import SearchEngine
from app.core.dependencies import get_search_engine
from app.services.history.service import HistoryService

router = APIRouter()

@router.post("/businesses", response_model=SearchResponse)
async def search_businesses(
    request: SearchRequest,
    engine: SearchEngine = Depends(get_search_engine)
):
    # Always use mock provider for now
    response = await engine.run_search(request, provider_name="mock")
    
    # Log to history
    try:
        history_svc = HistoryService()
        history_svc.add_history(request, provider="mock", result_count=response.result_count)
    except Exception as e:
        print("Failed to save history:", e)
        
    return response
