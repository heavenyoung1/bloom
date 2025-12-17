from backend.application.dto.event import EventResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.domain.entities.event import Event
from backend.application.commands.event import (
    GetEventsForAttorneyQuery,
    GetEventsForCaseQuery,
)

# ВАЛИДАТОР!
from backend.core.logger import logger


class GetEventByAttorneyUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetEventsForAttorneyQuery,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело по ATTORNEY_ID
                event = await uow.event_repo.get_all_for_attorney(cmd.attorney_id)

                if not event:
                    logger.error(f'События для юриста {cmd.attorney_id} не найдены.')
                    raise EntityNotFoundException(f'События не найдены.')
            except Exception as e:
                logger.error(
                    f'Ошибка при получении события с ID {cmd.attorney_id}: {e}'
                )
                raise e


class GetEventByCaseUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetEventsForCaseQuery,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело по CASE_ID
                event = await uow.event_repo.get_for_case(cmd.case_id)

                if not event:
                    logger.error(f'События для дела {cmd.attorney_id} не найдены.')
                    raise EntityNotFoundException(f'События не найдены.')
            except Exception as e:
                logger.error(f'Ошибка при получении события с ID {cmd.case_id}: {e}')
                raise e
