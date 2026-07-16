import json
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
