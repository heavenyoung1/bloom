from backend.domain.entities.attorney import Attorney

import pytest
from tests.fixtures.fixed_data import fixed_now


@pytest.fixture
def sample_attorney():
    return Attorney(
        id=None,  # Позволяем БД генерировать ID
        first_name='Иван',
        last_name='Петров',
        patronymic='Сергеевич',
        email='ivan@example.com',
        phone='+79991234567',
        password_hash='hash123',
        is_active=True,
        created_at=fixed_now,
        updated_at=fixed_now,
    )
