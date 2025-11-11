from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    id: int
    file_name: str
    storage_path: str
    file_size: str
    case_id: int
    attorney_id: int
    description: str

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
