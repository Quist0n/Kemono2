from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, unique

from typing import Dict, Optional
from src.internals.types import DatabaseEntry

@dataclass
class Notification(DatabaseEntry):
    id: int
    account_id: int
    type: str
    created_at: datetime
    extra_info: Optional[Dict]

@unique
class Notification_Types(IntEnum):
    ACCOUNT_ROLE_CHANGE = 1
