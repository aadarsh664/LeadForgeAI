from enum import Enum
from pydantic import BaseModel
from typing import Optional

class HealthStatus(str, Enum):
    READY = "Ready"
    BUSY = "Busy"
    OFFLINE = "Offline"
    RATE_LIMITED = "Rate Limited"
    AUTH_REQUIRED = "Authentication Required"
    BLOCKED = "Blocked"
    UNKNOWN = "Unknown"

class ProviderHealth(BaseModel):
    status: HealthStatus = HealthStatus.UNKNOWN
    last_check: Optional[str] = None
    error_message: Optional[str] = None
