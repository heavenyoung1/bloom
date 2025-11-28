import pytest
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from backend.infrastructure.tools.uow import AsyncUnitOfWork
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.db.database import DataBaseConnection

class TestUoWFactory:
    def __init__(self, uow: AsyncUnitOfWork):
        self._uow = uow

    @asynccontextmanager
    async def create(self):
        # В тестах можно не создавать новый UoW каждый раз,
        # а просто отдавать уже существующий
        yield self._uow

@pytest.fixture
async def test_uow(session) -> AsyncGenerator[AsyncUnitOfWork, None]:
    '''Создаёт директный UnitOfWork с тестовой сессией.'''
    uow = AsyncUnitOfWork(session)
    async with uow:
        yield uow


@pytest.fixture
async def test_uow_factory(test_uow):
    return TestUoWFactory(test_uow)
