from fastapi import APIRouter, BackgroundTasks
from app.schemas.system import StartupStatusResponse, ModeResponse, ModeRequest
from app.services.startup_service import StartupService, StartupStateManager
from app.services.mode_service import ModeService

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

@router.get("/mode", response_model=ModeResponse)
async def get_mode() -> ModeResponse:
    return ModeResponse(mode=ModeService.get_mode())

@router.patch("/mode", response_model=ModeResponse)
async def update_mode(request: ModeRequest) -> ModeResponse:
    if request.mode not in ["user", "developer"]:
        request.mode = "user"
    ModeService.set_mode(request.mode)
    return ModeResponse(mode=request.mode)
