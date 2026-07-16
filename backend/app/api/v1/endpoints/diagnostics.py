from fastapi import APIRouter, Depends
from app.services.search.engine import SearchEngine
from app.core.dependencies import get_search_engine

router = APIRouter()

@router.get("/diagnostics")
async def get_provider_diagnostics(engine: SearchEngine = Depends(get_search_engine)):
    provider = engine.registry.get_provider("google_maps")
    meta = provider.metadata()
    if getattr(provider, "adapter", None):
        meta["adapter"] = "Connected"
    else:
        meta["adapter"] = "No active adapter"
    return meta
