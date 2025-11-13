from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: int
    name: str
    description: str
    event_type: str
    event_date: datetime
    case_id: int
    attorney_id: int
