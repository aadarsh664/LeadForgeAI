from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workspace import Workspace
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate


class WorkspaceService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = WorkspaceRepository(session)

    async def create_workspace(self, data: WorkspaceCreate) -> Workspace:
        existing = await self.repository.get_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Workspace with this name already exists.",
                    "error_code": "WORKSPACE_NAME_EXISTS",
                },
            )

        workspace = Workspace(
            name=data.name,
            description=data.description,
            status=data.status or "active",
        )
        return await self.repository.create(workspace)

    async def get_workspace(self, workspace_id: UUID) -> Workspace:
        workspace = await self.repository.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "message": "Workspace not found.",
                    "error_code": "WORKSPACE_NOT_FOUND",
                },
            )
        return workspace

    async def list_workspaces(self) -> Sequence[Workspace]:
        return await self.repository.list_all()

    async def update_workspace(
        self, workspace_id: UUID, data: WorkspaceUpdate
    ) -> Workspace:
        workspace = await self.get_workspace(workspace_id)

        if data.name is not None and data.name != workspace.name:
            existing = await self.repository.get_by_name(data.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "success": False,
                        "message": "Workspace with this name already exists.",
                        "error_code": "WORKSPACE_NAME_EXISTS",
                    },
                )
            workspace.name = data.name

        if data.description is not None:
            workspace.description = data.description
        if data.status is not None:
            workspace.status = data.status

        return await self.repository.update(workspace)

    async def delete_workspace(self, workspace_id: UUID) -> None:
        workspace = await self.get_workspace(workspace_id)
        await self.repository.delete(workspace)
