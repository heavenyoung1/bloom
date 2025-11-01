from datetime import datetime
import pytest
from backend.domain.entities.case import Case  # Импортируем ваш класс Case


@pytest.fixture
async def sample_case(sample_attorney, sample_client):
    '''Фикстура для дефолтного дела с реальными attorney_id и client_id.'''
    return Case(
        id=None,
        name='Дело о краже',
        client_id=sample_client.id,  # Реальный ID из БД
        attorney_id=sample_attorney.id,  # Реальный ID из БД
        status='В процессе',
        description='Описание дела о краже',
    )


@pytest.fixture
async def sample_update_case(sample_attorney_for_update, sample_client_for_update):
    '''Фикстура для дела, которое будет обновляться.'''
    return Case(
        id=None,
        name='Дело о мошенничестве',
        client_id=sample_client_for_update.id,  # Реальный ID из БД
        attorney_id=sample_attorney_for_update.id,  # Реальный ID из БД
        status='Закрыто',
        description='Описание обновленного дела о мошенничестве',
    )


@pytest.fixture
async def cases_list(sample_attorney, sample_client):
    '''
    Фикстура: список дел для тестирования.
    Использует одних и тех же attorney и client для всех дел.
    '''
    return [
        Case(
            id=None,
            name='Дело о краже',
            client_id=sample_client.id,
            attorney_id=sample_attorney.id,
            status='В процессе',
            description='Описание дела о краже',
        ),
        Case(
            id=None,
            name='Дело о мошенничестве',
            client_id=sample_client.id,
            attorney_id=sample_attorney.id,
            status='Закрыто',
            description='Описание дела о мошенничестве',
        ),
        Case(
            id=None,
            name='Дело о нападении',
            client_id=sample_client.id,
            attorney_id=sample_attorney.id,
            status='В процессе',
            description='Описание дела о нападении',
        ),
        Case(
            id=None,
            name='Дело о разбирательстве',
            client_id=sample_client.id,
            attorney_id=sample_attorney.id,
            status='Ожидает решения',
            description='Описание дела о разбирательстве',
        ),
        Case(
            id=None,
            name='Дело о ДТП',
            client_id=sample_client.id,
            attorney_id=sample_attorney.id,
            status='Закрыто',
            description='Описание дела о ДТП',
        ),
    ]
