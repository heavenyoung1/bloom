from backend.core.settings import settings
from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys
from backend.core.logger import logger
from backend.core.exceptions import ValidationException


class TokenManagementService:
    '''
    Сервис для управления токенами и сессиями.

    ⚠️ Этот Service используется в РАЗНЫХ UseCase'ах:
    - SignInUseCase → save_refresh_token()
    - SignOutUseCase → revoke_token()
    - Middleware → is_token_revoked()
    - SignInUseCase → record_failed_attempt()
    '''

    # ========== REFRESH TOKEN ==========

    async def save_refresh_token(self, attorney_id: int, refresh_token: str) -> None:
        '''
        Сохранить refresh token в Redis.

        Используется в: SignInUseCase
        '''
        ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        await redis_client.set(
            RedisKeys.refresh_token(attorney_id),
            refresh_token,
            ttl=ttl,
        )
        logger.debug(f'Refresh token сохранён для юриста {attorney_id}')

    async def get_refresh_token(self, attorney_id: int) -> str:
        '''
        Получить refresh token из Redis.

        Используется в: RefreshTokenUseCase
        '''
        token = await redis_client.get(RedisKeys.refresh_token(attorney_id))
        if not token:
            raise ValidationException('Refresh token не найден или истёк')
        return token

    async def delete_refresh_token(self, attorney_id: int) -> None:
        '''
        Удалить refresh token (logout).

        Используется в: SignOutUseCase
        '''
        await redis_client.delete(RedisKeys.refresh_token(attorney_id))
        logger.info(f'Refresh token удалён для юриста {attorney_id}')

    # ========== TOKEN BLACKLIST ==========

    async def revoke_token(self, token: str) -> None:
        '''
        Добавить access token в чёрный список.

        Используется в: SignOutUseCase (для дополнительной безопасности)
        '''
        ttl = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        await redis_client.set(
            RedisKeys.token_blacklist(token),
            '1',  # Redis не может хранить boolean! сохраняем как Строку
            ttl=ttl,
        )
        logger.debug(f'Access token добавлен в чёрный список')

    async def is_token_revoked(self, token: str) -> bool:
        '''
        Проверить, в чёрном ли списке токен.

        Используется в: Middleware для проверки валидности токена
        '''
        return await redis_client.exists(RedisKeys.token_blacklist(token))

    # ========== RATE LIMITING ==========

    async def check_rate_limit(self, email: str) -> None:
        '''
        Проверить, не заблокирован ли адвокат по rate limit.

        Используется в: SignInUseCase

        Raises:
            ValidationException: Если заблокирован
        '''
        lockout_key = RedisKeys.login_lockout(email)
        if await redis_client.exists(lockout_key):
            raise ValidationException(
                f'Слишком много попыток входа. '
                f'Попробуйте позже ({settings.LOCKOUT_DURATION_MINUTES} минут)'
            )

    async def record_failed_attempt(self, email: str) -> None:
        '''
        Записать неудачную попытку входа.
        Заблокировать аккаунт если нужно.

        Используется в: SignInUseCase (при ошибке пароля)

        Logic:
        1. Инкрементировать счётчик попыток
        2. Если первая попытка - установить TTL (15 минут)
        3. Если превышен лимит - заблокировать

        Raises:
            ValidationException: Если превышен лимит попыток
        '''
        attempts_key = RedisKeys.login_attempts(email)
        attempts = await redis_client.increment(attempts_key, amount=1)

        # Если первая попытка - установить TTL (15 минут)
        if attempts == 1:
            await redis_client.expire(attempts_key, 900)

        # Если превышено максимум - заблокировать
        if attempts >= settings.MAX_LOGIN_ATTEMPTS:
            await redis_client.set(
                RedisKeys.login_lockout(email),
                '1',  # Redis не может хранить boolean! сохраняем как Строку
                ttl=settings.LOCKOUT_DURATION_MINUTES * 60,
            )
            logger.warning(
                f'Адвокат заблокирован по rate limit: {email} ' f'({attempts} попыток)'
            )
            raise ValidationException(
                f'Учетная запись заблокирована на '
                f'{settings.LOCKOUT_DURATION_MINUTES} минут'
            )

    async def clear_failed_attempts(self, email: str) -> None:
        '''
        Очистить счётчик попыток при успешном входе.

        Используется в: SignInUseCase (при успехе)
        '''
        await redis_client.delete(RedisKeys.login_attempts(email))
        logger.debug(f'Счётчик попыток очищен для {email}')
