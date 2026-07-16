from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.workspace import router as workspace_router
from app.api.routes.system import router as system_router

from app.api.v1.endpoints.search import router as search_router
from app.api.v1.endpoints.jobs import router as jobs_router
from app.api.v1.endpoints.history import router as history_router
from app.api.v1.endpoints.diagnostics import router as diagnostics_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(workspace_router)
api_router.include_router(system_router)

# V1 Endpoints
api_router.include_router(search_router, prefix="/api/v1/search", tags=["search"])
api_router.include_router(jobs_router, prefix="/api/v1/search", tags=["jobs"])
api_router.include_router(history_router, prefix="/api/v1/history", tags=["history"])
api_router.include_router(diagnostics_router, prefix="/api/v1/diagnostics", tags=["diagnostics"])
