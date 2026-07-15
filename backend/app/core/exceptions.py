class DatabaseUnavailableError(Exception):
    """Raised when the application cannot reach PostgreSQL."""

    def __init__(self, payload: dict[str, str | bool]) -> None:
        super().__init__("Database is unavailable.")
        self.payload = payload
