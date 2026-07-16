import os
import json

os.makedirs("backend/app/schemas", exist_ok=True)
os.makedirs("backend/app/services/history", exist_ok=True)
os.makedirs("backend/data", exist_ok=True)
os.makedirs("backend/app/api/v1/endpoints", exist_ok=True)

# 1. Schemas
history_schemas = """from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.schemas.search import SearchRequest

class SearchHistoryItem(BaseModel):
    id: str
    request: SearchRequest
    provider: str
    result_count: int
    created_at: datetime

class SavedSearch(BaseModel):
    id: str
    name: str
    request: SearchRequest
    is_favorite: bool = False
    created_at: datetime
    last_used: Optional[datetime] = None
"""
with open("backend/app/schemas/history.py", "w") as f:
    f.write(history_schemas)

# 2. Service
history_service = """import json
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from app.schemas.history import SearchHistoryItem, SavedSearch
from app.schemas.search import SearchRequest

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../../data")
os.makedirs(DATA_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
SAVED_FILE = os.path.join(DATA_DIR, "saved_searches.json")

class HistoryService:
    def _read_file(self, filepath: str) -> List[dict]:
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except:
            return []

    def _write_file(self, filepath: str, data: List[dict]):
        with open(filepath, "w") as f:
            json.dump(data, f, default=str, indent=2)

    # History
    def get_history(self) -> List[SearchHistoryItem]:
        data = self._read_file(HISTORY_FILE)
        return [SearchHistoryItem(**item) for item in data]

    def add_history(self, request: SearchRequest, provider: str, result_count: int) -> SearchHistoryItem:
        history = self._read_file(HISTORY_FILE)
        item = SearchHistoryItem(
            id=str(uuid.uuid4()),
            request=request,
            provider=provider,
            result_count=result_count,
            created_at=datetime.now(timezone.utc)
        )
        history.insert(0, item.model_dump(mode='json'))
        self._write_file(HISTORY_FILE, history)
        return item

    def delete_history(self, item_id: str) -> bool:
        history = self._read_file(HISTORY_FILE)
        initial_len = len(history)
        history = [h for h in history if h.get("id") != item_id]
        if len(history) < initial_len:
            self._write_file(HISTORY_FILE, history)
            return True
        return False

    def clear_history(self):
        self._write_file(HISTORY_FILE, [])

    # Saved Searches
    def get_saved_searches(self) -> List[SavedSearch]:
        data = self._read_file(SAVED_FILE)
        return [SavedSearch(**item) for item in data]

    def save_search(self, name: str, request: SearchRequest) -> SavedSearch:
        saved = self._read_file(SAVED_FILE)
        # check duplicate name
        if any(s.get("name") == name for s in saved):
            raise ValueError(f"A saved search with name '{name}' already exists.")
            
        item = SavedSearch(
            id=str(uuid.uuid4()),
            name=name,
            request=request,
            created_at=datetime.now(timezone.utc)
        )
        saved.insert(0, item.model_dump(mode='json'))
        self._write_file(SAVED_FILE, saved)
        return item

    def update_saved_search(self, search_id: str, name: Optional[str] = None, is_favorite: Optional[bool] = None, run: bool = False) -> Optional[SavedSearch]:
        saved = self._read_file(SAVED_FILE)
        for s in saved:
            if s.get("id") == search_id:
                if name is not None:
                    # check duplicate name
                    if any(other.get("name") == name and other.get("id") != search_id for other in saved):
                        raise ValueError(f"A saved search with name '{name}' already exists.")
                    s["name"] = name
                if is_favorite is not None:
                    s["is_favorite"] = is_favorite
                if run:
                    s["last_used"] = datetime.now(timezone.utc).isoformat()
                self._write_file(SAVED_FILE, saved)
                return SavedSearch(**s)
        return None

    def delete_saved_search(self, search_id: str) -> bool:
        saved = self._read_file(SAVED_FILE)
        initial_len = len(saved)
        saved = [s for s in saved if s.get("id") != search_id]
        if len(saved) < initial_len:
            self._write_file(SAVED_FILE, saved)
            return True
        return False
"""
with open("backend/app/services/history/service.py", "w") as f:
    f.write(history_service)

# 3. API
history_api = """from fastapi import APIRouter, HTTPException
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
"""
with open("backend/app/api/v1/endpoints/history.py", "w") as f:
    f.write(history_api)

# 4. Integrate to main.py and search endpoint
with open("backend/app/main.py", "r") as f:
    main_content = f.read()

if "from app.api.v1.endpoints import history" not in main_content:
    main_content = main_content.replace(
        "from app.api.v1.endpoints import search",
        "from app.api.v1.endpoints import search\nfrom app.api.v1.endpoints import history"
    )
    main_content = main_content.replace(
        'api_router.include_router(search.router, prefix="/search", tags=["search"])',
        'api_router.include_router(search.router, prefix="/search", tags=["search"])\napi_router.include_router(history.router, prefix="/history", tags=["history"])'
    )
    with open("backend/app/main.py", "w") as f:
        f.write(main_content)

search_endpoint_file = "backend/app/api/v1/endpoints/search.py"
with open(search_endpoint_file, "r") as f:
    search_content = f.read()

if "HistoryService" not in search_content:
    search_content = search_content.replace(
        "from app.core.dependencies import get_search_engine",
        "from app.core.dependencies import get_search_engine\nfrom app.services.history.service import HistoryService"
    )
    # Add history log inside search_businesses
    old_func = """    # Always use mock provider for now
    return await engine.run_search(request, provider_name="mock")"""
    
    new_func = """    # Always use mock provider for now
    response = await engine.run_search(request, provider_name="mock")
    
    # Log to history
    try:
        history_svc = HistoryService()
        history_svc.add_history(request, provider="mock", result_count=response.result_count)
    except Exception as e:
        print("Failed to save history:", e)
        
    return response"""
    
    search_content = search_content.replace(old_func, new_func)
    with open(search_endpoint_file, "w") as f:
        f.write(search_content)

print("Backend for TASK-015 generated successfully.")
