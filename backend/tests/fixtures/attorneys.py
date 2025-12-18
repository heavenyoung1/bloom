from backend.domain.entities.attorney import Attorney

import pytest


@pytest.fixture
async def persisted_attorney_id(attorney_repo, sample_attorney):
    '''Сохраняет юриста и возвращает ID юриста.'''
    result = await attorney_repo.save(sample_attorney)
    return result.id


@pytest.fixture
async def verifiied_persisted_attorney_id(attorney_repo, verified_attorney):
    '''Сохраняет юриста и возвращает ID ВЕРИФИЦИРОВАННОГО юриста.'''
    result = await attorney_repo.save(verified_attorney)
    return result.id


@pytest.fixture
def sample_attorney():
    return Attorney(
        id=None,  # Позволяем БД генерировать ID
        license_id='322/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan@example.com',
        telegram_username='advokat1234',
        phone='+79991234567',
        hashed_password='some_hash',
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )


@pytest.fixture
def sample_update_attorney():
    return Attorney(
        id=None,  # Позволяем БД генерировать ID
        license_id='322/4767',
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivanov3232@example.com',
        telegram_username='neadvokat4321',
        phone='+79914873567',
        hashed_password='some_hash',
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )


@pytest.fixture
def verified_attorney():
    return Attorney(
        id=None,  # Позволяем БД генерировать ID
        license_id='777/4767',
        first_name='Сергей',
        last_name='Петров',
        patronymic='Сергеевич',
        email='sergey@example.com',
        telegram_username='advokat1111',
        phone='+72991234567',
        hashed_password='some_hash',
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )


@pytest.fixture
def attorneys_list():
    '''Фикстура: список юристов для тестирования'''
    return [
        Attorney(
            id=None,  # Позволяем БД генерировать ID
            license_id='322/4767',
            first_name='Иван',
            last_name='Петров',
            patronymic='Сергеевич',
            email='ivan@example.com',
            telegram_username='advokat2222',
            phone='+79991234567',
            hashed_password='hash123',
            is_active=True,
            is_superuser=False,
            is_verified=True,
        ),
        Attorney(
            id=None,
            license_id='111/2222',
            first_name='Александр',
            last_name='Иванов',
            patronymic='Дмитриевич',
            email='alexander@example.com',
            telegram_username='advokat3333',
            phone='+79998887766',
            hashed_password='hash234',
            is_active=True,
            is_superuser=False,
            is_verified=True,
        ),
        Attorney(
            id=None,
            license_id='333/7777',
            first_name='Мария',
            last_name='Смирнова',
            patronymic='Петровна',
            email='maria@example.com',
            telegram_username='advokat4444',
            phone='+79993332211',
            hashed_password='hash345',
            is_active=True,
            is_superuser=False,
            is_verified=True,
        ),
        Attorney(
            id=None,
            license_id='444/8888',
            first_name='Екатерина',
            last_name='Васильева',
            patronymic='Сергеевна',
            email='ekaterina@example.com',
            telegram_username='advokat5555',
            phone='+79992223344',
            hashed_password='hash456',
            is_active=True,
            is_superuser=False,
            is_verified=True,
        ),
        Attorney(
            id=None,
            license_id='555/9999',
            first_name='Дмитрий',
            last_name='Александров',
            patronymic='Вячеславович',
            email='dmitry@example.com',
            telegram_username='advokat6666',
            phone='+79995556677',
            hashed_password='hash567',
            is_active=True,
            is_superuser=False,
            is_verified=True,
        ),
    ]


@pytest.fixture
async def attorney_id(test_uow_factory):
    '''Создание тестового юриста и возврат его ID'''
    async with test_uow_factory.create() as uow:
        from backend.core.security import SecurityService

        hashed_password = SecurityService.hash_password('password123')

        attorney = Attorney.create(
            license_id='LIC123456',
            first_name='John',
            last_name='Doe',
            patronymic='Test',
            email='john.doe@example.com',
            telegram_username='advokat1234',
            phone='+1234567890',
            hashed_password=hashed_password,
        )

        # Делаем юриста верифицированным
        attorney.is_verified = True
        attorney.is_active = True

        saved_attorney = await uow.attorney_repo.save(attorney)
        return saved_attorney.id
