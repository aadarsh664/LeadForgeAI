from fastapi import APIRouter, BackgroundTasks
from app.schemas.system import StartupStatusResponse
from app.services.startup_service import StartupService, StartupStateManager

router = APIRouter(prefix="/api/v1/system", tags=["system"])

@router.post("/startup")
async def trigger_startup(background_tasks: BackgroundTasks) -> dict:
    state = StartupStateManager.get_state()
    if state.overall_status == "running":
        return {"success": False, "message": "Startup is already running."}
        
    background_tasks.add_task(StartupService.run_startup_sequence)
    return {"success": True, "message": "Startup sequence initiated."}

@router.get("/startup/status", response_model=StartupStatusResponse)
async def get_startup_status() -> StartupStatusResponse:
    return StartupStateManager.get_state()
