from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.logger import logger

from backend.application.validators.client_validator import ClientValidator
from backend.application.usecases.client.create import CreateClientUseCase

from backend.application.dto.client import (
    ClientCreateRequest,
    ClientResponse,
)

from backend.core.exceptions import NotFoundException, VerificationError


class ClientService:
    '''
    Сервис для работы с клиентами

    Ответственность:
    - Координация различных UseCase'ов
    - Может добавить дополнительную логику (логирование, кэширование и т.д.)
    '''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory
        self.create_client_use_case = CreateClientUseCase(uow_factory)

    async def create_client(
        self, request: ClientCreateRequest, owner_attorney_id: int
    ) -> ClientResponse:
        '''Создание клиента через UseCase'''
        return await self.create_client_use_case.execute(request, owner_attorney_id)
