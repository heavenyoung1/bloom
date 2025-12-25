from backend.application.dto.contact import ContactResponse
from backend.domain.entities.contact import Contact
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import UpdateContactCommand
from backend.application.services.authorization_service import AuthorizationService
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class UpdateContactUseCase:
    '''Сценарий: юрист обновляет контакт'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: UpdateContactCommand,
        attorney_id: int,
    ) -> 'ContactResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить контакт
                contact = await uow.contact_repo.get(cmd.contact_id)
                if not contact:
                    logger.warning(f'Контакт не найден: ID = {cmd.contact_id}')
                    raise EntityNotFoundException(
                        f'Контакт не найден: ID = {cmd.contact_id}'
                    )

                # 2. Проверка прав доступа
                AuthorizationService.check_owner_access(
                    current_attorney_id=attorney_id,
                    owner_attorney_id=contact.attorney_id,
                    resource_type='контакт',
                    resource_id=cmd.contact_id,
                )

                # 3. Обновить контакт
                contact.update(cmd)

                # 4. Сохранить изменения
                updated_contact = await uow.contact_repo.update(contact)

                logger.info(
                    f'Контакт обновлен: ID = {updated_contact.id}, '
                    f'Владелец = {updated_contact.attorney_id}'
                )

                # 5. Возврат Response
                return ContactResponse.model_validate(updated_contact)

            except (EntityNotFoundException, AccessDeniedException) as e:
                logger.error(f'Ошибка при обновлении контакта: {e}')
                raise e
            except Exception as e:
                logger.error(f'Неизвестная ошибка при обновлении контакта: {e}')
                raise Exception('Ошибка при обновлении контакта')
