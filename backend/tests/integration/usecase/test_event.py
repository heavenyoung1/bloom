import pytest
from datetime import datetime, timedelta, timezone
from backend.core.logger import logger

from backend.application.usecases.event.create import CreateEventUseCase
from backend.application.usecases.event.update import UpdateEventUseCase
from backend.application.usecases.event.get import (
    GetEventUseCase,
    GetEventByAttorneyUseCase,
    GetEventByCaseUseCase,
)
from backend.application.usecases.event.delete import DeleteEventUseCase

from backend.application.commands.event import (
    GetEventQuery,
    GetEventsForAttorneyQuery,
    GetEventsForCaseQuery,
    DeleteEventCommand,
)

from backend.core.exceptions import EntityNotFoundException


@pytest.mark.asyncio
async def test_create_event(test_uow_factory, create_event_command):
    use_case = CreateEventUseCase(test_uow_factory)
    result = await use_case.execute(create_event_command)

    assert result.id is not None
    assert result.case_id == create_event_command.case_id
    assert result.attorney_id == create_event_command.attorney_id
    assert result.event_date is not None


@pytest.mark.asyncio
async def test_update_event(
    test_uow_factory, create_event_command, update_event_command
):
    # create
    create_use_case = CreateEventUseCase(test_uow_factory)
    created = await create_use_case.execute(create_event_command)
    assert created.id is not None

    # update
    update_event_command.event_id = created.id
    update_use_case = UpdateEventUseCase(test_uow_factory)
    updated = await update_use_case.execute(update_event_command)

    assert updated.id == created.id
    assert updated.name == update_event_command.name
    assert updated.event_type == update_event_command.event_type


@pytest.mark.asyncio
async def test_get_event_by_id(test_uow_factory, create_event_command):
    # create
    create_use_case = CreateEventUseCase(test_uow_factory)
    created = await create_use_case.execute(create_event_command)
    assert created.id is not None

    # get
    cmd = GetEventQuery(event_id=created.id)
    get_use_case = GetEventUseCase(test_uow_factory)
    retrieved = await get_use_case.execute(cmd)

    assert retrieved is not None
    assert retrieved.id == created.id


@pytest.mark.asyncio
async def test_get_events_for_attorney(test_uow_factory, create_event_command):
    use_case = CreateEventUseCase(test_uow_factory)
    result = await use_case.execute(create_event_command)
    assert result.id is not None
    create_event_command.event_date = datetime(
        2027, 11, 11, 11, 00, tzinfo=timezone.utc
    )
    create_event_command.name = 'Приговор'
    result = await use_case.execute(create_event_command)
    assert result.id is not None

    # получить
    cmd = GetEventsForAttorneyQuery(result.attorney_id)
    use_case = GetEventByAttorneyUseCase(test_uow_factory)
    events = await use_case.execute(cmd)

    assert isinstance(events, list)
    assert len(events) >= 2


@pytest.mark.asyncio
async def test_get_events_for_case(test_uow_factory, create_event_command):
    use_case = CreateEventUseCase(test_uow_factory)
    result = await use_case.execute(create_event_command)
    assert result.id is not None
    create_event_command.event_date = datetime(
        2027, 11, 11, 11, 00, tzinfo=timezone.utc
    )
    create_event_command.name = 'Приговор'
    result = await use_case.execute(create_event_command)
    assert result.id is not None

    # получить
    cmd = GetEventsForCaseQuery(result.case_id)
    use_case = GetEventByCaseUseCase(test_uow_factory)
    events = await use_case.execute(cmd)

    assert isinstance(events, list)
    assert len(events) >= 2


@pytest.mark.asyncio
async def test_delete_event(test_uow_factory, create_event_command):
    # create
    create_use_case = CreateEventUseCase(test_uow_factory)
    created = await create_use_case.execute(create_event_command)
    assert created.id is not None

    # delete
    cmd = DeleteEventCommand(event_id=created.id)
    delete_use_case = DeleteEventUseCase(test_uow_factory)
    result = await delete_use_case.execute(cmd)

    assert result is True

    # Проверить, что действительно удалилось
    get_use_case = GetEventUseCase(test_uow_factory)
    with pytest.raises(EntityNotFoundException):
        await get_use_case.execute(GetEventQuery(event_id=created.id))
