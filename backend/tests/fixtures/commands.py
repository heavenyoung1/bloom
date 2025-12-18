import pytest

from backend.application.commands.case import CreateCaseCommand, UpdateCaseCommand
from backend.application.commands.client import CreateClientCommand, UpdateClientCommand
from backend.application.commands.event import (
    CreateEventCommand,
    UpdateEventCommand,
)


@pytest.fixture
def create_case_command(sample_case_for_verified_attorney):
    return CreateCaseCommand(
        name='Дело о краже',
        client_id=sample_case_for_verified_attorney.client_id,  # Реальный ID из БД
        attorney_id=sample_case_for_verified_attorney.attorney_id,  # Реальный ID из БД
        status=sample_case_for_verified_attorney.status,
        description=sample_case_for_verified_attorney.description,
    )


@pytest.fixture
def update_case_command(sample_case_for_verified_attorney):
    return UpdateCaseCommand(
        case_id=None,
        name='Дело о падении камня',
        client_id=sample_case_for_verified_attorney.client_id,  # Реальный ID из БД
        attorney_id=sample_case_for_verified_attorney.attorney_id,  # Реальный ID из БД
        status=sample_case_for_verified_attorney.status,
        description='Произошло что-то непонятное',
    )


@pytest.fixture
def create_client_command(verifiied_persisted_attorney_id):
    return CreateClientCommand(
        name='АО Булочки и Пирожки товарища Ульянова и Джугашвили',
        type=True,
        email='leninandstalin@limited.com',
        phone='+79103353535',
        personal_info='12345678910',
        address='США, шт. Флорида, г. Майами ул. Ленина, д 55, кв. 32',
        messenger='MAX',
        messenger_handle='@sirLeninGuy',
        owner_attorney_id=verifiied_persisted_attorney_id,
    )


@pytest.fixture
def update_client_command(verifiied_persisted_attorney_id):
    return UpdateClientCommand(
        client_id=None,
        name='АО Булочки и Пирожки товарища Ульянова',
        type=True,
        email='lenin@limited.com',
        phone='+79103351422',
        personal_info='12345678910',
        address='США, шт. Флорида, г. Майами ул. Ленина, д 55, кв. 33',
        messenger='MAX',
        messenger_handle='@GayLeninGuy',
        owner_attorney_id=verifiied_persisted_attorney_id,
    )


@pytest.fixture
def create_event_command(persisted_case, persisted_attorney_id, sample_date):
    return CreateEventCommand(
        name='Судебное заседание',
        description='Продолжение суда, перенесенного в прошлый раз.',
        event_type='Судебное заседание',
        event_date=sample_date,
        case_id=persisted_case,
        attorney_id=persisted_attorney_id,
    )


@pytest.fixture
def update_event_command(sample_date):
    # event_id проставим уже в тесте после создания
    return UpdateEventCommand(
        event_id=None,
        name='Встреча с клиентом',
        description='',
        event_type='Встреча',
        event_date=sample_date,
    )
