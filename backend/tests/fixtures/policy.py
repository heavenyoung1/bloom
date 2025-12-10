import pytest

from unittest.mock import AsyncMock
from backend.application.policy.attorney_policy import AttorneyPolicy


@pytest.fixture
def attorney_validator(attorney_repo_mock):
    '''Фикстура для создания экземпляра валидатора'''
    return AttorneyPolicy(repo=attorney_repo_mock)


@pytest.fixture
def attorney_validator_mock():
    '''Мок валидатора для юристов'''
    return AsyncMock()
