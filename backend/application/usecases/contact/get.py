from backend.application.dto.contact import ContactResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import GetContactByIdQuery
from backend.core.exceptions import EntityNotFoundException
from backend.core.logger import logger


class GetContactByIdUseCase:
    '''Сценарий: юрист получает информацию о контакте по ID'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetContactByIdQuery,
    ) -> 'ContactResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело
                contact = await uow.contact_repo.get(cmd.contact_id)

                if not contact:
                    logger.error(f'Контакт с ID {cmd.contact_id} не найдено.')
                    raise EntityNotFoundException(f'Контакт не найден.')

                logger.info(f'Дело получено: ID = {cmd.contact_id}')
                return ContactResponse.model_validate(contact)
            except Exception as e:
                logger.error(f'Ошибка при получении контакта: {e}')
                raise e
