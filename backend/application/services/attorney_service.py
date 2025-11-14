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
            license_id=data.license_id,
            first_name=data.first_name,
            last_name=data.last_name,
            patronymic=data.patronymic,
            email=data.email,
            phone=data.phone,
            password_hash=data.password,  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        )

        # 3. Сохраняем в БД
        # Repository.save() возвращает полный объект с ID и временами
        saved_attorney = await self.uow.attorney_repo.save(attorney)
        # saved_attorney = Attorney(
        #     id=1,  # ← БД назначила!
        #     license_id='АД123456',
        #     password_hash='sha256xxx',
        #     created_at=datetime.now(),  # ← БД установила
        #     updated_at=datetime.now()   # ← БД установила
        # )

        # ТУТ ВОПРОСИКИ!! ПРОВЕРИТЬ ЧТО ВОЗВРАЩАЕТ!!!!
        logger.info(f'Юрист создан: ID={saved_attorney.id}, Email={saved_attorney.email}')
        return AttorneyResponseDTO.model_validate(saved_attorney)

    async def get_attorney(self, attorney_id: int) -> AttorneyResponseDTO:
        '''Получить Юриста по ID.'''
        # 1. Получаем из БД
        attorney = await self.uow.attorney_repo.get(attorney_id)

        if not attorney:
            logger.warning(f'Юрист ID {attorney_id} не найден')
            raise EntityNotFoundException(f'Юрист с ID {attorney_id} не найден')

        # Преобразуем в DTO и возвращаем
        return AttorneyResponseDTO.model_validate(attorney)

    async def get_all_attorneys(self) -> list[AttorneyListItemDTO]:
        '''
        Получить всех юристов.
        
        Returns:
            Список AttorneyListItemDTO (облегчённая версия)
        '''
        # Получаем всех юристов
        attorneys = await self.uow.attorney_repo.get_all()
        
        # Преобразуем каждого в DTO
        return [AttorneyListItemDTO.model_validate(a) for a in attorneys]
    
    # async def update_attorney(
    #         self,
    #         attorney_id: int,
    #         data: UpdateAttorneyDTO
    # ) -> AttorneyResponseDTO:
    #     # 1. Получаем существующего юриста
    #     attorney = await self.uow.attorney_repo.get(attorney_id)

    #     # 2. Проверка существования происходит в репозитории!
    #     # 3. Валидируем изменения (если меняем email - проверяем уникальность)
    #     if data.email != attorney.email:
    #         pass