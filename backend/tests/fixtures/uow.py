import pytest
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from backend.infrastructure.tools.uow import AsyncUnitOfWork

@pytest.fixture
def uow_mock(
    attorney_repo_mock,
    case_repo_mock,
    client_repo_mock,
    contact_repo_mock,
    document_repo_mock,
    event_repo_mock,
):
    '''
    Mock Unit of Work для unit тестов.
    
    Все repositories — mock объекты.
    
    Использование:
        async def test_create_attorney(uow_mock):
            # Настраиваем поведение mock
            uow_mock.attorney_repo.get_by_email.return_value = None
            uow_mock.attorney_repo.save.return_value = attorney_obj
            
            # Тестируем Service
            service = AttorneyService(uow_mock)
            result = await service.create_attorney(data)
    '''
    uow = AsyncMock()
    uow.attorney_repo = attorney_repo_mock
    uow.case_repo = case_repo_mock
    uow.client_repo = client_repo_mock
    uow.contact_repo = contact_repo_mock
    uow.document_repo = document_repo_mock
    uow.event_repo = event_repo_mock
    return uow


@pytest.fixture
async def test_uow(session) -> AsyncGenerator[AsyncUnitOfWork, None]:
    '''Реальный UoW с тестовой сессией + откатом'''
    uow = AsyncUnitOfWork(session)
    async with uow:
        yield uow


@pytest.fixture
@asynccontextmanager
async def test_uow_factory(session) -> AsyncGenerator[AsyncUnitOfWork, None]:
    '''
    Тестовая фабрика UoW — НЕ использует DataBaseConnection и Settings!
    
    Использование:
        async def test_something(test_uow_factory):
            async with test_uow_factory() as uow:
                ...
    '''
    uow = AsyncUnitOfWork(session)
    async with uow:
        yield uow
