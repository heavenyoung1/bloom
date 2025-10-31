import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

@pytest.fixture(scope='session')
def test_db_url():
    '''URL тестовой БД'''
    return 'postgresql+asyncpg://postgres:1234@192.168.175.129:5436/test_db'

@pytest.fixture(scope='session')
def event_loop():
    '''Создаёт единый event loop для всей сессии тестов.'''
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
async def engine(test_db_url, event_loop):
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
        await conn.run_sync(SQLModel.metadata.create_all)

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
        yield sess

        # Откатываем изменения после теста
        await sess.rollback()
