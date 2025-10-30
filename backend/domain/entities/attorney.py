from dataclasses import dataclass
from datetime import datetime

@dataclass
class Attorney:
    id: str
    first_name: str
    last_name: str
    patronymic: str
    email: str # Как валидировать email
    phone: str
    password_hash: str
    is_active: bool
    created_at: datetime
    updated_at: datetime