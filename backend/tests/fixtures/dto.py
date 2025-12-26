import pytest

from backend.application.dto.attorney import (
    RegisterRequest,
    UpdateRequest,
    VerifyEmailRequest,
    AttorneyResponse,
    LoginRequest,
    ChangePasswordDTO,
)

from backend.application.dto.client import (
    ClientCreateRequest,
)

from backend.application.dto.case import (
    CaseCreateRequest,
)

from backend.application.dto.event import (
    EventCreateRequest,
)


@pytest.fixture
async def valid_attorney_dto():
    return RegisterRequest(
        license_id='322/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan@example.com',
        telegram_username='advokat1234',
        phone='+79991234567',
        password='SecurePass123!',
    )


@pytest.fixture
async def valid_login_attorney_dto():
    return LoginRequest(
        email='ivan@example.com',
        password='SecurePass123!',
    )


@pytest.fixture
def change_password_dto():
    return ChangePasswordDTO(
        current_password='SecurePass123!',
        new_password='SecurePass456!',
    )


@pytest.fixture
async def valid_login_new_password_attorney_dto():
    return LoginRequest(
        email='ivan@example.com',
        password='SecurePass456!',
    )


@pytest.fixture
async def valid_verification_attorney_dto(code: str):
    return VerifyEmailRequest(
        email='ivan@example.com',
        code=code,
    )


@pytest.fixture
async def invalid_login_attorney_dto():
    return LoginRequest(
        email='ivan666@example.com',
        password='SecurePass1235!',
    )


@pytest.fixture
async def valid_attorney_dto_second():
    return RegisterRequest(
        license_id='111/2222',
        first_name='Александр',
        last_name='Иванов',
        patronymic='Дмитриевич',
        email='alexander@example.com',
        telegram_username='advokat123678',
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
        telegram_username='advokat1231425',
        phone='+79991234567',
    )


@pytest.fixture
async def valid_client_dto():
    return ClientCreateRequest(
        name='Иванов Иван Иванович',
        type=True,
        email='client@example.com',
        telegram_username='advweft1234',
        phone='+79991234567',
        personal_info='1212 443443',
        address='г. Москва, ул. Пушкина, д.1',
        messenger='Telegram',
        messenger_handle='@client123',
    )


@pytest.fixture
def valid_case_dto():
    return CaseCreateRequest(
        name='Спор об имуществе, для теста',
        client_id=1,  # будет переопределен в тестах
        status='Новое',
        description='Тестовое описание тестового дела',
    )


@pytest.fixture
def valid_event_dto(sample_date):
    return EventCreateRequest(
        case_id=1,
        description='Рассмотрение дела по существу',
        event_date=sample_date,
        event_type='Судебное заседание',
        name='Заседание суда',
    )
