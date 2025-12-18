import pytest
from backend.domain.entities.event import Event
from backend.core.logger import logger

from backend.core.exceptions import (
    EntityNotFoundException,
    DatabaseErrorException,
)


class TestEventRepository:
    # ========== SAVE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_save_event_success(self, event_repo, sample_event):
        '''Тест: Сохранение дела со связанными клиентом и адвокатом.'''
        event = await event_repo.save(sample_event)

        assert isinstance(event, Event)
        assert event.id is not None

        assert event.case_id == sample_event.case_id
        assert event.attorney_id == sample_event.attorney_id
        assert event.name == sample_event.name
        assert event.description == sample_event.description
        assert event.event_type == sample_event.event_type
        assert event.event_date == sample_event.event_date

    # ========== GET SUCCESS ==========
    @pytest.mark.asyncio
    async def test_get_success(self, event_repo, sample_event):
        saved_event = await event_repo.save(sample_event)
        assert isinstance(saved_event, Event)
        assert saved_event.id is not None

        got_event = await event_repo.get(saved_event.id)
        assert got_event is not None

        assert got_event.id == saved_event.id
        assert got_event.case_id == sample_event.case_id
        assert got_event.attorney_id == sample_event.attorney_id
        assert got_event.name == sample_event.name
        assert got_event.event_type == sample_event.event_type
        assert got_event.event_date == sample_event.event_date

    # ========== GET NOT FOUND ==========
    @pytest.mark.asyncio
    async def test_get_not_found_returns_none(self, event_repo):
        got_event = await event_repo.get(999999999)
        assert got_event is None

    # ========== GET FOR CASE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_get_for_case_success(
        self, event_repo, sample_events, persisted_case
    ):
        # persisted_case = id дела
        for e in sample_events:
            await event_repo.save(e)

        events = await event_repo.get_for_case(persisted_case)

        assert isinstance(events, list)
        assert len(events) == len(sample_events)
        for e in events:
            assert isinstance(e, Event)
            assert e.case_id == persisted_case

    # ========== GET ALL FOR ATTORNEY SUCCESS ==========
    @pytest.mark.asyncio
    async def test_get_all_for_attorney_success(
        self,
        event_repo,
        sample_events,
        persisted_attorney_id,
    ):
        for e in sample_events:
            await event_repo.save(e)

        events = await event_repo.get_all_for_attorney(persisted_attorney_id)

        assert isinstance(events, list)
        assert len(events) == len(sample_events)
        for e in events:
            assert isinstance(e, Event)
            assert e.attorney_id == persisted_attorney_id

    # ========== UPDATE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_update_success(self, event_repo, sample_event, sample_update_event):
        saved_event = await event_repo.save(sample_event)
        assert isinstance(saved_event, Event)
        assert saved_event.id is not None

        # До изменения
        assert saved_event.name == sample_event.name
        assert saved_event.description == sample_event.description
        assert saved_event.event_type == sample_event.event_type
        assert saved_event.event_date == sample_event.event_date

        # Проставляем ID
        sample_update_event.id = saved_event.id

        updated = await event_repo.update(sample_update_event)
        assert isinstance(updated, Event)
        assert updated.id == saved_event.id

        # После изменения
        assert updated.name == sample_update_event.name
        assert updated.description == sample_update_event.description
        assert updated.event_type == sample_update_event.event_type
        assert updated.event_date == sample_update_event.event_date

    # ========== DELETE SUCCESS ==========
    @pytest.mark.asyncio
    async def test_delete_success(self, event_repo, sample_event):
        saved_event = await event_repo.save(sample_event)
        assert saved_event.id is not None

        deleted = await event_repo.delete(saved_event.id)
        assert deleted is True

        check = await event_repo.get(saved_event.id)
        assert check is None

    # ========== DELETE NOT FOUND ==========
    @pytest.mark.asyncio
    async def test_delete_not_found_raises(self, event_repo):
        with pytest.raises(EntityNotFoundException) as exc_info:
            await event_repo.delete(999999999)

        assert 'не найдено' in str(exc_info.value).lower()

    # ========== UPDATE NOT FOUND ==========
    @pytest.mark.asyncio
    async def test_update_not_found_raises(self, event_repo, sample_update_event):
        sample_update_event.id = 999999999

        with pytest.raises(EntityNotFoundException) as exc_info:
            await event_repo.update(sample_update_event)

        assert 'не найдено' in str(exc_info.value).lower()
