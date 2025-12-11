from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.security import SecurityService
from backend.application.policy.attorney_policy import AttorneyPolicy
from backend.application.commands.attorney import (
    ChangePasswordCommand,
)
from backend.application.dto.attorney import AttorneyResponse
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class ChangePasswordUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, cmd: ChangePasswordCommand) -> dict:
        '''
        Изменить пароль адвоката.

        Flow:
        1. Получить юриста
        2. Проверить текущий пароль
        3. Валидировать новый пароль
        4. Захешировать и сохранить
        '''
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить юриста
                attorney = await uow.attorney_repo.get(cmd.attorney_id)
                if not attorney:
                    raise EntityNotFoundException(
                        f'Адвокат с ID {cmd.attorney_id} не найден'
                    )

                # 2. Проверить текущий пароль
                if not SecurityService.verify_password(
                    cmd.old_password, attorney.hashed_password
                ):
                    raise ValidationException('Текущий пароль неправильный')

                # 3. Валидировать новый пароль
                policy = AttorneyPolicy(uow.attorney_repo)
                policy._validate_password(cmd.new_password)

                # 4. Проверить что пароли разные
                if cmd.old_password == cmd.new_password:
                    raise ValidationException(
                        'Новый пароль должен отличаться от текущего'
                    )

                # 5. Захешировать и сохранить
                attorney.hashed_password = SecurityService.hash_password(
                    cmd.new_password
                )
                await uow.attorney_repo.save(attorney)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при изменении пароля: {e}')
                raise

        logger.info(f'Пароль изменен для адвоката ID: {cmd.attorney_id}')

        return {'message': 'Пароль успешно изменен'}
