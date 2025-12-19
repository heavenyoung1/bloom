"""Фикстуры для работы с Outbox в тестах."""

import pytest
from backend.tests.helpers.outbox_helper import process_outbox_events
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.db.database import database


@pytest.fixture
def auto_process_outbox():
    """
    Фикстура для автоматической обработки Outbox событий.
    
    Использование:
        async def test_something(http_client, auto_process_outbox, valid_attorney_dto):
            # Регистрация создаст событие в Outbox
            await http_client.post('/api/v0/auth/register', json=valid_attorney_dto.model_dump())
            
            # Автоматически обработает Outbox события
            await auto_process_outbox()
            
            # Теперь код верификации доступен в Redis
    """
    async def _process():
        uow_factory = UnitOfWorkFactory(database)
        await process_outbox_events(uow_factory)
    
    return _process

