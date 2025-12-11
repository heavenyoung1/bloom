from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.attorney import ResendVerificationRequest
from backend.application.services.verification_service import VerificationService
from backend.application.dto.attorney import AttorneyResponse
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.application.commands.attorney import (
    VerifyEmailCommand,
    ResendVerificationCommand,
)
from backend.core.logger import logger


class ResendVerificationUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, cmd: ResendVerificationCommand) -> dict:
        '''
        Повторно отправить код верификации.

        Flow:
        1. Проверить существование юриста
        2. Проверить, не верифицирован ли уже
        3. Отправить новый код
        '''

        async with self.uow_factory.create() as uow:
            # 1. Получить юриста
            attorney = await uow.attorney_repo.get_by_email(cmd.email)
            if not attorney:
                # ⚠️ Security: не раскрываем, существует ли email
                logger.warning(
                    f'Попытка переотправить код на несуществующий email: {cmd.email}'
                )
                raise ValidationException(
                    'Если такой email зарегистрирован, код был отправлен'
                )

            # 2. Проверить, не подтвержден ли уже
            if attorney.is_verified:
                raise ValueError('Этот email уже подтвержден')

        # 3. Отправить новый код (вне транзакции)
        await VerificationService.send_verification_code(
            email=cmd.email, first_name=attorney.first_name
        )

        logger.info(f'Код повторно отправлен на: {cmd.email}')

        return {
            'message': 'Код верификации отправлен на вашу почту',
            'email': cmd.email,
        }
