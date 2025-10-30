import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel

from backend.infrastructure.repositories import AttorneyRepository


@pytest.fixture(scope='session')
def test_db_url():
    '''URL тестовой БД'''
    return 'postgresql+asyncpg://postgres:1234@localhost:5436/test_db'


@pytest.fixture(scope='session')
async def engine(test_db_url):
    '''Создание engine для тестовой БД'''
    engine = create_async_engine(
        test_db_url,
        echo=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

    # Создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Удаляем таблицы после всех тестов
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope='session')
def SessionLocal(engine):
    '''Фабрика для создания сессий'''
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest.fixture
async def session(SessionLocal):
    '''Сессия для отдельного теста (чистая для каждого)'''
    async with SessionLocal() as sess:
        yield sess

        # Откатываем изменения после теста
        await sess.rollback()
