from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.infrastructure.models.client import Messenger
from backend.application.commands.client import UpdateClientCommand


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

    def update(self, cmd: UpdateClientCommand) -> None:
        '''Обновить поля на основе команды, если они не None'''
        if cmd.name is not None:
            self.name = cmd.name
        if cmd.type is not None:
            self.type = cmd.type
        if cmd.email is not None:
            self.email = cmd.email
        if cmd.phone is not None:
            self.phone = cmd.phone
        if cmd.personal_info is not None:
            self.personal_info = cmd.personal_info
        if cmd.address is not None:
            self.address = cmd.address
        if cmd.messenger is not None:
            self.messenger = cmd.messenger
        if cmd.messenger_handle is not None:
            self.messenger_handle = cmd.messenger_handle
