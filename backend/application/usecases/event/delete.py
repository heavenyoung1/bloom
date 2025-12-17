from backend.application.dto.event import EventResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.domain.entities.event import Event
from backend.application.commands.event import (
    DeleteEventCommand,
)

# ВАЛИДАТОР!
from backend.core.logger import logger


class DeleteEventUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: DeleteEventCommand,
    ) -> 'EventResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело по его ID - event_id
                event = await uow.event_repo.get(cmd.event_id)

                if not event:
                    logger.error(f'Событие {cmd.event_id} не найдено.')
                    raise EntityNotFoundException(f'События не найдены.')

                # 3. Удалить событие
                updated_event = await uow.event_repo.delete(event.id)

                logger.info(f'Событие с ID {cmd.id} удалено.')
                return True

            except Exception as e:
                logger.error(
                    f'Ошибка при получении события с ID {cmd.attorney_id}: {e}'
                )
                raise e
