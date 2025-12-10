from backend.infrastructure.repositories.attorney_repo import AttorneyRepository
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.security import SecurityService
from backend.application.services.auth_service import AuthService
from backend.application.policy.attorney_policy import AttorneyPolicy
from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys
from backend.core.settings import settings
from backend.core.logger import logger

from backend.application.dto.attorney import (
    AttorneyResponse,
    RegisterRequest,
    LoginRequest,
    UpdateRequest,
    TokenResponse,
)


class SignInUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory
        self.auth_service = AuthService(uow_factory)

    async def execute(self, request: LoginRequest) -> TokenResponse:
        '''
        Вход в систему.

        Flow:
        1. Проверить rate limit
        2. Получить юриста по email
        3. Проверить пароль
        4. Проверить что верифицирован
        5. Создать токены
        6. Сохранить refresh token в Redis
        7. Очистить счётчик попыток
        '''

        # 1. Проверить rate limiting
        await self._check_rate_limit(request.email)

        async with self.uow_factory.create() as uow:

            # 2. Получить юриста по email
            attorney = await uow.attorney_repo.get_by_email(request.email)
            if not attorney:
                await self._record_failed_attempt(request.email)  # Это что за хрень?
                raise ValueError('Invalid credentials')

            # 3. Проверить пароль
            if not SecurityService.verify_password(
                request.password, attorney.hashed_password
            ):
                await self._record_failed_attempt(request.email)
                raise ValueError('Invalid credentials')

            # 4. Проверить статус
            if not attorney.is_active:
                raise ValueError('Attorney account is not active')

            # 5. Проверить верификацию
            if not attorney.is_verified:
                raise ValueError("Email not verified. Please check your email")

        # 6. Создать токены
        access_token = SecurityService.create_access_token(str(attorney.id))
        refresh_token = SecurityService.create_refresh_token(str(attorney.id))

        # 7. Сохранить refresh token в Redis
        await self.auth_service.save_refresh_token(attorney.id, refresh_token)

        # 8. Очистить счётчик попыток
        await self.auth_service.clear_failed_attempts(request.email)

        logger.info(f"Attorney logged in: {request.email}")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60,
        )

    async def _check_rate_limit(self, email: str) -> None:
        '''Проверить блокировку по rate limit'''
        lockout_key = RedisKeys.login_lockout(email)
        if await redis_client.exists(lockout_key):
            raise ValueError('Слишком много попыток входа. Попробуйте позже')

    async def _record_failed_attempt(self, email: str) -> None:
        '''Записать неудачную попытку входа'''
        attempts_key = RedisKeys.login_attempts(email)
        attempts = await redis_client.increment(attempts_key)

        # Если первая попытка - установить TTL
        if attempts == 1:
            await redis_client.set(attempts_key, 1, ttl=900)  # 15 минут

        # Если превышено максимум - заблокировать
        if attempts >= settings.MAX_LOGIN_ATTEMPTS:
            await redis_client.set(
                RedisKeys.login_lockout(email),
                True,
                ttl=settings.LOCKOUT_DURATION_MINUTES * 60,
            )
            logger.warning(f'Юрист заблокирован по rate limit: {email}')
