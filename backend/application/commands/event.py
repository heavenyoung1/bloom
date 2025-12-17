from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from backend.domain.entities.auxiliary import EventType

from backend.domain.entities.auxiliary import CaseStatus

# ====== COMMANDS (write операции) ======


@dataclass
class CreateEventCommand:
    name: str
    description: str
    case_id: int
    attorney_id: int
    event_type: EventType
    event_date: datetime


@dataclass
class GetEventQuery:
    '''Получить одно событие по ID'''

    event_id: int


@dataclass
class UpdateEventCommand:
    #event_id: int
    #case_id: int
    name: Optional[str] = None
    description: Optional[str] = None

    # attorney_id: Optional[int] = None
    event_type: Optional[EventType] = None
    event_date: Optional[datetime] = None


@dataclass
class DeleteEventCommand:
    event_id: int


@dataclass
class GetEventsForAttorneyQuery:
    attorney_id: int


@dataclass
class GetEventsForCaseQuery:
    case_id: int
