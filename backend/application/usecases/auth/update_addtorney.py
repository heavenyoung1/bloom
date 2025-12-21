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


class UpdateAttorneyUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, cmd: UpdateAttorneyCommand) -> 'AttorneyResponse':
        '''
        Обновить профиль адвоката (PATCH).

        Flow:
        1. Валидировать через Policy
        2. Обновить только переданные поля
        3. Сохранить в БД
        '''
        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидировать
                policy = AttorneyPolicy(uow.attorney_repo)
                await policy.on_update(cmd.attorney_id, cmd)

                # 2. Получить юриста
                attorney = await uow.attorney_repo.get(cmd.attorney_id)
                if not attorney:
                    raise EntityNotFoundException(
                        f'Адвокат с ID {cmd.attorney_id} не найден'
                    )

                # 3. Обновить только переданные поля через доменный метод
                attorney.update(cmd)

                # 4. Сохранить изменения (используем update для существующей записи)
                updated_attorney = await uow.attorney_repo.update(attorney)

                logger.info(f'Профиль обновлен: ID {cmd.attorney_id}')

                return AttorneyResponse.model_validate(updated_attorney)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при обновлении профиля адвоката: {e}')
                raise
