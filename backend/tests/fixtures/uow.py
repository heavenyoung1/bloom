import pytest
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from backend.core.logger import logger
from backend.infrastructure.tools.uow import AsyncUnitOfWork
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.db.database import DataBaseConnection

from backend.infrastructure.repositories import (
    AttorneyRepository,
    CaseRepository,
    ClientRepository,
    ContactRepository,
    DocumentMetadataRepository,
    EventRepository,
    OutboxRepository,
)

# =============== ОПРЕДЕЛЕНИЯ КЛАССОВ  ===============


class TestUnitOfWork:
    def __init__(self, session):
        self.session = session
        self.attorney_repo = AttorneyRepository(session)
        self.case_repo = CaseRepository(session)
        self.client_repo = ClientRepository(session)
        self.contact_repo = ContactRepository(session)
        self.doc_meta_repo = DocumentMetadataRepository(session)
        self.event_repo = EventRepository(session)
        self.outbox_repo = OutboxRepository(session)

    async def __aenter__(self):
        '''Вход в async context manager.'''
        logger.info('TestUnitOfWork инициализирован')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def commit(self):
        '''
        Зафиксировать изменения в БД.
        
        В тестах это просто флаш (flush), а не реальный commit!
        Реальный commit будет только когда выходим из session контекста.
        '''
        try:
            # ℹ️ ВАЖНО: Используем flush() вместо commit()
            # flush() отправляет SQL на БД, но не коммитит транзакцию
            # Это позволяет избежать проблем с rollback в конце теста
            await self.session.flush()

            # ======= 🧪🧪🧪🧪🧪🧪🧪 ======= #
            # РАЗКОММИТИТЬ КОММИТ ДЛЯ ПРОВЕРКИ ЕДИНИЧНЫХ ТЕСТОВ
            # ВСЕ КОММИТИТСЯ И НЕ ОТКАТЫВАЕТСЯ ПРИ ROLLBACK
            # await self.session.commit()
            # ======= 🧪🧪🧪🧪🧪🧪🧪 ======= #

            logger.debug('[TEST UoW] FLUSH выполнен (не commit!)')
        except Exception as e:
            logger.error(f'[TEST UoW] Ошибка при FLUSH: {e}')
            await self.rollback()
            raise

    async def rollback(self):
        '''Откатить изменения.'''
        try:
            await self.session.rollback()
            logger.debug('[TEST UoW] ROLLBACK выполнен')
        except Exception:
            pass  # Ignore rollback errors

class TestUoWFactory:
    def __init__(self, uow: TestUnitOfWork):
        self._uow = uow

    @asynccontextmanager
    async def create(self):
        # В тестах можно не создавать новый UoW каждый раз,
        # а просто отдавать уже существующий
        yield self._uow


# =============== РЕАЛИЗАЦИЯ ФИКСТУР НА ОСНОВЕ КЛАССОВ, ДЛЯ ИСПОЛЬЗОВАНИЯ В ТЕСТАХ  ===============


@pytest.fixture
async def test_uow(session):
    '''Создаёт директный UnitOfWork с тестовой сессией.'''
    uow = TestUnitOfWork(session)
    yield uow
    # Cleanup после теста
    await uow.rollback()


@pytest.fixture
async def test_uow_factory(test_uow):
    return TestUoWFactory(test_uow)
