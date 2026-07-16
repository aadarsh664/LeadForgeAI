from fastapi import APIRouter
from app.services.search.providers.google_maps.provider import GoogleMapsProvider
from app.services.search.providers.google_maps.config import ProviderConfig

router = APIRouter()

# Temporary mock instance just for diagnostics
temp_provider = GoogleMapsProvider()

@router.get("/diagnostics")
async def get_provider_diagnostics():
    return temp_provider.metadata()
