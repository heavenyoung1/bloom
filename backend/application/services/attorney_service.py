from backend.infrastructure.tools.uow import AsyncUnitOfWork
from backend.application.dto.attorney import (
    CreateAttorneyDTO,
    UpdateAttorneyDTO,
    AttorneyResponseDTO,
    AttorneyListItemDTO,
)
from backend.domain.entities.attorney import Attorney
from backend.application.validators.attorney_validator import AttorneyValidator
from backend.domain.factories.attorney_factory import AttorneyFactory
from backend.core.exceptions import EntityNotFoundException, ValidationException
from backend.core.logger import logger
import hashlib


class AttorneyService:
    '''Service для работы с юристами'''

    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow
        self.validator = AttorneyValidator(uow.attorney_repo)
        self.factory = AttorneyFactory()

    async def create_attorney(self, data: CreateAttorneyDTO) -> 'AttorneyResponseDTO':
        '''
        Создать нового юриста.

        Шаги:
        1. Валидируем данные (Validator)
        2. Создаём Entity (Factory)
        3. Сохраняем через Repository (UoW)
        4. Возвращаем DTO
        '''

        # 1. Валидация
        await self.validator.validate_on_create(data)

        # 2. Создание Entity через Factory
        attorney = self.factory.create(
            license_id=data.attorney_id,
            first_name=data.first_name,
            last_name=data.last_name,
            patronymic=data.patronymic,
            email=data.email,
            phone=data.phone,
            password_hash=data.password,  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        )

        # 3. Сохраняем в БД
        saved_attorney = await self.uow.attorney_repo.save(attorney)

        # ТУТ ВОПРОСИКИ!! ПРОВЕРИТЬ ЧТО ВОЗВРАЩАЕТ!!!!
        return AttorneyResponseDTO.model_validate(saved_attorney)

    async def get_attorney(self, attorney_id: int) -> AttorneyResponseDTO:
        '''Получить Юриста по ID.'''
        attorney = await self.uow.attorney_repo.get(attorney_id)
        # КАК ВАЛИДИРОВАТЬ ТО?
        await self.validator.validate_on_create()
