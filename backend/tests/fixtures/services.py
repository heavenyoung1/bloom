import pytest

from backend.application.services import (
    AttorneyService,
    ClientService,
)


# @pytest.fixture
# async def attorney_service(test_uow_factory) -> 'AttorneyService':
#     '''Фикстура для создания сервиса юриста.'''
#     return AttorneyService(test_uow_factory)

@pytest.fixture
async def client_service(test_uow_factory) -> 'ClientService':
    '''Фикстура для создания сервиса клиента.'''
    return ClientService(test_uow_factory)
