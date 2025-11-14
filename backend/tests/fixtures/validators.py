import pytest

from unittest.mock import AsyncMock
from backend.application.validators.attorney_validator import AttorneyValidator


@pytest.fixture
def attorney_validator(attorney_repo_mock):
    '''Фикстура для создания экземпляра валидатора'''
    return AttorneyValidator(repo=attorney_repo_mock)


@pytest.fixture
def attorney_validator_mock():
    '''Мок валидатора для юристов'''
    return AsyncMock()
