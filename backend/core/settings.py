from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from backend.core.logger import logger
from pydantic import Field


class Settings(BaseSettings):
    '''Конфигурация приложения (читается из .env файла).'''

    PROJECT_NAME: str = 'CRM'
    DEBUG: bool = True

    # === PostgreSQL параметры ===
    HOST: str = 'localhost'
    PORT: int = 5432
    USER: str
    PASSWORD: str
    DB_NAME: str

    # SQLAlchemy параметры
    DRIVER: str = 'postgresql+asyncpg'
    ECHO: bool = False
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_PRE_PING: bool = True

    # === Драйвер для синхронного движка Alembic миграций. ===
    SYNC_DRIVER: str = 'postgresql'
    # === === === === === === === === === === === === === ====== === === ====

    # Redis
    REDIS_URL: str = Field(default='redis://localhost:6379')
    REDIS_DEFAULT_TTL: int = 3600  # 1 час

    # === JWT ===
    JWT_ALGORITHM: str = 'HS256'
    JWT_SECRET_KEY: str = Field(default='your-secret-key-change-in-production')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Security
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15

    # === Email (для сброса пароля) ===
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str = 'noreply@attorney-crm.com'

    # === File Storage ===
    FILE_STORAGE_BASE_PATH: str = Field(
        default='storage/',  # Относительный путь - будет создан в корне проекта
        description='Базовый путь для хранения файлов (локальное хранилище). '
        'Для Windows используйте относительный путь (storage/) или абсолютный (C:\\Projects\\storage\\)',
    )
    FILE_STORAGE_TYPE: str = Field(
        default='local',
        description='Тип хранилища: local или s3',
    )
    FILE_STORAGE_TEMPLATE: str = Field(
        default='',
        description='Абсолютный путь к PDF шаблону для генерации платежных документов. '
        'Пример: C:\\Projects\\bloom\\backend\\infrastructure\\pdf\\template\\check_template.pdf',
    )

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='',  # <- Без префикса
        extra='ignore',
        case_sensitive=False,  # В .env можно использовать как верхний, так и нижний регистр
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
        return f'{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}'

    def alembic_url(self) -> str:
        '''Строка для подключения к БД ТОЛЬКО для выполнения Alembic миграций.'''
        url = f'{self.SYNC_DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}'
        return url


# Singleton - Единственный экземпляр настроек на всё приложение
settings = Settings()
