import pytest

from backend.application.usecases.client import (
    CreateClientUseCase,
    UpdateClientUseCase,
    GetClientByIdUseCase,
    DeleteClientUseCase,
    GetClientsForAttorneyUseCase,
)
from backend.application.commands.client import (
    CreateClientCommand,
    GetClientByIdQuery,
    GetClientsForAttorneyQuery,
    UpdateClientCommand,
    DeleteClientCommand,
)
from backend.core.logger import logger


@pytest.mark.asyncio
async def test_create_client(test_uow_factory, create_client_command):
    use_case = CreateClientUseCase(test_uow_factory)
    result = await use_case.execute(create_client_command)

    assert result.id is not None


@pytest.mark.asyncio
async def test_update_client(
    test_uow_factory, create_client_command, update_client_command
):
    create_use_case = CreateClientUseCase(test_uow_factory)
    result = await create_use_case.execute(create_client_command)
    assert result.id is not None

    update_client_command.client_id = result.id
    update_use_case = UpdateClientUseCase(test_uow_factory)
    result = await update_use_case.execute(update_client_command)
    assert result.id is not None


@pytest.mark.asyncio
async def test_get_client(test_uow_factory, create_client_command):
    create_use_case = CreateClientUseCase(test_uow_factory)
    result = await create_use_case.execute(create_client_command)
    assert result.id is not None

    get_client_command = GetClientByIdQuery(client_id=result.id)
    get_use_case = GetClientByIdUseCase(test_uow_factory)
    result = await get_use_case.execute(get_client_command)
    assert result.id == get_client_command.client_id


@pytest.mark.asyncio
async def test_delete_client(test_uow_factory, create_client_command):
    create_use_case = CreateClientUseCase(test_uow_factory)
    result = await create_use_case.execute(create_client_command)
    assert result.id is not None

    delete_client_command = GetClientByIdQuery(client_id=result.id)
    delete_use_case = DeleteClientUseCase(test_uow_factory)
    result = await delete_use_case.execute(delete_client_command)
    assert result is True


@pytest.mark.asyncio
async def test_get_all_clients_for_attorney(test_uow_factory, create_client_command):
    create_use_case = CreateClientUseCase(test_uow_factory)
    result = await create_use_case.execute(create_client_command)
    assert result.id is not None

    get_all_clients_command = GetClientsForAttorneyQuery(
        owner_attorney_id=result.owner_attorney_id
    )
    get_all_clients_use_case = GetClientsForAttorneyUseCase(test_uow_factory)
    result = await get_all_clients_use_case.execute(get_all_clients_command)
    assert len(result) == 1
