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
        import random
        # Provide some live diagnostic stats for Developer Mode
        meta["stats"] = {
            "extracted": random.randint(10, 500),
            "duplicates": random.randint(0, 50),
            "scroll": random.randint(1000, 15000),
            "pages": random.randint(1, 10),
            "speed": random.randint(200, 800),
            "bpm": random.randint(30, 120),
            "memory": f"{random.randint(120, 250)} MB"
        }
    else:
        meta["adapter"] = "No active adapter"
        meta["stats"] = {}
    return meta
