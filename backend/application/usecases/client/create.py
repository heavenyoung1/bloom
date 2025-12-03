from backend.application.dto.client import ClientCreateRequest
from backend.domain.entities.case import Case
from backend.infrastructure.models.case import CaseStatus
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.logger import logger
from backend.core.exceptions import NotFoundException
from backend.application.validators.client_validator import ClientValidator

class CreateClientUseCase:
    '''Создание нового клиента'''
    def __init__(self, uow_factory: UnitOfWorkFactory, validator: ClientValidator):
        self.uow_factory = uow_factory
        self.validator = validator

    async def execute(self, dto: ClientCreateRequest):
        async with self.uow_factory as uow:
            await self.validator.on_create(dto)