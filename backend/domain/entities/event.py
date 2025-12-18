from backend.domain.entities.auxiliary import EventType
from backend.application.commands.event import UpdateEventCommand

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: int
    name: str
    description: str
    event_type: EventType
    event_date: datetime
    case_id: int
    attorney_id: int

    @staticmethod
    def create(
        *,
        name: str,
        description: str,
        event_type: EventType,
        event_date: datetime,
        case_id: int,
        attorney_id: int,
    ) -> 'Event':
        return Event(
            id=None,
            name=name,
            description=description,
            event_type=event_type,
            event_date=event_date,
            case_id=case_id,
            attorney_id=attorney_id,
        )

    @staticmethod
    def update(self, cmd: UpdateEventCommand) -> None:
        if cmd.name is not None:
            self.name = cmd.name
        if cmd.description is not None:
            self.description = cmd.description
        if cmd.event_type is not None:
            self.event_type = cmd.event_type
        if cmd.event_date is not None:
            self.event_date = cmd.event_date
        if cmd.case_id is not None:
            self.case_id = cmd.case_id
