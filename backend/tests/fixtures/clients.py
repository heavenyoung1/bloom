from datetime import datetime, timezone
import pytest
from backend.domain.entities.client import (
    Client,
)  # Предполагается, что у вас есть такой класс Client


# Фикстура для дефолтного клиента
@pytest.fixture
def sample_client(sample_attorney):
    '''Фикстура для дефолтного клиента.'''
    return Client(
        id=None,  # Позволяем БД генерировать ID
        name='Иван Иванович Петров',
        type=True,  # Физическое лицо
        email='ivan@example.com',
        phone='+79991234567',
        personal_info='1234567890',  # ИНН или номер паспорта
        address='Москва, ул. Тверская, 1',
        messenger='tg',  # Мессенджер Telegram
        messenger_handle='ivan123',
        owner_attorney_id=sample_attorney.id,  # Пример ссылки на адвоката
    )


# Фикстура для клиента, который будет обновляться
@pytest.fixture
def sample_update_client(sample_attorney):
    '''Фикстура для обновленного клиента.'''
    return Client(
        id=None,  # Позволяем БД генерировать ID
        name='Иван Иванович Смирнов',
        type=False,  # Юридическое лицо
        email='ivanov3232@example.com',
        phone='+79998887766',
        personal_info='0987654321',  # Новый номер паспорта или ИНН
        address='Москва, ул. Арбат, 5',
        messenger='wa',  # Мессенджер WhatsApp
        messenger_handle='ivanov3232',
        owner_attorney_id=sample_attorney.id,  # Пример ссылки на адвоката
    )


# Фикстура для списка клиентов
@pytest.fixture
def clients_list(fixed_now):
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
            messenger='tg',
            messenger_handle='ivan123',
            created_at=fixed_now,
            owner_attorney_id=1,
        ),
        Client(
            id=None,
            name='Александр Дмитриевич Иванов',
            type=False,
            email='alexander@example.com',
            phone='+79998887766',
            personal_info='2345678901',
            address='Москва, ул. Ленина, 10',
            messenger='wa',
            messenger_handle='alexander_ivanov',
            created_at=fixed_now,
            owner_attorney_id=2,
        ),
        Client(
            id=None,
            name='Мария Петровна Смирнова',
            type=True,
            email='maria@example.com',
            phone='+79993332211',
            personal_info='3456789012',
            address='Москва, ул. Пушкина, 15',
            messenger='tg',
            messenger_handle='maria_smirnova',
            created_at=fixed_now,
            owner_attorney_id=3,
        ),
        Client(
            id=None,
            name='Екатерина Сергеевна Васильева',
            type=False,
            email='ekaterina@example.com',
            phone='+79992223344',
            personal_info='4567890123',
            address='Москва, ул. Красная, 20',
            messenger='ma',
            messenger_handle='ekaterina_vasileva',
            created_at=fixed_now,
            owner_attorney_id=4,
        ),
        Client(
            id=None,
            name='Дмитрий Вячеславович Александров',
            type=True,
            email='dmitry@example.com',
            phone='+79995556677',
            personal_info='5678901234',
            address='Москва, ул. Маяковская, 30',
            messenger='tg',
            messenger_handle='dmitry_alexandrov',
            created_at=fixed_now,
            owner_attorney_id=5,
        ),
    ]
