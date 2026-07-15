from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WorkspaceBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: Optional[str] = "active"


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None


class WorkspaceResponse(WorkspaceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorkspaceListResponse(BaseModel):
    success: bool
    data: list[WorkspaceResponse]


class WorkspaceSingleResponse(BaseModel):
    success: bool
    data: WorkspaceResponse
