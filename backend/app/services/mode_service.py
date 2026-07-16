import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODE_FILE = DATA_DIR / "mode.json"

class ModeService:
    @staticmethod
    def _ensure_dir():
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_mode() -> str:
        if not MODE_FILE.exists():
            return "user"
        try:
            with open(MODE_FILE, "r") as f:
                data = json.load(f)
                return data.get("mode", "user")
        except Exception:
            return "user"

    @staticmethod
    def set_mode(mode: str) -> None:
        ModeService._ensure_dir()
        with open(MODE_FILE, "w") as f:
            json.dump({"mode": mode}, f)
