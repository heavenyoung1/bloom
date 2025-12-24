from backend.application.dto.contact import ContactCreateRequest, ContactResponse
from backend.domain.entities.contact import Contact
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import UpdateContactCommand
from backend.application.policy.case_policy import CasePolicy
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger

class UpdateContactUseCase:

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: UpdateContactCommand,
    ) -> 'ContactResponse':
        async with self.uow_factory.create() as uow:
            try:
                contact = await uow.contact_repo.get(cmd.contact_id)
                if not contact:
                    logger.warning(f'контакт не найден: ID = {cmd.contact_id}')
                    raise EntityNotFoundException(
                        f'контакт не найден: ID = {cmd.contact_id}'
                    )
                
                contact.update(cmd)

                updated_contact = await uow.contact_repo.update(contact)

                logger.info(
                    f'Контакт обновлен: ID = {updated_contact.id}'
                    f'Владелец = {updated_contact.attorney_id}'
                )

                # 4. Возврат Response
                return ContactResponse.model_validate(updated_contact)

            except Exception as e:
                logger.error(f'Неизвестная ошибка при обновлении контакта: {e}')
                raise Exception('Ошибка при обновлении контакта')
