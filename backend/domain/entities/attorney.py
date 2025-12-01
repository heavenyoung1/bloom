from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Attorney:
    id: int
    license_id: str
    first_name: str
    last_name: str
    patronymic: str
    email: str  # Как валидировать email
    phone: str
    hashed_password: str
    is_active: bool  # Можно ли юзеру логиниться
    is_superuser: bool  # Админ?
    is_verified: bool  # Подтвердил ли email

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
