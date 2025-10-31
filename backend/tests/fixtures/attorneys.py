from backend.domain.entities.attorney import Attorney

import pytest
# from .fixed_data import fixed_now


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
        # created_at=fixed_now,
        # updated_at=fixed_now,
    )
