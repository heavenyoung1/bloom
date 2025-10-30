from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from backend.core.logger import logger


class Settings(BaseSettings):
    '''Конфигурация приложения (читается из .env файла).'''

    # Параметры БД
    host: str = 'localhost'
    port: int = 5432
    user: str
    password: str
    db_name: str

    # SQLAlchemy параметры
    driver: str = 'postgresql+asyncpg'
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_pre_ping: bool = True

    # === Нужен для синхронного движка Alembic миграций. Не использовать! ===
    _sync_driver: str = 'postgresql'
    # === === === === === === === === === === === === === ====== === === ====

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='pg_',
        extra='ignore',
        case_sensitive=True,
    )

    def url(self) -> str:
        '''Собрать URL подключения безопасно (защита от SQL injection).'''
        return str(
            URL.create(
                drivername=self.driver,
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db_name,
            )
        )

    def alembic_url(self) -> str:
        '''Строка для подключения к БД ТОЛЬКО для выполнения Alembic миграций.'''
        url = f'{self._sync_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        return url
