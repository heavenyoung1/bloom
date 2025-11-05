from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from backend.infrastructure.models import (
        AttorneyORM,
        ClientORM,
        ContactORM,
        DocumentORM,
        EventORM,
    )

class CaseStatus(str, Enum):
    '''Перечисление возможных статусов дела.'''

    NEW = 'Новое'                     # Дело только создано, в работу ещё не принято
    IN_PROGRESS = 'В работе'          # Адвокат/юрист ведёт дело
    ON_HOLD = 'На паузе'              # Временная приостановка (ожидание клиента, документов и т.п.)
    COMPLETED = 'Завершено'           # Успешно завершено
    CLOSED = 'Закрыто'                # Закрыто без результата (например, по инициативе клиента)
    CANCELLED = 'Отменено'            # Отменено до начала работы
    ARCHIVED = 'Архивировано'         # Перемещено в архив (историческое дело)


class CaseORM(SQLModel, table=True):
    __tablename__ = 'cases'  # Таблица 'Дела'

    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    client_id: int = Field(foreign_key='clients.id', index=True)
    attorney_id: int = Field(default=None, foreign_key='attorneys.id', index=True)
    status: str = Field(max_length=50, description='Статус делопроизводства')
    description: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # отношения
    attorney: 'AttorneyORM' = Relationship(back_populates='cases')
    client: 'ClientORM' = Relationship(back_populates='cases')

    contacts: List['ContactORM'] = Relationship(
        back_populates='case', sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
    documents: List['DocumentORM'] = Relationship(
        back_populates='case', sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
    events: List['EventORM'] = Relationship(
        back_populates='case', sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
