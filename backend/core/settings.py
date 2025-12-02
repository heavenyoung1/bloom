from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from backend.core.logger import logger
from pydantic import Field


class Settings(BaseSettings):
    '''Конфигурация приложения (читается из .env файла).'''

    project_name: str = 'CRM'
    debug: bool = True

    # === PostgreSQL параметры ===
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

    # === Драйвер для синхронного движка Alembic миграций. ===
    _sync_driver: str = 'postgresql'
    # === === === === === === === === === === === === === ====== === === ====

    # Redis
    redis_url: str = Field(default='redis://localhost:6379')
    redis_default_ttl: int = 3600  # 1 час

    # === JWT ===
    algorithm: str = 'HS256'
    secret_key: str = Field(default='your-secret-key-change-in-production')
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Security
    password_min_length: int = 8
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 15

    # === Email (для сброса пароля) ===
    smtp_host: str = 'smtp.gmail.com'
    smtp_port: int = 587
    smtp_user: str = ''
    smtp_password: str = ''
    smtp_from: str = 'noreply@attorney-crm.com'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='',  # <- Без префикса
        extra='ignore',
        case_sensitive=True,
    )

    # ============= 🧪 ВОТ ТУТ ПАРОЛЬ ПЕРЕДАЕТСЯ КАК *** 🧪 ================
    # def url(self) -> str:
    #     '''Собрать URL подключения безопасно (защита от SQL injection).'''
    #     return str(
    #         URL.create(
    #             drivername=self.driver,
    #             username=self.user,
    #             password=self.password,
    #             host=self.host,
    #             port=self.port,
    #             database=self.db_name,
    #         )
    #     )
    # ============= 🧪 ================================= 🧪 ================

    def url(self) -> str:
        return f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'

    def alembic_url(self) -> str:
        '''Строка для подключения к БД ТОЛЬКО для выполнения Alembic миграций.'''
        url = f'{self._sync_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        return url


# Singleton - Единственный экземпляр настроек на всё приложение
settings = Settings()
