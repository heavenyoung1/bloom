from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    id: int
    name: str
    case_id: int
    client_id: int
    attorney_id: int
    event_type: str
    event_date: datetime
    description: str
    