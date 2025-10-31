from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
import sqlalchemy as sa

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models import ClientORM, CaseORM, DocumentORM, EventORM


class AttorneyORM(SQLModel, table=True):
    __tablename__ = 'attorneys'  # Таблица Адвокат

    id: int = Field(primary_key=True)
    attorney_id: str = Field(max_length=50, unique=True)  # Номер удостоверения юриста
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    patronymic: Optional[str] = Field(max_length=50)
    email: str = Field(max_length=50, index=True, unique=True)  # валидацию делаем на уровне Pydantic DTO / сервисов
    phone: Optional[str] = Field(max_length=20)
    password_hash: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    # Отношения (1:N обратные стороны)
    clients: List['ClientORM'] = Relationship(
        back_populates='owner_attorney',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'},
    )
    cases: List['CaseORM'] = Relationship(
        back_populates='attorney',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'},
    )
    documents: List['DocumentORM'] = Relationship(
        back_populates='attorney',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'},
    )
    events: List['EventORM'] = Relationship(
        back_populates='attorney',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'},
    )
