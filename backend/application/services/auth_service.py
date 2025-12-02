from typing import Optional

from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys
from backend.core.security import SecurityService
from backend.core.logger import logger


class AuthService:
    '''Сервис для управления сессиями и токенами'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def refresh_access_token(self, refresh_token: str, attorney_id: int) -> str:
        '''Обновить access token используя refresh token'''

        # 1. Проверить, есть ли этот refresh token в Redis
        stored_token = await redis_client.get(RedisKeys.refresh_token(attorney_id))
        if stored_token != refresh_token:
            logger.warning(
                f'Попытка использовать невалидный refresh token, ID={attorney_id}'
            )
            raise ValueError('Invalid refresh token')

        # 2. Создать новый access token
        new_access_token = SecurityService.create_access_token(str(attorney_id))
        logger.info(f'Access token обновлён для юриста ID={attorney_id}')

        return new_access_token

    async def logout(self, attorney_id: int) -> None:
        '''Выход из системы (удалить refresh token)'''
        await redis_client.delete(RedisKeys.refresh_token(attorney_id))
        logger.info(f'Юрист вышел из системы, ID={attorney_id}')

    async def revoke_token(self, token: str) -> None:
        '''Добавить токен в чёрный список'''
        await redis_client.set(
            RedisKeys.token_blacklist(token), True, ttl=15 * 60  # 15 минут
        )

    async def is_token_revoked(self, token: str) -> bool:
        '''Проверить, в чёрном ли списке токен'''
        return await redis_client.exists(RedisKeys.token_blacklist(token))
