from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum as enum

if TYPE_CHECKING:

    from backend.infrastructure.models import Attorney
    from backend.infrastructure.models import Case

# Справочник типов событий
class EventType(str, enum):
    meeting = 'Встреча'           
    task = 'Задача'                
    deadline = 'Дедлайн'       
    court_hearing = 'Судебное заседание' 

class Event(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    event_type: str = Field(max_length=50)
    event_date: datetime

    case_id: int = Field(foreign_key='cases.id', index=True)
    attorney_id: int = Field(foreign_key='attorneys.id', index=True)

    # relationships
    case: Optional['Case'] = Relationship(back_populates='events')
    attorney: Optional['Attorney'] = Relationship(back_populates='events')



