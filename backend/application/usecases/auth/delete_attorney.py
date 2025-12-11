from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.security import SecurityService
from backend.application.policy.attorney_policy import AttorneyPolicy
from backend.application.commands.attorney import (
    UpdateAttorneyCommand,
    ChangePasswordCommand,
    DeleteAttorneyAccountCommand,
)
from backend.application.dto.attorney import AttorneyResponse
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class DeleteAttorneyAccountUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, cmd: DeleteAttorneyAccountCommand) -> dict:
        '''
        Удалить учетную запись адвоката (со всеми связанными данными).

        Flow:
        1. Получить юриста
        2. Проверить пароль (подтверждение)
        3. Удалить адвоката (каскадное удаление через БД)
        '''
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить юриста
                attorney = await uow.attorney_repo.get(cmd.attorney_id)
                if not attorney:
                    raise EntityNotFoundException(
                        f'Адвокат с ID {cmd.attorney_id} не найден'
                    )

                # 2. Проверить пароль
                if not SecurityService.verify_password(
                    cmd.password, attorney.hashed_password
                ):
                    raise ValidationException('Пароль неправильный')

                # 3. Удалить
                await uow.attorney_repo.delete(cmd.attorney_id)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при удалении аккаунта: {e}')
                raise

        logger.warning(f'Учетная запись адвоката удалена: ID {cmd.attorney_id}')

        return {'message': 'Учетная запись успешно удалена'}
