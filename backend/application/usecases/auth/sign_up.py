from backend.infrastructure.repositories.attorney_repo import AttorneyRepository
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.domain.entities.attorney import Attorney
from backend.core.security import SecurityService
from backend.application.policy.attorney_policy import AttorneyPolicy
from backend.application.services.verification_service import VerificationService
from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys

from backend.application.dto.attorney import (
    AttorneyResponse,
    RegisterRequest,
    LoginRequest,
    UpdateRequest,
)

from backend.core.logger import logger


class SignUpUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, request: RegisterRequest) -> AttorneyResponse:
        '''
        Регистрация нового юриста.

        Flow:
        1. Валидировать данные через Policy
        2. Захешировать пароль
        3. Создать Entity
        4. Сохранить в БД
        5. Отправить код верификации
        '''
        async with self.uow_factory.create() as uow:

            # 2. Валидировать данные
            validator = AttorneyPolicy(uow.attorney_repo)
            await validator.on_create(request)

            # 3. Захэшировать пароль
            hashed_password = SecurityService.hash_password(request.password)

            # Создание юриста через Фабрику
            attorney = Attorney.create(
                license_id=request.license_id,
                first_name=request.first_name,
                last_name=request.last_name,
                patronymic=request.patronymic,
                email=request.email,
                phone=request.phone,
                hashed_password=hashed_password,
            )

            # 5. Сохранить в БД
            attorney = await uow.attorney_repo.save(attorney)

        # 6. Сгенерировать код верификации (в реальности - случайный)
        await VerificationService.send_verification_code(
            email=request.email, first_name=request.first_name
        )

        logger.info(f'Юрист зарегистрирован: {attorney.email}. Ожидание верификации...')

        return AttorneyResponse.model_validate(attorney)
