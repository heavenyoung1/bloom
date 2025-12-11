from typing import Optional

from backend.core.settings import settings
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys
from backend.core.security import SecurityService
from backend.core.exceptions import ValidationException
from backend.core.logger import logger


class AuthService:
    '''Сервис для управления сессиями и токенами'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    # ========== REFRESH TOKEN ==========

    async def refresh_access_token(self, refresh_token: str, attorney_id: int) -> str:
        '''
        Обновить access token используя refresh token.

        Flow:
        1. Проверить, есть ли refresh token в Redis
        2. Создать новый access token
        '''
        # 1. Проверить валидность refresh token
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

    async def save_refresh_token(self, attorney_id: int, refresh_token: str) -> None:
        '''Сохранить refresh token в Redis с TTL'''

        ttl = settings.refresh_token_expire_days * 24 * 3600
        await redis_client.set(
            RedisKeys.refresh_token(attorney_id),
            refresh_token,
            ttl=ttl,
        )
        logger.debug(f'Refresh token сохранён для юриста {attorney_id}')

    # ========== LOGOUT ==========

    async def logout(self, attorney_id: int) -> None:
        '''
        Выход из системы (удалить refresh token из Redis).

        Flow:
        1. Удалить refresh token
        2. Залогировать выход
        '''
        await redis_client.delete(RedisKeys.refresh_token(attorney_id))
        logger.info(f'Юрист вышел из системы, ID={attorney_id}')

    # ========== TOKEN BLACKLIST ==========

    async def revoke_token(self, token: str) -> None:
        '''Добавить токен в чёрный список при logout'''
        ttl = settings.lockout_duration_minutes * 60
        await redis_client.set(
            RedisKeys.token_blacklist(token),
            True,
            ttl=ttl,
        )
        logger.debug('Токен добавлен в чёрный список')

    async def is_token_revoked(self, token: str) -> bool:
        '''Проверить в чёрном ли списке токен'''
        return await redis_client.exists(RedisKeys.token_blacklist(token))

    # ========== RATE LIMITING ==========

    async def check_rate_limit(self, email: str) -> None:
        '''
        Проверить есть ли блокировка по rate limit.

        Raises:
            ValidationException: Если заблокирован
        '''
        lockout_key = RedisKeys.login_lockout(email)
        if await redis_client.exists(lockout_key):
            raise ValidationException(
                f'Слишком много попыток входа. '
                f'Попробуйте позже ({settings.lockout_duration_minutes} минут)'
            )

    async def record_failed_attempt(self, email: str) -> None:
        '''
        Записать неудачную попытку входа и заблокировать если нужно.

        Logic:
        1. Инкрементировать счётчик попыток
        2. Если первая попытка - установить TTL (15 минут)
        3. Если превышен лимит - заблокировать
        '''
        attempts_key = RedisKeys.login_attempts(email)
        attempts = await redis_client.increment(attempts_key, amount=1)

        # Если первая попытка - установить TTL (15 минут)
        if attempts == 1:
            await redis_client.set(attempts_key, 1, ttl=900)

        # Если превышено максимум - заблокировать
        if attempts >= settings.max_login_attempts:
            await redis_client.set(
                RedisKeys.login_lockout(email),
                True,
                ttl=settings.lockout_duration_minutes * 60,
            )
            logger.warning(
                f'Юрист заблокирован по rate limit: {email} ' f'({attempts} попыток)'
            )
            raise ValidationException(
                f'Учетная запись заблокирована на {settings.lockout_duration_minutes} минут'
            )

    async def clear_failed_attempts(self, email: str) -> None:
        '''Очистить счётчик попыток при успешном логине'''
        await redis_client.delete(RedisKeys.login_attempts(email))
        logger.debug(f'Счётчик попыток очищен для {email}')
