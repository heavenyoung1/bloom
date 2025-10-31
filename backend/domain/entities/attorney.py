from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Attorney:
    id: str
    attorney_id: str
    first_name: str
    last_name: str
    patronymic: str
    email: str  # Как валидировать email
    phone: str
    password_hash: str
    is_active: bool

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
