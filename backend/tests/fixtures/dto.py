import pytest

from backend.application.dto.attorney import (
    CreateAttorneyDTO,
    UpdateAttorneyDTO,
)


@pytest.fixture
async def valid_attorney_dto():
    return CreateAttorneyDTO(
        license_id='322/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan@example.com',
        phone='+79991234567',
        password='SecurePass123!',
    )


@pytest.fixture
async def valid_attorney_dto_second():
    return CreateAttorneyDTO(
        license_id='111/2222',
        first_name='Александр',
        last_name='Иванов',
        patronymic='Дмитриевич',
        email='alexander@example.com',
        phone='+79998887766',
        password='hash232343244',
    )


@pytest.fixture
async def update_attorney_dto():
    return UpdateAttorneyDTO(
        license_id='321/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan12231@example.com',
        phone='+79991234567',
    )
