from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.schemas.history import SearchHistoryItem, SavedSearch
from app.schemas.search import SearchRequest
from app.services.history.service import HistoryService

router = APIRouter()
service = HistoryService()

class SaveSearchRequest(BaseModel):
    name: str
    request: SearchRequest

class UpdateSavedSearchRequest(BaseModel):
    name: str = None
    is_favorite: bool = None
    run: bool = False

@router.get("/history", response_model=List[SearchHistoryItem])
def get_history():
    return service.get_history()

@router.post("/history")
def clear_history():
    # In a real app we'd use DELETE /history, but keeping it simple
    service.clear_history()
    return {"status": "cleared"}

@router.delete("/history/{item_id}")
def delete_history_item(item_id: str):
    if not service.delete_history(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted"}

@router.get("/saved", response_model=List[SavedSearch])
def get_saved_searches():
    return service.get_saved_searches()

@router.post("/saved", response_model=SavedSearch)
def save_search(req: SaveSearchRequest):
    try:
        return service.save_search(req.name, req.request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/saved/{search_id}", response_model=SavedSearch)
def update_saved_search(search_id: str, req: UpdateSavedSearchRequest):
    try:
        updated = service.update_saved_search(search_id, name=req.name, is_favorite=req.is_favorite, run=req.run)
        if not updated:
            raise HTTPException(status_code=404, detail="Search not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/saved/{search_id}")
def delete_saved_search(search_id: str):
    if not service.delete_saved_search(search_id):
        raise HTTPException(status_code=404, detail="Search not found")
    return {"status": "deleted"}
