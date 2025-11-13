from datetime import datetime

from backend.domain.entities.event import Event
from backend.infrastructure.models.event import EventType


class EventFactory:
    '''Фабрика для создания Event'''

    @staticmethod
    def create(
        *,
        name: str,
        description: str,
        event_type: EventType,
        event_date: datetime,
        case_id: int,
        attorney_id: int,
    ) -> Event:
        '''Создать новый объект Event'''
        return Event(
            id=None,
            name=name,
            description=description,
            event_type=event_type,
            event_date=event_date,
            case_id=case_id,
            attorney_id=attorney_id,
        )
