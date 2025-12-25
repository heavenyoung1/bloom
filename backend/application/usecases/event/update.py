from backend.application.dto.event import EventResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException
from backend.application.commands.event import (
    UpdateEventCommand,
)

# ВАЛИДАТОР!
from backend.core.logger import logger


class UpdateEventUseCase:
    '''Сценарий: обновляе событие.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: UpdateEventCommand,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело по его ID - event_id
                event = await uow.event_repo.get(cmd.event_id)

                if not event:
                    logger.error(f'События для юриста {cmd.event_id} не найдены.')
                    raise EntityNotFoundException(f'События не найдены.')

                # 2. Применяем изменения через метод update доменной сущности
                event.update(cmd)

                # 3. Сохраняем изменения
                updated_event = await uow.event_repo.update(event)
                logger.info(f'Событие обновлено: ID = {updated_event.id}')

                return EventResponse.model_validate(updated_event)

            except Exception as e:
                logger.error(f'Ошибка при получении события с ID {cmd.event_id}: {e}')
                raise e
