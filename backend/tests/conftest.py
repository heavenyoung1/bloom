pytest_plugins = [
    'fixtures.attorneys',
    'fixtures.database',
    'fixtures.fixed_data',
    'fixtures.repositories',
]


def pytest_configure(config):
    config.addinivalue_line('markers', 'integration: интеграционные тесты')
    config.addinivalue_line('markers', 'unit: unit-тесты')
