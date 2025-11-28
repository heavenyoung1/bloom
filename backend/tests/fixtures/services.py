import pytest

from backend.application.services.attorney_service import AttorneyService


@pytest.fixture
async def attorney_service(test_uow_factory) -> 'AttorneyService':
    '''Фикстура для создания сервиса юриста.'''
    return AttorneyService(test_uow_factory)
