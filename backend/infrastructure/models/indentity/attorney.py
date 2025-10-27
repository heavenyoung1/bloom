from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models.billing import Subscription 
    from backend.infrastructure.models.crm import Client
    from backend.infrastructure.models.matter import Case, Document

class Attorney(SQLModel, table=True):
    'Таблица Юрист'

    id: int = Field(primary_key=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    patronymic: Optional[str] = Field(max_length=100)
    email: str = Field(max_length=100, index=True)  # валидацию делаем на уровне Pydantic DTO / сервисов
    phone: Optional[str] = Field(max_length=50)
    password_hash: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now(tz=None)) # type: ignore
    updated_at: datetime = Field(default_factory=datetime.now(tz=None)) # type: ignore

    # relations
    clients: List['Client'] = Relationship(back_populates='owner_attorney')
    cases: List['Case'] = Relationship(back_populates='attorney')
    documents: List['Document'] = Relationship(back_populates='attorney')
    subscriptions: List['Subscription'] = Relationship(back_populates='attorney')