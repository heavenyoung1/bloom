pytest_plugins = [
    'backend.tests.fixtures.attorneys',
    'backend.tests.fixtures.database',
    'backend.tests.fixtures.fixed_data',
    'backend.tests.fixtures.repositories',
]


def pytest_configure(config):
    config.addinivalue_line('markers', 'integration: интеграционные тесты')
    config.addinivalue_line('markers', 'unit: unit-тесты')
