from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.attorney import ResendVerificationRequest
from backend.application.services.verification_service import VerificationService
from backend.core.logger import logger


class ResendVerificationUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, request: ResendVerificationRequest) -> dict:
        '''Повторно отправить код верификации'''

        async with self.uow_factory.create() as uow:

            # 1. Проверить, существует ли такой юрист
            attorney = await uow.attorney_repo.get_by_email(request.email)
            if not attorney:
                # ⚠️ Security: не раскрываем, существует ли email
                raise ValueError('Если такой email зарегистрирован, код отправлен')

            # 2. Проверить, не подтвержден ли уже
            if attorney.is_verified:
                raise ValueError('Этот email уже подтвержден')

            # 3. Отправить новый код
            await VerificationService.send_verification_code(
                email=request.email, first_name=attorney.first_name
            )

        logger.info(f'Код повторно отправлен на: {request.email}')

        return {'message': 'Код отправлен на вашу почту', 'email': request.email}
