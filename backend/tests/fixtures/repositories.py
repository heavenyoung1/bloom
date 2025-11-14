import pytest
from unittest.mock import AsyncMock

from backend.infrastructure.repositories.interfaces import (
    IAttorneyRepository,
    ICaseRepository,
    IClientRepository,
    IContactRepository,
    IDocumentMetadataRepository,
    IEventRepository,
    IFileStorage,
)

from backend.infrastructure.repositories import (
    AttorneyRepository,
    CaseRepository,
    ClientRepository,
    ContactRepository,
    DocumentMetadataRepository,
    EventRepository,
)

# =============== ДЛЯ ИНТЕГРАЦИОННЫХ ТЕСТОВ РЕПОЗИТОРИИ С СЕССИЕЙ РЕАЛЬНОЙ БД =============== 

@pytest.fixture
def attorney_repo(session):
    '''Репозиторий с тестовой сессией'''
    return AttorneyRepository(session)


@pytest.fixture
def case_repo(session):
    '''Репозиторий с тестовой сессией'''
    return CaseRepository(session)


@pytest.fixture
def client_repo(session):
    '''Репозиторий с тестовой сессией'''
    return ClientRepository(session)


@pytest.fixture
def contact_repo(session):
    '''Репозиторий с тестовой сессией'''
    return ContactRepository(session)


@pytest.fixture
def document_repo(session):
    '''Репозиторий с тестовой сессией'''
    return DocumentMetadataRepository(session)


@pytest.fixture
def event_repo(session):
    '''Репозиторий с тестовой сессией'''
    return EventRepository(session)

# =========================================================================================
# =============== ЗАМОКАННЫЕ РЕПОЗИТОРИИ ДЛЯ ЮНИТ - ТЕСТИРОВАНИЯ ==========================
# AsyncMock, чтобы можно было await'ить методы

@pytest.fixture
def attorney_repo_mock():
    mock = AsyncMock()
    mock.get_by_email = AsyncMock(return_value=None)
    mock.get_by_license_id = AsyncMock(return_value=None)
    mock.get_by_phone = AsyncMock(return_value=None)
    return mock

@pytest.fixture
def case_repo_mock():
    return AsyncMock(spec=ICaseRepository)

@pytest.fixture
def client_repo_mock():
    return AsyncMock(spec=IClientRepository)

@pytest.fixture
def contact_repo_mock():
    return AsyncMock(spec=IContactRepository)

@pytest.fixture
def document_repo_mock():
    return AsyncMock(spec=IDocumentMetadataRepository)

@pytest.fixture
def event_repo_mock():
    return AsyncMock(spec=IEventRepository)

# =========================================================================================
