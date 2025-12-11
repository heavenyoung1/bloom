from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.services.token_management_service import TokenManagementService
from backend.core.logger import logger


class SignOutUseCase:
    """
    UseCase для выхода из системы (logout).

    Использует TokenManagementService для работы с токенами.
    """

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory
        self.token_service = TokenManagementService()

    async def execute(self, attorney_id: int, access_token: str) -> dict:
        """
        Выход из системы.

        Flow:
        1. Добавить access token в чёрный список
        2. Удалить refresh token из Redis
        3. Залогировать выход

        Args:
            attorney_id: ID адвоката из JWT токена
            access_token: Текущий access token для внесения в blacklist

        Returns:
            dict с сообщением об успешном выходе
        """
        try:
            # 1. Добавить access token в чёрный список
            await self.token_service.revoke_token(access_token)

            # 2. Удалить refresh token из Redis
            await self.token_service.delete_refresh_token(attorney_id)

            logger.info(f'Адвокат успешно вышел из системы: ID={attorney_id}')

            return {
                'message': 'Вы успешно вышли из системы',
                'attorney_id': attorney_id,
            }

        except Exception as e:
            logger.error(f'Ошибка при выходе из системы (ID={attorney_id}): {e}')
            raise
