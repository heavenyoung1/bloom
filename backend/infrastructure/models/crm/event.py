from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum as enum

if TYPE_CHECKING:

    from backend.infrastructure.models.crm import Client

# Справочник типов событий
class EventType(str, enum):
    meeting = 'Встреча'           
    task = 'Задача'                
    deadline = 'Дедлайн'       
    court_hearing = 'Судебное заседание' 

class Event(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    case_id: Optional[int] = Field(default=None, foreign_key='cases.id', index=True)
    client_id: Optional[int] = Field(default=None, foreign_key='clients.id', index=True)
    attorney_id: Optional[int] = Field(default=None, foreign_key='attorneys.id', index=True)
    
    event_type: EventType = Field(sa_column_kwargs={'nullable': False})
    event_date: datetime = Field(default_factory=datetime.now(tz=None)) # type: ignore
    description: str = Field(max_length=255)


