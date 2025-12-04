from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

from backend.application.usecases.client import (
    CreateClientUseCase,
    UpdateClientUseCase,
    DeleteClientUseCase,
    GetClientByIdUseCase,
    GetClientsForAttorneyUseCase,
)

from backend.application.validators.client_validator import ClientValidator
from backend.application.usecases.client.create import CreateClientUseCase

from backend.application.dto.client import (
    ClientCreateRequest,
    ClientResponse,
)

from backend.core.exceptions import NotFoundException, VerificationError

from backend.core.logger import logger


class ClientService:
    '''
    Сервис для работы с клиентами

    Ответственность:
    - Координация различных UseCase'ов
    - Может добавить дополнительную логику (логирование, кэширование и т.д.)
    '''

    def __init__(
        self,
        create_client_use_case: CreateClientUseCase,
        update_client_use_case: UpdateClientUseCase,
        delete_client_use_case: DeleteClientUseCase,
        get_client_by_id_use_case: GetClientByIdUseCase,
        get_clients_for_attorney_use_case: GetClientsForAttorneyUseCase,
    ):
        self.create_client_use_case = create_client_use_case
        self.update_client_use_case = update_client_use_case
        self.delete_client_use_case = delete_client_use_case
        self.get_client_by_id_use_case = get_client_by_id_use_case
        self.get_clients_for_attorney_use_case = get_clients_for_attorney_use_case

    async def create_client(self, request, owner_attorney_id: int):
        # Проверяем права доступа владельца
        # ТУТ ДОБАВИТЬ ПРОВЕРКУ!!!
        return await self.create_client_use_case.execute(request, owner_attorney_id)

    async def update_client(self, request, owner_attorney_id: int):
        # Проверяем права доступа владельца
        # ТУТ ДОБАВИТЬ ПРОВЕРКУ!!!
        return await self.update_client_use_case.execute(request, owner_attorney_id)

    async def delete_client(self, request, owner_attorney_id: int):
        # Проверяем права доступа владельца
        # ТУТ ДОБАВИТЬ ПРОВЕРКУ!!!
        return await self.delete_client_use_case.execute(request, owner_attorney_id)

    async def get_client_by_id(self, request, owner_attorney_id: int):
        # Проверяем права доступа владельца
        # ТУТ ДОБАВИТЬ ПРОВЕРКУ!!!
        return await self.get_client_by_id_use_case.execute(request, owner_attorney_id)

    async def get_all_clients(self, request, owner_attorney_id: int):
        # Проверяем права доступа владельца
        # ТУТ ДОБАВИТЬ ПРОВЕРКУ!!!
        return await self.get_clients_for_attorney_use_case.execute(
            request, owner_attorney_id
        )
