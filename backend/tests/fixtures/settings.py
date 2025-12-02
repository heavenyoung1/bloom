from pydantic_settings import BaseSettings, SettingsConfigDict
import pytest


class TestSettings(BaseSettings):
    '''Конфигурация для тестовой среды.'''

    # Параметры БД
    host: str
    port: int
    user: str
    password: str
    db_name: str

    # SQLAlchemy параметры
    driver: str = 'postgresql+asyncpg'
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_pre_ping: bool = True

    model_config = SettingsConfigDict(
        env_file='.env.test',  # указываем отдельный файл конфигурации для тестов
        env_file_encoding='utf-8',
        env_prefix='',
        extra='ignore',
        case_sensitive=True,
    )

    def url(self) -> str:
        '''Строка для подключения к БД для тестов'''
        url = f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        return url


@pytest.fixture(scope='session')
def test_settings() -> TestSettings:
    '''Фикстура настроек для тестовой среды.'''
    return TestSettings()  #  загружается .env.test
