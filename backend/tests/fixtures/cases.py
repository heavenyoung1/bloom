from datetime import datetime
import pytest
from backend.domain.entities.case import Case
from backend.domain.entities.auxiliary import CaseStatus


@pytest.fixture
async def persisted_case(case_repo, sample_case):
    '''Сохраняет дело и возвращает ID дела.'''
    result = await case_repo.save(sample_case)
    return result.id


@pytest.fixture
async def sample_case(persisted_attorney_id, persisted_client_id):
    '''Фикстура для дефолтного дела с реальными attorney_id и client_id.'''
    return Case(
        id=None,
        name='Дело о краже',
        client_id=persisted_client_id,  # Реальный ID из БД
        attorney_id=persisted_attorney_id,  # Реальный ID из БД
        status=CaseStatus.IN_PROGRESS,
        description='Описание дела о краже',
    )


@pytest.fixture
async def sample_case_for_verified_attorney(
    verifiied_persisted_attorney_id, verified_persisted_client_id
):
    '''Фикстура для дефолтного дела с реальными attorney_id и client_id.'''
    return Case(
        id=None,
        name='Дело о краже',
        client_id=verified_persisted_client_id,  # Реальный ID из БД
        attorney_id=verifiied_persisted_attorney_id,  # Реальный ID из БД
        status=CaseStatus.IN_PROGRESS,
        description='Описание дела о краже',
    )


@pytest.fixture
async def sample_update_case(persisted_attorney_id, persisted_client_id):
    '''Фикстура для дела, которое будет обновляться.'''
    return Case(
        id=None,
        name='Дело о мошенничестве',
        client_id=persisted_client_id,  # Реальный ID из БД
        attorney_id=persisted_attorney_id,  # Реальный ID из БД
        status=CaseStatus.ON_HOLD,
        description='Описание обновленного дела о мошенничестве',
    )


@pytest.fixture
async def cases_list(persisted_attorney_id, persisted_client_id):
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
        ),
        Case(
            id=None,
            name='Дело о разбирательстве',
            client_id=persisted_client_id,  # Реальный ID из БД
            attorney_id=persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.CANCELLED,
            description='Описание дела о разбирательстве',
        ),
        Case(
            id=None,
            name='Дело о ДТП',
            client_id=persisted_client_id,  # Реальный ID из БД
            attorney_id=persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.ARCHIVED,
            description='Описание дела о ДТП',
        ),
    ]


@pytest.fixture
async def verified_cases_list(
    verifiied_persisted_attorney_id, verified_persisted_client_id
):
    '''
    Фикстура: список дел для тестирования.
    Использует одних и тех же attorney и client для всех дел.
    '''
    return [
        Case(
            id=None,
            name='Дело о краже 1',
            client_id=verified_persisted_client_id,  # Реальный ID из БД
            attorney_id=verifiied_persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.IN_PROGRESS,
            description='Описание дела о краже 1',
        ),
        Case(
            id=None,
            name='Дело о краже 2',
            client_id=verified_persisted_client_id,  # Реальный ID из БД
            attorney_id=verifiied_persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.IN_PROGRESS,
            description='Описание дела о краже 2',
        ),
        Case(
            id=None,
            name='Дело о краже 3',
            client_id=verified_persisted_client_id,  # Реальный ID из БД
            attorney_id=verifiied_persisted_attorney_id,  # Реальный ID из БД
            status=CaseStatus.IN_PROGRESS,
            description='Описание дела о краже 3',
        ),
    ]
