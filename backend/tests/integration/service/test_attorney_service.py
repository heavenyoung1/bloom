import pytest

from backend.application.services.attorney_service import AttorneyService
from backend.core.logger import logger


@pytest.mark.asyncio
class TestAttorneyService:

    async def test_create_attorney(self, attorney_service, valid_attorney_dto):

        # Создание юриста через сервис
        created_attorney = await attorney_service.create_attorney(valid_attorney_dto)

        # Проверка, что юрист был создан
        logger.info(f'ЮРИСТ СОЗ')
        assert created_attorney.id is not None
