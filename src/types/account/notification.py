from dataclasses import dataclass
from datetime import datetime

from typing import Dict
from src.internals.types import DatabaseEntry

@dataclass
class Notification(DatabaseEntry):
    id: int
    account_id: int
    type: str
    created_at: datetime
    extra_info: Dict
