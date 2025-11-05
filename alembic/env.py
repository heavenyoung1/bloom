from backend.core.db.settings import Settings
from backend.infrastructure.models import *
from backend.core.logger import logger

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool, create_engine
from alembic import context

# === Импортируем Settings и модели ===
from sqlmodel import SQLModel
from backend.core.db.settings import Settings
from backend.infrastructure.models import (
    AttorneyORM,
    CaseORM,
    ClientORM,
    ContactORM,
    DocumentORM,
    EventORM,
)

# === Настройка ===
config = context.config
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata


def get_alembic_url():
    """Получить URL из Settings (читает .env)"""
    settings = Settings()  # pydantic сам загрузит .env
    logger.debug(f'Получен Alembic url для миграций - {settings.alembic_url()}')
    return settings.alembic_url()


# config.set_main_option("sqlalchemy.url", get_alembic_url())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    context.configure(
        url=get_alembic_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Автообнаружение изменений типов колонок
    )
    logger.debug(f'ALEMBIC_URL = {context.configure()}')

    with context.begin_transaction():
        context.run_migrations()


# === Онлайн миграции (синхронные!) ===
def run_migrations_online():
    # Создаём СИНХРОННЫЙ движок — Alembic не поддерживает async
    # Но URL — тот же, что и в create_async_engine!
    connectable = create_engine(
        get_alembic_url(),
        poolclass=pool.NullPool,
        echo=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


# === Запуск ===
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
