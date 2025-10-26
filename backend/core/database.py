from sqlalchemy import create_async_engine
from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from settings import Settings


class DataBaseConnection:
    def __init__(self, settings: Settings):
        self.settings = settings
        url = self.settings.get_db_url()
        
        self.engine = create_async_engine(
            url,
            echo=True,                  # Логгирование SQL-запросов для отладки
            pool_pre_ping=True,         # лечит «мертвые» коннекты
            pool_size=10,               # тюнинг пула по ситуации
            max_overflow=20,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,     # не «просрочивать» объекты после commit
            autoflush=False,            # опционально, чтобы контролировать flush вручную
        )