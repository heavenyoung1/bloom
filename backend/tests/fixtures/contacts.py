from datetime import datetime, timezone
import pytest
from backend.domain.entities.contact import (
    Contact,
)  # Предполагается, что у вас есть такой класс Contact


# Фикстура для дефолтного контакта
@pytest.fixture
def sample_contact(persisted_case):
    '''Фикстура для дефолтного контакта.'''
    return Contact(
        id=None,  # Позволяем БД генерировать ID
        name='Иван Иванович Петров',
        personal_info='1234567890',  # Номер паспорта или другие данные
        phone='+79991234567',
        email='ivan@example.com',
        case_id=persisted_case,
    )


# Фикстура для контакта, который будет обновляться
@pytest.fixture
def sample_update_contact(persisted_case):
    '''Фикстура для обновленного контакта.'''
    return Contact(
        id=None,  # Позволяем БД генерировать ID
        name='Иван Иванович Смирнов',
        personal_info='0987654321',  # Новый номер паспорта или другие данные
        phone='+79998887766',
        email='ivanov3232@example.com',
        case_id=persisted_case,
    )


# Фикстура для списка контактов
@pytest.fixture
def contacts_list(persisted_case):
    '''Фикстура: список контактов для тестирования.'''
    return [
        Contact(
            id=None,
            name='Иван Иванович Петров',
            personal_info='1234567890',
            phone='+79991234567',
            email='ivan@example.com',
            case_id=persisted_case,
        ),
        Contact(
            id=None,
            name='Александр Дмитриевич Иванов',
            personal_info='2345678901',
            phone='+79998887766',
            email='alexander@example.com',
            case_id=persisted_case,
        ),
        Contact(
            id=None,
            name='Мария Петровна Смирнова',
            personal_info='3456789012',
            phone='+79993332211',
            email='maria@example.com',
            case_id=persisted_case,
        ),
        Contact(
            id=None,
            name='Екатерина Сергеевна Васильева',
            personal_info='4567890123',
            phone='+79992223344',
            email='ekaterina@example.com',
            case_id=persisted_case,
        ),
        Contact(
            id=None,
            name='Дмитрий Вячеславович Александров',
            personal_info='5678901234',
            phone='+79995556677',
            email='dmitry@example.com',
            case_id=persisted_case,
        ),
    ]
