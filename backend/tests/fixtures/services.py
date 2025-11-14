import pytest

from backend.application.services.attorney_service import AttorneyService


@pytest.fixture
async def attorney_service(uow_factory):
    '''Фикстура для создания сервиса юриста.'''
    return AttorneyService(uow_factory)
