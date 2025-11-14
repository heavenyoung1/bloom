from backend.infrastructure.tools.uow import AsyncUnitOfWork
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
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

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory  # Используем фабрику для создания UoW
        self.validator = AttorneyValidator(
            uow_factory.attorney_repo
        )  # Валидатор использует репозиторий из фабрики
        self.factory = AttorneyFactory()  # Фабрика для создания сущностей

    async def create_attorney(self, data: CreateAttorneyDTO) -> 'AttorneyResponseDTO':
        '''
        Создать нового юриста.

        Шаги:
        1. Валидируем данные (Validator)
        2. Создаём Entity (Factory)
        3. Сохраняем через Repository (UoW)
        4. Возвращаем DTO
        '''

        # 1. Валидация через Validator
        await self.validator.validate_on_create(data)

        # 1.1 ТУТ ДОЛЖНА БЫТЬ ХЕШИРОВАНИЕ ПАРОЛЯ

        # 3. Создание Entity через Factory
        attorney = self.factory.create(
            license_id=data.license_id,
            first_name=data.first_name,
            last_name=data.last_name,
            patronymic=data.patronymic,
            email=data.email,
            phone=data.phone,
            password_hash=data.password,  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        )

        # 4. Используем фабрику для создания UoW и работы с репозиториями
        async with self.uow_factory.create() as uow:
            # Сохраняем юриста в БД через репозиторий из UoW
            saved_attorney = await uow.attorney_repo.save(attorney)

        # ТУТ ВОПРОСИКИ!! ПРОВЕРИТЬ ЧТО ВОЗВРАЩАЕТ!!!!
        logger.info(
            f'Юрист создан: ID={saved_attorney.id}, Email={saved_attorney.email}'
        )
        return AttorneyResponseDTO.model_validate(saved_attorney)

    async def get_attorney(self, attorney_id: int) -> AttorneyResponseDTO:
        '''Получить Юриста по ID.'''
        # Используем фабрику для создания UoW и работы с репозиториями
        async with self.uow_factory.create() as uow:
            # Получаем юриста по ID через репозиторий из UoW
            attorney = await uow.attorney_repo.get(attorney_id)

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
        # Используем фабрику для создания UoW и работы с репозиториями
        async with self.uow_factory.create() as uow:
            # Получаем всех юристов через репозиторий из UoW
            attorneys = await uow.attorney_repo.get_all()

        # Преобразуем каждого в DTO
        return [AttorneyListItemDTO.model_validate(a) for a in attorneys]

    async def update_attorney(
        self, attorney_id: int, data: UpdateAttorneyDTO
    ) -> AttorneyResponseDTO:
        # Используем фабрику для создания UoW и работы с репозиториями
        async with self.uow_factory.create() as uow:
            # Получаем существующего юриста
            attorney = await uow.attorney_repo.get(attorney_id)

        if not attorney:
            logger.warning(f'Юрист ID {attorney_id} не найден')
            raise EntityNotFoundException(f'Юрист с ID {attorney_id} не найден')
        # 2. Проверка существования происходит в репозитории!
        # 3. Валидируем изменения (если меняем email - проверяем уникальность)
        if data.email != attorney.email:
            pass

            # Обновляем поля юриста
            attorney.first_name = data.first_name
            attorney.last_name = data.last_name
            attorney.patronymic = data.patronymic
            attorney.email = data.email
            attorney.phone = data.phone

            # Сохраняем изменения
            saved_attorney = await uow.attorney_repo.save(attorney)

            # Возвращаем обновленный DTO
            return AttorneyResponseDTO.model_validate(saved_attorney)
