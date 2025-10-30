from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum as enum


if TYPE_CHECKING:
    from backend.infrastructure.models import Contact
    from backend.infrastructure.models import Case, Document
    from backend.infrastructure.models import Attorney


class Mesenger(str, enum):
    tg = 'Telegram'
    wa = 'WhatsApp'
    ma = 'MAX'


class Client(SQLModel, table=True):

    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    type: bool = Field(description='True: Физ.лицо / False: Юр.лицо')
    email: Optional[str] = Field(max_length=50, index=True)
    phone: str = Field(max_length=20)
    personal_info: str = Field(
        default=None,
        description='ИНН для компании / Серия-Номер паспорта для человека',
        max_length=20,
    )
    address: Optional[str] = Field(default=None, max_length=255)
    messenger: Optional[str] = Field(default=None, description='Мессенджер клиента')
    messenger_handle: Optional[str] = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    owner_attorney_id: Optional[int] = Field(foreign_key="attorneys.id", index=True)

    # Отношения
    owner_attorney: Optional['Attorney'] = Relationship(back_populates="clients")
    cases: List['Case'] = Relationship(back_populates="client")
