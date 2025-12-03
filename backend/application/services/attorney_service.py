# from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
# from backend.application.dto.attorney import (
#     AttorneyCreate,
#     AttorneyRead,
#     AttorneyUpdate,
# )
# from backend.domain.entities.attorney import Attorney
# from backend.application.validators.attorney_validator import AttorneyValidator
# from backend.domain.factories.attorney_factory import AttorneyFactory
# from backend.core.exceptions import EntityNotFoundException, ValidationException
# from backend.core.logger import logger
# import hashlib


# class AttorneyService:
#     '''Service для работы с юристами'''

#     def __init__(self, uow_factory: UnitOfWorkFactory):
#         self.uow_factory = uow_factory  # Используем фабрику для создания UoW
#         # self.validator = AttorneyValidator(
#         #     uow_factory.attorney_repo
#         # )  # Валидатор использует репозиторий из фабрики
#         self.factory = AttorneyFactory()  # Фабрика для создания сущностей

#     async def create_attorney(self, data: AttorneyCreate) -> 'AttorneyRead':
#         '''
#         Создать нового юриста.

#         Шаги:
#         1. Создаём UoW через фабрику
#         2. Валидируем данные
#         3. Хешируем пароль
#         4. Создаём Entity
#         5. Сохраняем в БД
#         6. Возвращаем DTO
#         '''

#         # 1. Создаём UoW через фабрику (получаем все репозитории)
#         async with self.uow_factory.create() as uow:

#             # 2. Инициализируем валидатор с репозиторием из UoW
#             validator = AttorneyValidator(uow.attorney_repo)

#             # 3. Валидируем данные
#             await validator.validate_on_create(data)

#             # 4 ТУТ ДОЛЖНА БЫТЬ ХЕШИРОВАНИЕ ПАРОЛЯ

#             # 5. Создаём Entity через Factory
#             attorney = self.factory.create(
#                 license_id=data.license_id,
#                 first_name=data.first_name,
#                 last_name=data.last_name,
#                 patronymic=data.patronymic,
#                 email=data.email,
#                 phone=data.phone,
#                 hashed_password=data.hashed_password,
#             )

#             # 6. Сохраняем в БД
#             saved_attorney = await uow.attorney_repo.save(attorney)

#             logger.info(
#                 f'Юрист создан: ID={saved_attorney.id}, Email={saved_attorney.email}'
#             )

#             # 7. Преобразуем в DTO и возвращаем
#             return AttorneyRead.model_validate(saved_attorney)

#     async def get_attorney(self, attorney_id: int) -> AttorneyRead:
#         '''Получить Юриста по ID.'''
#         # Используем фабрику для создания UoW и работы с репозиториями
#         async with self.uow_factory.create() as uow:
#             # Получаем юриста по ID через репозиторий из UoW
#             attorney = await uow.attorney_repo.get(attorney_id)

#         if not attorney:
#             logger.warning(f'Юрист ID {attorney_id} не найден.')
#             raise EntityNotFoundException(f'Юрист с ID {attorney_id}')

#         # Преобразуем в DTO и возвращаем
#         return AttorneyRead.model_validate(attorney)

#     # async def get_all_attorneys(self) -> list[AttorneyResponseDTO]:
#     #     '''
#     #     Получить всех юристов.

#     #     Returns:
#     #         Список AttorneyListItemDTO (облегчённая версия)
#     #     '''
#     #     # Используем фабрику для создания UoW и работы с репозиториями
#     #     async with self.uow_factory.create() as uow:
#     #         # Получаем всех юристов через репозиторий из UoW
#     #         attorneys = await uow.attorney_repo.get_all()

#     #     # Преобразуем каждого в DTO
#     #     return [AttorneyResponseDTO.model_validate(a) for a in attorneys]

#     async def update_attorney(
#         self, attorney_id: int, data: AttorneyUpdate
#     ) -> AttorneyRead:
#         # Используем фабрику для создания UoW и работы с репозиториями
#         async with self.uow_factory.create() as uow:
#             # Получаем существующего юриста
#             attorney = await uow.attorney_repo.get(attorney_id)

#             if not attorney:
#                 logger.warning(f'Юрист ID {attorney_id} не найден')
#                 raise EntityNotFoundException(f'Юрист с ID {attorney_id} не найден')
#             # 2. Проверка существования происходит в репозитории!
#             # 3. Валидируем изменения (если меняем email - проверяем уникальность)
#             if data.email != attorney.email:
#                 pass

#             # Обновляем поля юриста
#             attorney.license_id = data.license_id
#             attorney.first_name = data.first_name
#             attorney.last_name = data.last_name
#             attorney.patronymic = data.patronymic
#             attorney.email = data.email
#             attorney.phone = data.phone

#             # Сохраняем изменения
#             saved_attorney = await uow.attorney_repo.update(attorney)

#             # Возвращаем обновленный DTO
#             return AttorneyRead.model_validate(saved_attorney)
