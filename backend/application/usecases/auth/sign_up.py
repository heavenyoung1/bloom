from backend.infrastructure.repositories.attorney_repo import AttorneyRepository
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.security import SecurityService
from backend.domain.factories.attorney_factory import AttorneyFactory
from backend.application.validators.attorney_validator import AttorneyValidator
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
        self.factory = AttorneyFactory()  # Фабрика для создания сущностей

    async def execute(self, request: RegisterRequest) -> AttorneyResponse:
        '''Регистрация нового юриста'''
        # 1. Получить UoW (транзакция + все репозитории)
        async with self.uow_factory.create() as uow:

            # 2. Валидировать данные
            validator = AttorneyValidator(uow.attorney_repo)
            await validator.on_create(request)

            # 3. Захэшировать пароль
            hashed_password = SecurityService.hash_password(request.password)

            # Создание юриста через Фабрику
            attorney = self.factory.create(
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
        verification_code = '123456'  # В реальности генерируется случайно
        await redis_client.set(
            RedisKeys.email_verification_code(request.email),
            verification_code,
            ttl=900,  # 15 минут Что это?
        )

        logger.info(f'Юрист зарегистрирован: {attorney.email}')

        return AttorneyResponse.model_validate(attorney)
