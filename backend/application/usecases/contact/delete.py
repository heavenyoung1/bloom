from backend.application.dto.contact import ContactResponse
from backend.domain.entities.contact import Contact
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import DeleteContactCommand
from backend.application.policy.case_policy import CasePolicy
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger

class DeleteContactUseCase:
    '''Сценарий: юрист удаляеь контакт.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: DeleteContactCommand,
    ) -> bool:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить контакт
                contact = await uow.contact_repo.get(cmd.contact_id)

                if not contact:
                    raise EntityNotFoundException(
                        f'Контакт с ID {cmd.contact_id} не найден.'
                    )

                # 3. Удалить контакт
                await uow.contact_repo.delete(cmd.contact_id)

                logger.info(f'Контакт с ID {cmd.contact_id} удалён.')
                return True
            
            except Exception as e:
                logger.error(f'Ошибка при удалении контакта: {e}')
                raise e
