from backend.infrastructure.repositories import (
    AttorneyRepository,
    CaseRepository,
    ClientRepository,
    ContactRepository,
    DocumentRepository,
    EventRepository,
)

import pytest


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
    return DocumentRepository(session)


@pytest.fixture
def event_repo(session):
    '''Репозиторий с тестовой сессией'''
    return EventRepository(session)
