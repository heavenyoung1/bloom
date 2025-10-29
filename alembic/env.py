from backend.core.db.settings import Settings
from backend.infrastructure.models import *

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool, create_engine
from alembic import context

# === Импортируем Settings и модели ===
from  sqlmodel import SQLModel
from backend.core.db.settings import Settings
from backend.infrastructure.models import (
    Attorney,
    Case,
    Client,
    Contact,
    Document,
    Payment, 
    Subscription,
)

# === Настройка ===
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def get_url():
    """Получить URL из Settings (читает .env)"""
    settings = Settings()  # pydantic сам загрузит .env
    return settings.url()


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
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # Автообнаружение изменений типов колонок
    )

    with context.begin_transaction():
        context.run_migrations()


# === Онлайн миграции (синхронные!) ===
def run_migrations_online():
    # Создаём СИНХРОННЫЙ движок — Alembic не поддерживает async
    # Но URL — тот же, что и в create_async_engine!
    connectable = create_engine(
        get_url(),  # ← ТОТ ЖЕ URL!
        poolclass=pool.NullPool,
        # Можно добавить echo, если нужно:
        # echo=settings.echo,
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
