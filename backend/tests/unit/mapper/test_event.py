import pytest
from backend.infrastructure.mappers.event_mapper import EventMapper
from backend.domain.entities.event import Event
from backend.infrastructure.models import EventORM

from datetime import datetime


class TestEventMapper:

    @pytest.fixture
    def sampleevent_domain(self, persisted_case, persisted_attorney_id):
        return Event(
            id=None,
            name='Судебное заседание',
            description='Продолжение суда, перенесённого в прошлый раз.',
            event_type='Суд',
            event_date=datetime(2023, 1, 15, 14, 0, 0),
            case_id=persisted_case,
            attorney_id=persisted_attorney_id,
        )

    @pytest.fixture
    def sampleevent_orm(self, persisted_case, persisted_attorney_id):
        return EventORM(
            id=None,
            name='Судебное заседание',
            description='Продолжение суда, перенесённого в прошлый раз.',
            event_type='Суд',
            event_date=datetime(2023, 1, 15, 14, 0, 0),
            case_id=persisted_case,
            attorney_id=persisted_attorney_id,
        )

    def test_to_orm(self, sampleevent_domain):
        orm = EventMapper.to_orm(sampleevent_domain)
        assert orm.id == sampleevent_domain.id
        assert orm.name == sampleevent_domain.name
        assert orm.description == sampleevent_domain.description
        assert orm.event_type == sampleevent_domain.event_type
        assert orm.event_date == sampleevent_domain.event_date
        assert orm.case_id == sampleevent_domain.case_id
        assert orm.attorney_id == sampleevent_domain.attorney_id

    def test_to_domain(self, sampleevent_orm):
        domain = EventMapper
