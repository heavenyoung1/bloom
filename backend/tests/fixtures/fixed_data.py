import pytest
from datetime import datetime, timedelta, timezone

MOSCOW = timezone(timedelta(hours=3))


# В фикстуре
@pytest.fixture
def fixed_now():
    return datetime(2025, 4, 1, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def sample_date():
    return datetime(2026, 11, 11, 11, 00, tzinfo=MOSCOW)
