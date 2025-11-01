from datetime import datetime
import pytest
from backend.domain.entities.case import Case  # Импортируем ваш класс Case

# Фикстура для дефолтного дела
@pytest.fixture
def sample_case(fixed_now):
    '''Фикстура для дефолтного дела.'''
    return Case(
        id=None,  # Позволяем БД генерировать ID
        name='Дело о краже',
        client_id='client-1',
        attorney_id='attorney-1',
        status='В процессе',
        description='Описание дела о краже',
    )


# Фикстура для дела, которое будет обновляться
@pytest.fixture
def sample_update_case(fixed_now):
    '''Фикстура для дела, которое будет обновляться.'''
    return Case(
        id=None,  # Позволяем БД генерировать ID
        name='Дело о мошенничестве',
        client_id='client-2',
        attorney_id='attorney-2',
        status='Закрыто',
        description='Описание обновленного дела о мошенничестве',
    )


# Фикстура для списка дел
@pytest.fixture
def cases_list(fixed_now):
    '''Фикстура: список дел для тестирования.'''
    return [
        Case(
            id=None,
            name='Дело о краже',
            client_id='client-1',
            attorney_id='attorney-1',
            status='В процессе',
            description='Описание дела о краже',
        ),
        Case(
            id=None,
            name='Дело о мошенничестве',
            client_id='client-2',
            attorney_id='attorney-2',
            status='Закрыто',
            description='Описание дела о мошенничестве',
        ),
        Case(
            id=None,
            name='Дело о нападении',
            client_id='client-3',
            attorney_id='attorney-3',
            status='В процессе',
            description='Описание дела о нападении',
        ),
        Case(
            id=None,
            name='Дело о разбирательстве',
            client_id='client-4',
            attorney_id='attorney-4',
            status='Ожидает решения',
            description='Описание дела о разбирательстве',
        ),
        Case(
            id=None,
            name='Дело о ДТП',
            client_id='client-5',
            attorney_id='attorney-5',
            status='Закрыто',
            description='Описание дела о ДТП',
        ),
    ]
