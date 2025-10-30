from backend.domain.entities.event import Event
from backend.infrastructure.models import EventORM


class EventMapper:
    @staticmethod
    def to_domain(orm: EventORM) -> 'Event':
        '''Конвертация ORM модели события в доменную сущность.'''
        return Event(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            event_type=orm.event_type,
            event_date=orm.event_date,
            case_id=orm.case_id,
            attorney_id=orm.attorney_id,
        )

    @staticmethod
    def to_orm(domain: 'Event') -> EventORM:
        '''Конвертация доменной сущности события в ORM модель.'''
        return EventORM(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            event_type=domain.event_type,
            event_date=domain.event_date,
            case_id=domain.case_id,
            attorney_id=domain.attorney_id,
        )
