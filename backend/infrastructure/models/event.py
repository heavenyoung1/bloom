from __future__ import annotations
from datetime import datetime
from enum import Enum
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM, CaseORM


class EventType(str, Enum):
    '''Типы событий'''

    meeting = 'Встреча'
    task = 'Задача'
    court_hearing = 'Судебное заседание'
    deadline = 'Дедлайн'
    important = 'Важное'
    other = 'Другое'


class EventORM(TimeStampMixin, Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000))
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    case_id: Mapped[int] = mapped_column(
        ForeignKey('cases.id', ondelete='CASCADE'), nullable=False, index=True
    )
    attorney_id: Mapped[int] = mapped_column(
        ForeignKey('attorneys.id', ondelete='RESTRICT'), nullable=False, index=True
    )

    case: Mapped['CaseORM'] = relationship(back_populates='events')
    attorney: Mapped['AttorneyORM'] = relationship(back_populates='events')
