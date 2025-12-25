from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import DeleteContactCommand
from backend.application.services.authorization_service import AuthorizationService
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class DeleteContactUseCase:
    '''Сценарий: юрист удаляет контакт.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: DeleteContactCommand,
        attorney_id: int,
    ) -> bool:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить контакт
                contact = await uow.contact_repo.get(cmd.contact_id)

                if not contact:
                    raise EntityNotFoundException(
                        f'Контакт с ID {cmd.contact_id} не найден.'
                    )

                # 2. Проверка прав доступа
                AuthorizationService.check_owner_access(
                    current_attorney_id=attorney_id,
                    owner_attorney_id=contact.attorney_id,
                    resource_type='контакт',
                    resource_id=cmd.contact_id,
                )

                # 3. Удалить контакт
                await uow.contact_repo.delete(cmd.contact_id)

                logger.info(f'Контакт с ID {cmd.contact_id} удалён.')
                return True

            except (EntityNotFoundException, AccessDeniedException) as e:
                logger.error(f'Ошибка при удалении контакта: {e}')
                raise e
            except Exception as e:
                logger.error(f'Неизвестная ошибка при удалении контакта: {e}')
                raise Exception('Ошибка при удалении контакта')
