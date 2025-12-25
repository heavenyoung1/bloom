# ПОДКЛЮЧЕНИЕ ФИКСТУР, НЕ ИСПОЛЬЗУЕМ pytest_plugins!
from backend.tests.fixtures.database import *
from backend.tests.fixtures.fixed_data import *
from backend.tests.fixtures.repositories import *
from backend.tests.fixtures.attorneys import *
from backend.tests.fixtures.cases import *
from backend.tests.fixtures.events import *
from backend.tests.fixtures.contacts import *
from backend.tests.fixtures.clients import *
from backend.tests.fixtures.documents import *
from backend.tests.fixtures.policy import *
from backend.tests.fixtures.dto import *
from backend.tests.fixtures.factories import *
from backend.tests.fixtures.uow import *
from backend.tests.fixtures.settings import *
from backend.tests.fixtures.commands import *
from backend.tests.fixtures.http_client import *
from backend.tests.fixtures.redis import *
from backend.tests.fixtures.outbox import *
from backend.tests.fixtures.email_service import *


def pytest_configure(config):
    config.addinivalue_line('markers', 'integration: интеграционные тесты')
    config.addinivalue_line('markers', 'unit: unit-тесты')


# ==================== ИМПОРТ ФИКСТУР ====================
# Все фикстуры из подпапок автоматически подгружаются pytest
# ПОЗЖЕ ПОПРОБОВАТЬ ИСПОЛЬЗОВАТЬ ЭТО ДЕРЬМО!
# pytest_plugins = [
#     'backend.tests.fixtures.database',  # session, async_session
#     'backend.tests.fixtures.uow',       # test_uow, test_uow_factory
#     'backend.tests.fixtures.outbox',    # auto_process_outbox
#     'backend.tests.fixtures.redis',     # clear_redis
#     'backend.tests.fixtures.mocks',     # mock_email_service, mock_telegram_service
# ]
