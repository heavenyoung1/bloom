from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from backend.infrastructure.models.mixins import TimeStampMixin
from enum import Enum as enum

if TYPE_CHECKING:

    from backend.infrastructure.models import AttorneyORM, CaseORM


# Справочник типов событий
class EventType(str, enum):
    meeting = 'Встреча'
    task = 'Задача'
    deadline = 'Дедлайн'
    court_hearing = 'Судебное заседание'


class EventORM(SQLModel, TimeStampMixin, table=True):
    __tablename__ = 'events'  # Таблица 'События по делу'

    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    event_type: str = Field(max_length=50)
    event_date: datetime

    case_id: int = Field(foreign_key='cases.id', index=True)
    attorney_id: int = Field(foreign_key='attorneys.id', index=True)

    # relationships
    case: Optional['CaseORM'] = Relationship(back_populates='events')
    attorney: Optional['AttorneyORM'] = Relationship(back_populates='events')
