import pytest

from backend.application.dto.attorney import (
    RegisterRequest,
    UpdateRequest,
    AttorneyResponse,
)

from backend.application.dto.client import (
    ClientCreateRequest,
)


@pytest.fixture
async def valid_attorney_dto():
    return RegisterRequest(
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
    return RegisterRequest(
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
    return UpdateRequest(
        license_id='321/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan12231@example.com',
        phone='+79991234567',
    )


@pytest.fixture
async def valid_client_dto():
    return ClientCreateRequest(
        name='Иванов Иван Иванович',
        type=True,
        email='client@example.com',
        phone='+79991234567',
        personal_info='1212 443443',
        address='г. Москва, ул. Пушкина, д.1',
        messenger='Telegram',
        messenger_handle='@client123',
    )