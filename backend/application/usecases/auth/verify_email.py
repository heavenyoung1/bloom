from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.attorney import VerifyEmailRequest
from backend.application.services.verification_service import VerificationService
from backend.application.services.attorney_service import AttorneyService
from backend.application.dto.attorney import AttorneyVerificationResponse
from backend.core.exceptions import NotFoundException, VerificationError
from backend.core.logger import logger


class VerifyEmailUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory
        self.attorney_service = AttorneyService(uow_factory)

    async def execute(
        self, request: VerifyEmailRequest
    ) -> AttorneyVerificationResponse:
        '''Верифицировать email по коду.'''

        # 1. Проверяем код через VerificationService
        is_valid = await VerificationService.verify_code(
            email=request.email,
            code=request.code,
        )
        if not is_valid:
            raise VerificationError('Неправильный или истёкший код')

        # 2. Помечаем юриста как верифицированного через AttorneyService
        logger.info(f'[DEBUGAUTH] ТУТ ВЫПОЛНЯЕТСЯ!')
        response = await self.attorney_service.set_verified(request.email)

        # 3. Чистим код в Redis
        await VerificationService.cleanup_code(request.email)

        logger.info(f'Email подтверждён: {request.email}')

        return response
