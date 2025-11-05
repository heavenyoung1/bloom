from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
import sqlalchemy as sa


if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM, CaseORM


class Messenger(str, Enum):
    TG = 'Telegram'
    WA = 'WhatsApp'
    MA = 'MAX'


class ClientORM(SQLModel, table=True):
    __tablename__ = 'clients'  # Таблица 'Клиенты'

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

    created_at: datetime | None = Field(
    sa_column=sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),   # ставит NOW() на INSERT
        nullable=False,
    ))

    owner_attorney_id: int = Field(foreign_key='attorneys.id', index=True)

    # Отношения
    owner_attorney: Optional['AttorneyORM'] = Relationship(back_populates='clients')
    cases: List['CaseORM'] = Relationship(back_populates='client')
