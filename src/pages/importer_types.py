from dataclasses import dataclass

from typing import Optional, List
from src.types.kemono import DM
@dataclass
class StatusPageProps:
    current_page: str
    import_id: str
    dms: Optional[List[DM]]

@dataclass
class DMPageProps:
    current_page: str
    import_id: str
    account_id: str
    dms: Optional[List[DM]]
