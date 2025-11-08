from datetime import datetime
import pytest
from backend.domain.entities.case import Case
from backend.infrastructure.models import CaseStatus


@pytest.fixture
async def persisted_case(case_repo, sample_case):
    '''Сохраняет дело и возвращает ID дела.'''
    result = await case_repo.save(sample_case)
    return result.id


@pytest.fixture
async def sample_case(persisted_attorney_id, persisted_client_id, fixed_now):
    '''Фикстура для дефолтного дела с реальными attorney_id и client_id.'''
    return Case(
        id=None,
        name='Дело о краже',
        client_id=persisted_client_id,  # Реальный ID из БД
        attorney_id=persisted_attorney_id,  # Реальный ID из БД
        status=CaseStatus.IN_PROGRESS,
        description='Описание дела о краже',
        created_at=fixed_now,
    )


@pytest.fixture
async def sample_update_case(persisted_attorney_id, persisted_client_id, fixed_now):
    '''Фикстура для дела, которое будет обновляться.'''
    return Case(
        id=None,
        name='Дело о мошенничестве',
        client_id=persisted_client_id,  # Реальный ID из БД
        attorney_id=persisted_attorney_id,  # Реальный ID из БД
        status=CaseStatus.ON_HOLD,
        description='Описание обновленного дела о мошенничестве',
        created_at=fixed_now,
    )


@pytest.fixture
async def cases_list(persisted_attorney_id, persisted_client_id, fixed_now):
    '''
    Фикстура: список дел для тестирования.
    Использует одних и тех же attorney и client для всех дел.
    '''
    return [
        Case(
            id=None,
            name='Дело о краже',
            client_id=persisted_client_id,  # Реальный ID из БД
            attorney_id=persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.NEW,
            description='Описание дела о краже',
            created_at=fixed_now,
        ),
        Case(
            id=None,
            name='Дело о мошенничестве',
            client_id=persisted_client_id,  # Реальный ID из БД
            attorney_id=persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.NEW,
            description='Описание дела о мошенничестве',
        ),
        Case(
            id=None,
            name='Дело о нападении',
            client_id=persisted_client_id,  # Реальный ID из БД
            attorney_id=persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.NEW,
            description='Описание дела о нападении',
            created_at=fixed_now,
        ),
        Case(
            id=None,
            name='Дело о разбирательстве',
            client_id=persisted_client_id,  # Реальный ID из БД
            attorney_id=persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.CANCELLED,
            description='Описание дела о разбирательстве',
            created_at=fixed_now,
        ),
        Case(
            id=None,
            name='Дело о ДТП',
            client_id=persisted_client_id,  # Реальный ID из БД
            attorney_id=persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.ARCHIVED,
            description='Описание дела о ДТП',
            created_at=fixed_now,
        ),
    ]
