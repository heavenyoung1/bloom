from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.services.token_management_service import TokenManagementService
from backend.core.security import SecurityService
from backend.core.settings import settings
from backend.core.logger import logger
from backend.application.commands.attorney import LoginAttorneyCommand
from backend.application.dto.attorney import TokenResponse
from backend.core.exceptions import ValidationException, EntityNotFoundException


class SignInUseCase:
    """
    UseCase для входа в систему.

    Использует TokenManagementService для работы с токенами и rate limiting.
    """

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory
        self.token_service = TokenManagementService()

    async def execute(self, cmd: LoginAttorneyCommand) -> TokenResponse:
        """
        Вход в систему.

        Flow:
        1. Проверить rate limit
        2. Получить юриста по email
        3. Проверить пароль
        4. Проверить статусы (активен, верифицирован)
        5. Создать токены
        6. Сохранить refresh token
        7. Очистить счётчик попыток

        Raises:
            ValidationException: Если неправильные учетные данные или заблокирован
            EntityNotFoundException: Если юрист не найден
        """
        # 1. Проверить rate limiting
        await self.token_service.check_rate_limit(cmd.email)

        async with self.uow_factory.create() as uow:
            # 2. Получить юриста по email
            attorney = await uow.attorney_repo.get_by_email(cmd.email)
            if not attorney:
                # Записать попытку
                await self.token_service.record_failed_attempt(cmd.email)
                raise ValidationException('Некорректный email или пароль')

            # 3. Проверить пароль
            if not SecurityService.verify_password(
                cmd.password, attorney.hashed_password
            ):
                # Записать попытку
                await self.token_service.record_failed_attempt(cmd.email)
                raise ValidationException('Некорректный email или пароль')

            # 4. Проверить статусы
            if not attorney.is_active:
                raise ValidationException('Учетная запись адвоката заблокирована')

            if not attorney.is_verified:
                raise ValidationException('Email не подтвержден. Проверьте почту')

        # 5. Создать токены
        access_token = SecurityService.create_access_token(str(attorney.id))
        refresh_token = SecurityService.create_refresh_token(str(attorney.id))

        # 6. Сохранить refresh token в Redis
        await self.token_service.save_refresh_token(attorney.id, refresh_token)

        # 7. Очистить счётчик попыток при успешном входе
        await self.token_service.clear_failed_attempts(cmd.email)

        logger.info(f'Адвокат успешно вошел: {cmd.email} (ID: {attorney.id})')

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
