from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.attorney import VerifyEmailRequest
from backend.application.services.verification_service import VerificationService
from backend.core.logger import logger


class VerifyEmailUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, request: VerifyEmailRequest) -> dict:
        """Верифицировать email по коду"""

        # 1. Проверить код
        is_valid = await VerificationService.verify_code(
            email=request.email, code=request.code
        )

        if not is_valid:
            raise ValueError('Неправильный или истёкший код')

        # 2. Обновить БД
        async with self.uow_factory.create() as uow:
            attorney = await uow.attorney_repo.get_by_email(request.email)
            if not attorney:
                raise ValueError('Юрист не найден')

            if attorney.is_verified:
                raise ValueError('Email уже подтвержден')

            # Обновляем напрямую в ORM
            # (в production нужно добавить метод update в репозиторий)
            stmt = (
                __import__('sqlalchemy')
                .select(
                    __import__(
                        'backend.infrastructure.models.attorney',
                        fromlist=['AttorneyORM'],
                    ).AttorneyORM
                )
                .where(
                    __import__(
                        'backend.infrastructure.models.attorney',
                        fromlist=['AttorneyORM'],
                    ).AttorneyORM.id
                    == attorney.id
                )
            )
            result = await uow.session.execute(stmt)
            orm_attorney = result.scalars().first()
            orm_attorney.is_verified = True

            # Очистить код из Redis
            await VerificationService.cleanup_code(request.email)

        logger.info(f'Email подтвержден: {request.email}')

        return {'message': 'Email успешно подтвержден', 'email': request.email}
