from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.attorney import ResetPasswordCommand
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.application.dto.attorney import PasswordResetResponse
from backend.core.security import SecurityService
from backend.application.services.verification_service import VerificationService
from backend.application.services.token_management_service import TokenManagementService

from backend.core.logger import logger


class ResetPasswordUseCase:
    def __init__(
            self, 
            uow_factory: UnitOfWorkFactory,
            token_service: TokenManagementService,
            ):
        self.uow_factory = uow_factory
        self.token_service = token_service
        

    async def execute(self, cmd: ResetPasswordCommand):
        try:
            # 1. Проверить rate limiting
            await self.token_service.check_rate_limit(cmd.email)

            # 1. Проверить код верификации
            ok = await VerificationService.verify_code(cmd.email, cmd.code)
            if not ok:
                await self.token_service.record_failed_attempt(cmd.email)
                raise ValidationException('Неверный или истёкший код')

            # 2. Очистить код из Redis (чтобы его нельзя было использовать повторно)
            await VerificationService.cleanup_code(cmd.email)

            async with self.uow_factory.create() as uow:

                # 2. Получить юриста по email
                attorney = await uow.attorney_repo.get_by_email(cmd.email)
                if not attorney:
                    # Записать попытку
                    await self.token_service.record_failed_attempt(cmd.email)
                    raise ValidationException('Некорректный email')
                
                # 3. Захешировать пароль
                hashed_password = SecurityService.hash_password(cmd.new_password)

                attorney.hashed_password = hashed_password

                await uow.attorney_repo.update(attorney)
                # Коммит произойдет автоматически при выходе из контекстного менеджера

        except (ValidationException, EntityNotFoundException) as e:
            logger.error(f'Ошибка при сбросе пароля юриста: {e}')
            raise

        logger.info(f'Пароль изменен: {cmd.email}')

        return PasswordResetResponse(ok=True)
    



