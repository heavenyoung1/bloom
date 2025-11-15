import pytest
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from backend.infrastructure.tools.uow import AsyncUnitOfWork
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.db.database import DataBaseConnection


# @pytest.fixture
# def uow_mock(
#     attorney_repo_mock,
#     case_repo_mock,
#     client_repo_mock,
#     contact_repo_mock,
#     document_repo_mock,
#     event_repo_mock,
# ):
#     uow = AsyncMock()
#     uow.attorney_repo = attorney_repo_mock
#     uow.case_repo = case_repo_mock
#     uow.client_repo = client_repo_mock
#     uow.contact_repo = contact_repo_mock
#     uow.document_repo = document_repo_mock
#     uow.event_repo = event_repo_mock
#     return uow


@pytest.fixture
async def test_uow(session) -> 'AsyncUnitOfWork':
    """
    Создаёт директный UnitOfWork с тестовой сессией.

    Использование (если нужно работать с UoW напрямую):
        async def test_something(test_uow):
            attorney = await test_uow.attorney_repo.get(1)
    """
    uow = AsyncUnitOfWork(session)
    async with uow:
        yield uow


@pytest.fixture
async def uow_factory(test_settings):
    '''Тестовая фабрика UoW с тестовой базой данных.'''
    # Подключаемся к тестовой базе данных
    db_connection = DataBaseConnection(settings=test_settings)

    # Создаём фабрику
    uow_factory = UnitOfWorkFactory(db_connection)

    # # Возвращаем фабрику для создания UnitOfWork
    # async with uow_factory.create() as uow:
    #     yield uow
    yield uow_factory

    # Cleanup
    await uow_factory.close()
