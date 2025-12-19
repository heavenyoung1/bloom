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

                # 3. Обновить только переданные поля
                if cmd.first_name is not None:
                    attorney.first_name = cmd.first_name
                if cmd.last_name is not None:
                    attorney.last_name = cmd.last_name
                if cmd.patronymic is not None:
                    attorney.patronymic = cmd.patronymic
                if cmd.phone is not None:
                    attorney.phone = cmd.phone
                if cmd.license_id is not None:
                    attorney.license_id = cmd.license_id

                # 4. Сохранить
                # ВОТ ТУ ВОПРОСИКИ??
                # ПОЧЕМУ ТУТ SAVE?????????
                attorney = await uow.attorney_repo.save(attorney)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при обновлении профиля адвоката: {e}')
                raise

        logger.info(f'Профиль обновлен: ID {cmd.attorney_id}')

        return AttorneyResponse.model_validate(attorney)
