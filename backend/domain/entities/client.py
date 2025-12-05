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
    owner_attorney_id: int

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        name: str,
        type: bool,
        email: str | None,
        phone: str,
        personal_info: str,
        address: str,
        messenger: Messenger,
        messenger_handle: str,
        owner_attorney_id: int,
    ) -> 'Client':
        '''Factory method для создания нового клиента'''
        return Client(
            id=None,
            name=name,
            type=type,
            email=email,
            phone=phone,
            personal_info=personal_info,
            address=address,
            messenger=messenger,
            messenger_handle=messenger_handle,
            owner_attorney_id=owner_attorney_id,
        )
