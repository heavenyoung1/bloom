import pytest

from backend.application.services.attorney_service import AttorneyService
from backend.core.logger import logger

from backend.core.exceptions import EntityNotFoundException, ValidationException


class TestAttorneyService:
    @pytest.mark.asyncio
    async def test_create_attorney(self, attorney_service, valid_attorney_dto):
        # Вызываем метод сервиса — он сам откроет test_uow_factory.create()
        created_attorney = await attorney_service.create_attorney(valid_attorney_dto)

        # Проверка, что юрист был создан
        logger.info(f'TestAttorneyService -> Юрист создан.')
        assert created_attorney.id is not None
        assert created_attorney.license_id == valid_attorney_dto.license_id

    @pytest.mark.asyncio
    async def test_create_duplicate_attorney(
        self, attorney_service, valid_attorney_dto
    ):
        # Вызываем метод сервиса — он сам откроет test_uow_factory.create()
        created_attorney_first = await attorney_service.create_attorney(
            valid_attorney_dto
        )

        # Проверка, что юрист был создан
        logger.info(f'TestAttorneyService -> Юрист создан.')
        assert created_attorney_first.id is not None
        with pytest.raises(ValidationException) as exc_info:
            await attorney_service.create_attorney(valid_attorney_dto)

    @pytest.mark.asyncio
    async def test_get_attorney(self, attorney_service, valid_attorney_dto):
        # Вызываем метод сервиса — он сам откроет test_uow_factory.create()
        created_attorney = await attorney_service.create_attorney(valid_attorney_dto)

        # Проверка, что юрист был создан
        logger.info(f'TestAttorneyService -> Юрист создан.')
        assert created_attorney.id is not None

        get_attorney = await attorney_service.get_attorney(created_attorney.id)
        assert get_attorney.id is not None

    @pytest.mark.asyncio
    async def test_get_attorney(self, attorney_service, valid_attorney_dto):
        logger.info(f'TestAttorneyService -> Получаем несуществующего юриста.')
        not_found_id = 1234245234
        with pytest.raises(EntityNotFoundException) as exc_info:
            await attorney_service.get_attorney(not_found_id)

            # Проверяем тип исключения
        assert isinstance(exc_info.value, EntityNotFoundException)

        # Проверяем текст ошибки
        assert str(exc_info.value) == f'Юрист с ID {not_found_id} не найден.'
