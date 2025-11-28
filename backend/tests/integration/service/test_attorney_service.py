import pytest

from backend.application.services.attorney_service import AttorneyService
from backend.core.logger import logger


class TestAttorneyService:
    @pytest.mark.asyncio
    async def test_create_attorney(self, test_uow_factory, attorney_service, valid_attorney_dto):
        # Вызываем метод сервиса — он сам откроет test_uow_factory.create()
        created_attorney = await attorney_service.create_attorney(valid_attorney_dto)

        # Проверка, что юрист был создан
        logger.info(f'TestAttorneyService -> Юрист создан.')
        assert created_attorney.id is not None
