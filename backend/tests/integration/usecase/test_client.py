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
async def test_update_client(test_uow_factory, create_client_command, update_client_command):
    create_use_case = CreateClientUseCase(test_uow_factory)
    result = await create_use_case.execute(create_client_command)
    assert result.id is not None

    update_client_command.client_id = result.id
    update_use_case = UpdateClientUseCase(test_uow_factory)
    result = await update_use_case.execute(update_client_command)
    assert result.id is not None