from app.core.session import async_session_factory
from app.schemas.system import StartupStatusResponse
from app.services.health_service import HealthService
from app.services.workspace_service import WorkspaceService

class StartupStateManager:
    _state = StartupStatusResponse(
        current_step="idle",
        completed_steps=[],
        progress_percentage=0,
        overall_status="idle",
        is_ready=False,
        message="Ready to start."
    )

    @classmethod
    def get_state(cls) -> StartupStatusResponse:
        return cls._state

    @classmethod
    def update_state(cls, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(cls._state, k, v)

    @classmethod
    def reset(cls) -> None:
        cls._state = StartupStatusResponse(
            current_step="idle",
            completed_steps=[],
            progress_percentage=0,
            overall_status="idle",
            is_ready=False,
            message="Ready to start."
        )

class StartupService:
    @staticmethod
    async def run_startup_sequence() -> None:
        StartupStateManager.reset()
        StartupStateManager.update_state(
            overall_status="running", 
            current_step="Backend", 
            message="Verifying Backend..."
        )
        
        # Step 1: Backend
        backend_health = await HealthService.get_backend_health()
        if not backend_health.success:
            StartupStateManager.update_state(overall_status="failed", message="Backend verification failed.")
            return
            
        StartupStateManager.update_state(
            completed_steps=["Backend"], 
            progress_percentage=20, 
            current_step="Database", 
            message="Verifying Database..."
        )

        # Step 2: Database
        db_health = await HealthService.get_database_health()
        if not db_health.success:
            StartupStateManager.update_state(overall_status="failed", message=f"Database verification failed: {db_health.message}")
            return
            
        StartupStateManager.update_state(
            completed_steps=["Backend", "Database"], 
            progress_percentage=40, 
            current_step="Docker", 
            message="Verifying Docker..."
        )

        # Step 3: Docker
        docker_health = await HealthService.get_docker_health()
        if not docker_health.success:
            StartupStateManager.update_state(overall_status="failed", message=f"Docker verification failed: {docker_health.message}")
            return
            
        StartupStateManager.update_state(
            completed_steps=["Backend", "Database", "Docker"], 
            progress_percentage=60, 
            current_step="n8n", 
            message="Verifying n8n..."
        )

        # Step 4: n8n
        n8n_health = await HealthService.get_n8n_health()
        if not n8n_health.success:
            StartupStateManager.update_state(overall_status="failed", message=f"n8n verification failed: {n8n_health.message}")
            return
            
        StartupStateManager.update_state(
            completed_steps=["Backend", "Database", "Docker", "n8n"], 
            progress_percentage=80, 
            current_step="Workspace", 
            message="Verifying Workspace..."
        )

        # Step 5: Workspace
        try:
            async with async_session_factory() as session:
                workspace_service = WorkspaceService(session)
                await workspace_service.list_workspaces()
                
            StartupStateManager.update_state(
                completed_steps=["Backend", "Database", "Docker", "n8n", "Workspace"], 
                progress_percentage=100, 
                current_step="Ready", 
                overall_status="success", 
                is_ready=True, 
                message="LeadForgeAI is Ready"
            )
        except Exception as e:
            StartupStateManager.update_state(overall_status="failed", message=f"Workspace verification failed: {str(e)}")
            return
