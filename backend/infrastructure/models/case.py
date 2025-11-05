from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING
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


class CaseORM(TimeStampMixin, Base):
    __tablename__ = 'cases'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False, index=True)
    attorney_id: Mapped[int] = mapped_column(ForeignKey('attorneys.id', ondelete='RESTRICT'), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))

    attorney: Mapped['AttorneyORM'] = relationship(back_populates='cases')
    client: Mapped['ClientORM'] = relationship(back_populates='cases')

    contacts: Mapped[list['ContactORM']] = relationship(back_populates='case', cascade='all, delete-orphan')
    documents: Mapped[list['DocumentORM']] = relationship(back_populates='case', cascade='all, delete-orphan')
    events: Mapped[list['EventORM']] = relationship(back_populates='case', cascade='all, delete-orphan')
