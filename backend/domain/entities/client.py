from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.infrastructure.models.client import Messenger


@dataclass
class Client:
    id: int
    name: str
    type: bool
    email: str
    phone: str
    personal_info: str  # ИНН/ПАСПОРТ
    address: str
    messenger: Messenger
    messenger_handle: str
    owner_attorney_id: str

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
