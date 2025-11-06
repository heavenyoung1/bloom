from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Contact:
    id: int
    name: str
    personal_info: str  # ИНН/ПАСПОРТ
    phone: str
    email: str
    case_id: str

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
