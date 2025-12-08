# ПОДКЛЮЧЕНИЕ ФИКСТУР, НЕ ИСПОЛЬЗУЕМ pytest_plugins!
from backend.tests.fixtures.database import *
from backend.tests.fixtures.fixed_data import *
from backend.tests.fixtures.repositories import *
from backend.tests.fixtures.attorneys import *
from backend.tests.fixtures.cases import *
from backend.tests.fixtures.contacts import *
from backend.tests.fixtures.clients import *
from backend.tests.fixtures.documents import *
from backend.tests.fixtures.policy import *
from backend.tests.fixtures.dto import *
from backend.tests.fixtures.factories import *
from backend.tests.fixtures.services import *
from backend.tests.fixtures.uow import *
from backend.tests.fixtures.settings import *


def pytest_configure(config):
    config.addinivalue_line('markers', 'integration: интеграционные тесты')
    config.addinivalue_line('markers', 'unit: unit-тесты')
