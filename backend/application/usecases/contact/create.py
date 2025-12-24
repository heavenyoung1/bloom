from backend.application.dto.contact import ContactCreateRequest, ContactResponse
from backend.domain.entities.contact import Contact
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import CreateContactCommand
from backend.application.policy.case_policy import CasePolicy
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class CreateContactUseCase:
    '''Сценарий: юрист создаёт новый контакт, связанный с делом.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: CreateContactCommand,
    ) -> 'ContactResponse':
        async with self.uow_factory.create() as uow:
            try:
                contact = Contact.create(
                    name=cmd.name,
                    personal_info=cmd.personal_info,
                    phone=cmd.phone,
                    email=cmd.email,
                    case_id=cmd.case_id,
                    attorney_id=cmd.attorney_id,
                )

                saved_contact = await uow.contact_repo.save(contact)

                logger.info(
                    f'Контакт создан: ID = {saved_contact.id} '
                    f'Владелец = {saved_contact.attorney_id} '
                    f'Связанное дело = {saved_contact.case_id} '
                )

                return ContactResponse.model_validate(saved_contact)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании контакта: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании контакта: {e}')
                raise Exception('Ошибка при создании контакта')
