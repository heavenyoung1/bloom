from backend.domain.entities.attorney import Attorney

import pytest

# from .fixed_data import fixed_now

@pytest.fixture
async def persisted_attorney_id(attorney_repo, sample_attorney):
    '''Сохраняет юриста и возвращает ID юриста.'''
    result = await attorney_repo.save(sample_attorney)
    assert result['success'] is True
    return result['id']

@pytest.fixture
def sample_attorney(fixed_now):
    return Attorney(
        id=None,  # Позволяем БД генерировать ID
        attorney_id='322/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan@example.com',
        phone='+79991234567',
        password_hash='hash123',
        is_active=True,
    )


@pytest.fixture
def sample_update_attorney(fixed_now):
    return Attorney(
        id=None,  # Позволяем БД генерировать ID
        attorney_id='322/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivanov3232@example.com',
        phone='+79914873567',
        password_hash='hash123567853',
        is_active=True,
    )


@pytest.fixture
def attorneys_list(fixed_now):
    '''Фикстура: список юристов для тестирования'''
    return [
        Attorney(
            id=None,  # Позволяем БД генерировать ID
            attorney_id='322/4767',
            first_name='Иван',
            last_name='Петров',
            patronymic='Сергеевич',
            email='ivan@example.com',
            phone='+79991234567',
            password_hash='hash123',
            is_active=True,
        ),
        Attorney(
            id=None,
            attorney_id='111/2222',
            first_name='Александр',
            last_name='Иванов',
            patronymic='Дмитриевич',
            email='alexander@example.com',
            phone='+79998887766',
            password_hash='hash234',
            is_active=True,
        ),
        Attorney(
            id=None,
            attorney_id='333/7777',
            first_name='Мария',
            last_name='Смирнова',
            patronymic='Петровна',
            email='maria@example.com',
            phone='+79993332211',
            password_hash='hash345',
            is_active=True,
        ),
        Attorney(
            id=None,
            attorney_id='444/8888',
            first_name='Екатерина',
            last_name='Васильева',
            patronymic='Сергеевна',
            email='ekaterina@example.com',
            phone='+79992223344',
            password_hash='hash456',
            is_active=True,
        ),
        Attorney(
            id=None,
            attorney_id='555/9999',
            first_name='Дмитрий',
            last_name='Александров',
            patronymic='Вячеславович',
            email='dmitry@example.com',
            phone='+79995556677',
            password_hash='hash567',
            is_active=True,
        ),
    ]
