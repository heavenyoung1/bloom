from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from backend.domain.entities.auxiliary import Messenger

# ====== COMMANDS (write операции) ======


@dataclass
class CreateClientCommand:
    name: str
    type: bool
    email: Optional[str]
    phone: str
    personal_info: str
    address: str
    messenger: Messenger
    messenger_handle: str
    owner_attorney_id: int  # из JWT


@dataclass
class UpdateClientCommand:
    client_id: int
    owner_attorney_id: int

    # PATCH — все поля опциональные
    name: Optional[str] = None
    type: Optional[bool] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    personal_info: Optional[str] = None
    address: Optional[str] = None
    messenger: Optional[Messenger] = None
    messenger_handle: Optional[str] = None


@dataclass
class DeleteClientCommand:
    client_id: int
    owner_attorney_id: int


# ====== QUERIES (read операции) ======


@dataclass
class GetClientByIdQuery:
    client_id: int
    owner_attorney_id: int


@dataclass
class GetClientsForAttorneyQuery:
    owner_attorney_id: int
    # если потом добавишь пагинацию/фильтры:
    # page: int = 1
    # page_size: int = 20
