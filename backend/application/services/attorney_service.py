from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.logger import logger

from backend.application.dto.attorney import (
    AttorneyVerificationResponse,
    AttorneyVerificationUpdateRequest,
)

from backend.core.exceptions import NotFoundException, VerificationError


class AttorneyService:
    '''Service для работы с юристами'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory  # Используем фабрику для создания UoW

    async def set_verified(self, email: str) -> 'AttorneyVerificationResponse':
        '''Установить флаг верификации для юриста по email.'''
        # 1. Создаём UoW через фабрику (получаем все репозитории)
        async with self.uow_factory.create() as uow:
            attorney = await uow.attorney_repo.get_by_email(email)
            if attorney is None:
                logger.warning(
                    f'Попытка изменить статус верификации несуществующего юриста: {email}'
                )
                raise NotFoundException('Юрист с таким email не найден')
            if attorney.is_verified == True:
                logger.warning(f'Пользователь {attorney.email} уже верифицирован')
                raise VerificationError(
                    f'Пользователь {attorney.email} уже верифицирован'
                )

            # 2. Обновляем только флаг в БД через отдельный метод
            updated_attorney = await uow.attorney_repo.change_verify(
                attorney_id=attorney.id,
                is_verified=True,
            )

            logger.info(
                f'Статус верификации изменён: email={attorney.email}, '
                f'is_verified={attorney.is_verified}'
            )

        # 5. Формируем ответ
        return AttorneyVerificationResponse(
            id=attorney.id,
            email=attorney.email,
            is_verified=attorney.is_verified,
        )
