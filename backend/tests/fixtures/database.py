import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock

from backend.infrastructure.models._base import Base


@pytest.fixture(scope='session')
def test_db_url():
    '''URL тестовой БД'''
    return 'postgresql+asyncpg://postgres:1234@192.168.175.129:5436/test_db'


@pytest.fixture(scope='session')
async def engine(test_db_url):
    '''
    Создание engine для тестовой БД.

    scope='session' - engine существует на протяжении ВСЕХ тестов
    Это экономит время на создание/удаление таблиц
    '''
    engine = create_async_engine(
        test_db_url,
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


@pytest.fixture
async def session(SessionLocal):
    '''Сессия для отдельного теста.

    scope='function' (по умолчанию) - НОВАЯ сессия для каждого теста
    Это гарантирует чистоту данных между тестами
    '''
    async with SessionLocal() as sess:
        await sess.begin()  # ← начинаем транзакцию
        try:
            yield sess
        finally:
            await sess.rollback()  # ← откатываем
            # ← НИКАКОГО close()!


@pytest.fixture
def uow_mock(attorney_repo_mock):
    '''Мок Unit of Work'''
    uow = AsyncMock()
    uow.attorney_repo = attorney_repo_mock
    return uow
