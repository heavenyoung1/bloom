import pytest
from datetime import datetime, timezone


# В фикстуре
@pytest.fixture
def fixed_now():
    return datetime(2025, 4, 1, 12, 0, 0, tzinfo=timezone.utc)
