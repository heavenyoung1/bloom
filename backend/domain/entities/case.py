from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Case:
    id: int
    name: str
    client_id: str
    attorney_id: int
    status: str
    description: str

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
