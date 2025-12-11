from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.attorney import VerifyEmailRequest
from backend.application.services.verification_service import VerificationService
from backend.application.services.attorney_service import AttorneyService
from backend.application.dto.attorney import AttorneyVerificationResponse
from backend.core.exceptions import NotFoundException, VerificationError
from backend.core.logger import logger
from backend.application.commands.attorney import (
    VerifyEmailCommand,
    ResendVerificationCommand,
)
from backend.application.dto.attorney import AttorneyResponse
from backend.core.exceptions import ValidationException, EntityNotFoundException

class VerifyEmailUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory
        self.attorney_service = AttorneyService(uow_factory)

    async def execute(
        self, 
        cmd: VerifyEmailCommand,
    ) -> AttorneyVerificationResponse:
        '''
        Верифицировать email по коду.

        Flow:
        1. Проверить валидность кода верификации
        2. Пометить юриста как верифицированного
        3. Очистить код из Redis
        '''
        # 1. Проверить код
        is_valid = await VerificationService.verify_code(
            email=cmd.email,
            code=cmd.code,
        )
        if not is_valid:
            raise ValidationException('Неправильный или истёкший код верификации')

        async with self.uow_factory.create() as uow:
            # 2. Получить юриста и обновить статус
            attorney = await uow.attorney_repo.get_by_email(cmd.email)
            if not attorney:
                raise EntityNotFoundException(
                    f'Адвокат с email {cmd.email} не найден'
                )

            # Уже верифицирован?
            if attorney.is_verified:
                raise ValidationException('Email уже верифицирован')

            # Пометить как верифицированного
            attorney.is_verified = True
            await uow.attorney_repo.save(attorney)

        # 3. Очистить код в Redis
        await VerificationService.cleanup_code(cmd.email)

        logger.info(f'Email успешно верифицирован: {cmd.email} (ID: {attorney.id})')

        return AttorneyResponse.model_validate(attorney)
