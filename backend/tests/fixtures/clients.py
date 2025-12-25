from datetime import datetime, timezone
import pytest
from backend.domain.entities.client import Client
from backend.infrastructure.models.client import Messenger


@pytest.fixture
async def persisted_client_id(client_repo, sample_client, persisted_attorney_id):
    '''Сохраняет клиента и возвращает его ID. Требует существующего адвоката-владельца.'''
    sample_client.owner_attorney_id = persisted_attorney_id
    result = await client_repo.save(sample_client)
    return result.id


@pytest.fixture
async def verified_persisted_client_id(
    client_repo, sample_client_for_verify, verifiied_persisted_attorney_id
):
    '''Сохраняет клиента и возвращает его ID. Требует существующего адвоката-владельца.'''
    sample_client.owner_attorney_id = verifiied_persisted_attorney_id
    result = await client_repo.save(sample_client_for_verify)
    return result.id


# Фикстура для дефолтного клиента
@pytest.fixture
def sample_client(persisted_attorney_id):
    '''Фикстура для дефолтного клиента.'''
    return Client(
        id=None,  # Позволяем БД генерировать ID
        name='Иван Иванович Петров',
        type=True,  # Физическое лицо
        email='ivan@example.com',
        phone='+79991234567',
        personal_info='1234567890',  # ИНН или номер паспорта
        address='Москва, ул. Тверская, 1',
        messenger=Messenger.TG,  # Мессенджер Telegram
        messenger_handle='ivan123',
        owner_attorney_id=persisted_attorney_id,  # Пример ссылки на адвоката
    )


# Фикстура для дефолтного клиента
@pytest.fixture
def sample_client_for_verify(verifiied_persisted_attorney_id):
    '''Фикстура для дефолтного клиента.'''
    return Client(
        id=None,  # Позволяем БД генерировать ID
        name='Иван Иванович Петров',
        type=True,  # Физическое лицо
        email='ivan@example.com',
        phone='+79991234567',
        personal_info='1234567890',  # ИНН или номер паспорта
        address='Москва, ул. Тверская, 1',
        messenger=Messenger.TG,  # Мессенджер Telegram
        messenger_handle='ivan123',
        owner_attorney_id=verifiied_persisted_attorney_id,  # Пример ссылки на адвоката
    )


# Фикстура для клиента, который будет обновляться
@pytest.fixture
def sample_update_client(persisted_attorney_id):
    '''Фикстура для обновленного клиента.'''
    return Client(
        id=None,  # Позволяем БД генерировать ID
        name='Иван Иванович Смирнов',
        type=False,  # Юридическое лицо
        email='ivanov3232@example.com',
        phone='+79998887766',
        personal_info='0987654321',  # Новый номер паспорта или ИНН
        address='Москва, ул. Арбат, 5',
        messenger=Messenger.WA,  # Мессенджер WhatsApp
        messenger_handle='ivanov3232',
        owner_attorney_id=persisted_attorney_id,  # Пример ссылки на адвоката
    )


# Фикстура для списка клиентов
@pytest.fixture
def clients_list(persisted_attorney_id):
    '''Фикстура: список клиентов для тестирования.'''
    return [
        Client(
            id=None,
            name='Иван Иванович Петров',
            type=True,
            email='ivan@example.com',
            phone='+79991234567',
            personal_info='1234567890',
            address='Москва, ул. Тверская, 1',
            messenger=Messenger.TG,
            messenger_handle='ivan123',
            owner_attorney_id=persisted_attorney_id,
        ),
        Client(
            id=None,
            name='Александр Дмитриевич Иванов',
            type=False,
            email='alexander@example.com',
            phone='+79998887766',
            personal_info='2345678901',
            address='Москва, ул. Ленина, 10',
            messenger=Messenger.WA,
            messenger_handle='alexander_ivanov',
            owner_attorney_id=persisted_attorney_id,
        ),
        Client(
            id=None,
            name='Мария Петровна Смирнова',
            type=True,
            email='maria@example.com',
            phone='+79993332211',
            personal_info='3456789012',
            address='Москва, ул. Пушкина, 15',
            messenger=Messenger.MA,
            messenger_handle='maria_smirnova',
            owner_attorney_id=persisted_attorney_id,
        ),
        Client(
            id=None,
            name='Екатерина Сергеевна Васильева',
            type=False,
            email='ekaterina@example.com',
            phone='+79992223344',
            personal_info='4567890123',
            address='Москва, ул. Красная, 20',
            messenger=Messenger.MA,
            messenger_handle='ekaterina_vasileva',
            owner_attorney_id=persisted_attorney_id,
        ),
        Client(
            id=None,
            name='Дмитрий Вячеславович Александров',
            type=True,
            email='dmitry@example.com',
            phone='+79995556677',
            personal_info='5678901234',
            address='Москва, ул. Маяковская, 30',
            messenger=Messenger.MA,
            messenger_handle='dmitry_alexandrov',
            owner_attorney_id=persisted_attorney_id,
        ),
    ]
