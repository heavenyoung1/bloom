from backend.application.dto.case import CaseCreateRequest, CaseResponse
from backend.domain.entities.case import Case
from backend.infrastructure.models.case import CaseStatus
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.logger import logger
from backend.core.exceptions import NotFoundException


class CreateCaseUseCase:
    '''Сценарий: юрист создаёт новое дело.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, dto: CaseCreateRequest, attorney_id: int) -> CaseResponse:
        # 1. Проверяем, что клиент существует (опционально, но правильно)
        async with self.uow_factory.create() as uow:
            # 1. Проверяем, что клиент существует (опционально, но правильно)

            pass