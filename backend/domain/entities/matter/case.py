from dataclasses import dataclass
from datetime import datetime

@dataclass
class Case:
    id: int
    client_id: str
    attorney_id: str
    name: str
    status: str
    description: str
    created_at: datetime