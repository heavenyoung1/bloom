import pytest

from backend.application.dto.attorney import (
    CreateAttorneyDTO,
    UpdateAttorneyDTO,
)


@pytest.fixture
async def valid_attorney_dto():
    return CreateAttorneyDTO(
        license_id='153/3232',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan@example.com',
        phone='+79991234567',
        password='SecurePass123!',
    )
