import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def attorney_factory_mock():
    '''Мок фабрики для создания юриста'''
    return AsyncMock()
