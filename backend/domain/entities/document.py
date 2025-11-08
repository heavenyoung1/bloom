from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    id: int
    file_name: str
    storage_path: str
    file_size: str
    client_id: int
    case_id: int
    attorney: int

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
