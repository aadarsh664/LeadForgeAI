from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_database_session
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceListResponse,
    WorkspaceSingleResponse,
    WorkspaceUpdate,
)
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/api/v1/workspaces", tags=["workspaces"])


@router.post(
    "",
    response_model=WorkspaceSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    data: WorkspaceCreate,
    db: AsyncSession = Depends(get_database_session),
) -> Any:
    service = WorkspaceService(db)
    workspace = await service.create_workspace(data)
    return {"success": True, "data": workspace}


@router.get("", response_model=WorkspaceListResponse)
async def list_workspaces(
    db: AsyncSession = Depends(get_database_session),
) -> Any:
    service = WorkspaceService(db)
    workspaces = await service.list_workspaces()
    return {"success": True, "data": workspaces}


@router.get("/{workspace_id}", response_model=WorkspaceSingleResponse)
async def get_workspace(
    workspace_id: UUID,
    db: AsyncSession = Depends(get_database_session),
) -> Any:
    service = WorkspaceService(db)
    workspace = await service.get_workspace(workspace_id)
    return {"success": True, "data": workspace}


@router.patch("/{workspace_id}", response_model=WorkspaceSingleResponse)
async def update_workspace(
    workspace_id: UUID,
    data: WorkspaceUpdate,
    db: AsyncSession = Depends(get_database_session),
) -> Any:
    service = WorkspaceService(db)
    workspace = await service.update_workspace(workspace_id, data)
    return {"success": True, "data": workspace}


@router.delete("/{workspace_id}", status_code=status.HTTP_200_OK)
async def delete_workspace(
    workspace_id: UUID,
    db: AsyncSession = Depends(get_database_session),
) -> Any:
    service = WorkspaceService(db)
    await service.delete_workspace(workspace_id)
    return {"success": True, "message": "Workspace deleted successfully."}
