from datetime import datetime, timezone
import pytest
from backend.domain.entities.event import Event
from backend.infrastructure.models.client import Messenger


# Фикстура для события
@pytest.fixture
def sample_event(persisted_case, persisted_attorney_id, fixed_now):
    '''Фикстура для дефолтного клиента.'''
    return Event(
        id=None,
        name='Судебное заседание',
        description='Продолжение суда, перенесенного в прошлый раз.',
        event_type='Суд',
        event_date=fixed_now,
        case_id=persisted_case,
        attorney_id=persisted_attorney_id,
    )


# Фикстура для события
@pytest.fixture
def sample_update_event(persisted_case, persisted_attorney_id, fixed_now):
    '''Фикстура для дефолтного клиента.'''
    return Event(
        id=None,
        name='Встреча с клиентом',
        description='',
        event_type='Встреча',
        event_date=fixed_now,
        case_id=persisted_case,
        attorney_id=persisted_attorney_id,
    )


# Фикстура для списка событий
@pytest.fixture
def sample_events(persisted_case, persisted_attorney_id, fixed_now):
    '''Фикстура для списка из 5 событий.'''
    events = []
    for i in range(5):
        event = Event(
            id=None,
            name=f'Судебное заседание {i+1}',
            description=f'Продолжение суда, перенесенного в прошлый раз. Заседание #{i+1}',
            event_type='Суд',
            event_date=fixed_now,
            case_id=persisted_case,
            attorney_id=persisted_attorney_id,
        )
        events.append(event)
    return events
