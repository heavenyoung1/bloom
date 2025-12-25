from backend.application.dto.event import EventResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException
from backend.application.commands.event import (
    GetEventQuery,
    GetEventsForAttorneyQuery,
    GetEventsForCaseQuery,
)

# ВАЛИДАТОР!
from backend.core.logger import logger


class GetEventUseCase:
    '''Сценарий: юрист получает событие.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetEventQuery,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело по ATTORNEY_ID
                event = await uow.event_repo.get(cmd.event_id)

                if not event:
                    logger.error(f'Событие по этому ID {cmd.event_id} не найдено.')
                    raise EntityNotFoundException(f'Событие не найдено.')

                logger.info(f'Событие получен: ID = {cmd.event_id}')
                return EventResponse.model_validate(event)

            except Exception as e:
                logger.error(f'Ошибка при получении события с ID {cmd.event_id}: {e}')
                raise e


class GetEventByAttorneyUseCase:
    '''Получить все события юриста'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetEventsForAttorneyQuery,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                events = await uow.event_repo.get_all_for_attorney(cmd.attorney_id)

                if not events:
                    logger.warning(f'События для юриста {cmd.attorney_id} не найдены.')
                    return []

                logger.info(
                    f'Получено {len(events)} событий для юриста {cmd.attorney_id}'
                )

                # ПРЕОБРАЗУЕМ КАЖДЫЙ ЭЛЕМЕНТ СПИСКА ОТДЕЛЬНО!
                return [EventResponse.model_validate(event) for event in events]

            except Exception as e:
                logger.error(
                    f'Ошибка при получении событий юриста {cmd.attorney_id}: {e}'
                )
                raise e


class GetNearestEventsByAttorneyUseCase:
    '''Получить ближайшие события для юриста отсортированные по дате и ограниченные по количеству'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetEventsForAttorneyQuery,
        events_count: int,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                events = await uow.event_repo.get_nearest_for_attorney(
                    attorney_id=cmd.attorney_id,
                    count=events_count,
                )

                if not events:
                    logger.warning(f'События для юриста {cmd.attorney_id} не найдены.')
                    return []

                logger.info(
                    f'Получено {len(events)} событий для юриста {cmd.attorney_id}'
                )

                # ПРЕОБРАЗУЕМ КАЖДЫЙ ЭЛЕМЕНТ СПИСКА ОТДЕЛЬНО!
                return [EventResponse.model_validate(event) for event in events]

            except Exception as e:
                logger.error(
                    f'Ошибка при получении событий юриста {cmd.attorney_id}: {e}'
                )
                raise e


class GetEventByCaseUseCase:
    '''Получить все события для конкретного дела'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetEventsForCaseQuery,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело по CASE_ID
                events = await uow.event_repo.get_for_case(cmd.case_id)

                if not events:
                    logger.error(f'События для дела {cmd.attorney_id} не найдены.')
                    return []

                logger.info(f'Получено {len(events)} событий для дела {cmd.case_id}')

                # ПРЕОБРАЗУЕМ КАЖДЫЙ ЭЛЕМЕНТ СПИСКА ОТДЕЛЬНО!
                return [EventResponse.model_validate(event) for event in events]

            except Exception as e:
                logger.error(f'Ошибка при получении события с ID {cmd.case_id}: {e}')
                raise e
