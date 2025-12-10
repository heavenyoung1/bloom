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
async def test_create_case(test_uow_factory, create_case_command):
    pass