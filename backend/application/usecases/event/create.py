from backend.application.dto.event import EventResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.domain.entities.event import Event
from backend.application.commands.event import CreateEventCommand

# ВАЛИДАТОР!
from backend.core.logger import logger


class CreateEventUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: CreateEventCommand,
    ) -> 'EventResponse':

        async with self.uow_factory.create() as uow:
            try:
                event = Event.create(
                    name=cmd.name,
                    description=cmd.description,
                    event_type=cmd.event_type,
                    event_date=cmd.event_date,
                    case_id=cmd.case_id,
                    attorney_id=cmd.attorney_id,
                )

                # 3. Сохранение в БД
                saved_event = await uow.event_repo.save(event)

                logger.info(
                    f'Событие создано: ID = {saved_event.id}'
                    f'Владелец = {saved_event.attorney_id}'
                    f'Назначенное дело = {saved_event.case_id}'
                )

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании события: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании события: {e}')
                raise Exception('Ошибка при создании события')
