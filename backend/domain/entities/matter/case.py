from dataclasses import dataclass
from datetime import datetime

@dataclass
class Case:
    id: int
    name: str
    client_id: str
    attorney_id: str
    status: str
    description: str
    created_at: datetime