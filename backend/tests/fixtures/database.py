import pytest
import asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.models._base import Base
from backend.core.logger import logger


@pytest.fixture(scope='session')
async def engine(test_settings):
    '''
    Создание engine для тестовой БД.

    scope='session' - engine существует на протяжении ВСЕХ тестов
    Это экономит время на создание/удаление таблиц
    '''
    logger.info(f'БД ПОДКЛЮЧЕНИЕ {test_settings.url()}')
    engine = create_async_engine(
        test_settings.url(),
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

    # Создаём таблицы один раз для всей сессии
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Очищаем БД после всех тестов
    # ❌ больше не удаляем таблицы (это создаёт гонки)
    # async with engine.begin() as conn:
    #     await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope='session')
def SessionLocal(engine):
    '''Фабрика для создания async сессий'''
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest.fixture(scope='function')
async def session(SessionLocal):
    '''Сессия для отдельного теста.

    scope='function' (по умолчанию) - НОВАЯ сессия для каждого теста
    Это гарантирует чистоту данных между тестами.
    Все изменения будут откатываться после выполнения теста.
    '''
    async with SessionLocal() as sess:
        logger.debug(f'SessionLocal() BEGIN')
        await sess.begin()  # начинаем транзакцию
        try:
            logger.debug(f'YIELD SESSION')
            yield sess
        finally:
            logger.debug(f'Выполнение Rollback')
            await sess.rollback()  # ← откатываем
            # ← НИКАКОГО close()!
