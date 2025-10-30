from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models import Subscription 
    from backend.infrastructure.models import Client
    from backend.infrastructure.models import Case, Document

class Attorney(SQLModel, table=True):
    'Таблица Адвокат'

    id: int = Field(primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    patronymic: Optional[str] = Field(max_length=50)
    email: str = Field(max_length=50, index=True)  # валидацию делаем на уровне Pydantic DTO / сервисов
    phone: Optional[str] = Field(max_length=20)
    password_hash: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # Отношения
    clients: List['Client'] = Relationship(back_populates='owner_attorney')
    cases: List['Case'] = Relationship(back_populates='attorney')
    documents: List['Document'] = Relationship(back_populates='attorney')
    subscriptions: List['Subscription'] = Relationship(back_populates='attorney')