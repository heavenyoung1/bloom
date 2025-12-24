from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.security import SecurityService
from backend.application.services.token_management_service import TokenManagementService
from backend.application.commands.attorney import RefreshTokenCommand
from backend.application.dto.attorney import TokenResponse
from backend.core.settings import settings
from backend.core.exceptions import ValidationException
from backend.core.logger import logger


class RefreshTokenUseCase:
    '''
    UseCase для обновления access token по refresh token.

    Flow:
    1. Декодировать refresh token
    2. Проверить тип токена (должен быть 'refresh')
    3. Получить attorney_id из токена
    4. Проверить что refresh token существует в Redis
    5. Создать новый access token
    6. Вернуть новый access token (refresh token остается прежним)
    '''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory
        self.token_service = TokenManagementService()

    async def execute(self, cmd: RefreshTokenCommand) -> TokenResponse:
        try:
            # 1. Декодировать refresh token
            payload = SecurityService.decode_token(cmd.refresh_token)

            # 2. Проверить тип токена
            if not SecurityService.verify_token_type(payload, 'refresh'):
                raise ValidationException(
                    'Неправильный тип токена. Ожидается refresh token'
                )

            # 3. Получить attorney_id из токена
            attorney_id_str = SecurityService.get_subject_from_token(payload)
            attorney_id = int(attorney_id_str)

            # 4. Проверить что refresh token существует в Redis
            stored_token = await self.token_service.get_refresh_token(attorney_id)
            if stored_token != cmd.refresh_token:
                raise ValidationException('Refresh token не найден или недействителен')

            # 5. Проверить что адвокат существует и активен
            async with self.uow_factory.create() as uow:
                attorney = await uow.attorney_repo.get(attorney_id)
                if not attorney:
                    raise ValidationException('Адвокат не найден')
                if not attorney.is_active:
                    raise ValidationException('Учетная запись адвоката заблокирована')

            # 6. Создать новый access token
            access_token = SecurityService.create_access_token(str(attorney_id))

            logger.info(f'Access token обновлен для адвоката ID: {attorney_id}')

            # 7. Вернуть новый access token (refresh token остается прежним)
            return TokenResponse(
                access_token=access_token,
                refresh_token=cmd.refresh_token,  # Возвращаем тот же refresh token
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )

        except ValueError as e:
            logger.warning(f'Ошибка при обновлении токена: {e}')
            raise ValidationException(f'Невалидный refresh token: {str(e)}')
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f'Неожиданная ошибка при обновлении токена: {e}')
            raise ValidationException('Ошибка при обновлении токена')
