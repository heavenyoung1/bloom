from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db.database import DataBaseConnection
from backend.core.settings import Settings


# Singleton
_db_connection: DataBaseConnection | None = None


def get_db_connection() -> DataBaseConnection:
    '''
    Получить singleton подключения к БД.

    Создаётся один раз при первом вызове.
    '''
    global _db_connection
    if _db_connection is None:
        settings = Settings()
        _db_connection = DataBaseConnection(settings)
    return _db_connection


async def get_async_session(
    db: DataBaseConnection = Depends(get_db_connection),
) -> AsyncGenerator[AsyncSession, None]:
    '''
    FastAPI Dependency для получения async сессии SQLAlchemy.

    ⚠️ ВАЖНО: Эта функция - мост между вашим DataBaseConnection
    и FastAPI системой зависимостей.

    Использование:
        @app.get("/attorneys/{id}")
        async def get_attorney(
            id: int,
            session: AsyncSession = Depends(get_async_session)
        ):
            result = await session.execute(select(AttorneyORM).where(...))
            return result.scalar_one()

    Почему нужна обёртка:
    - DataBaseConnection.get_session() - это async context manager
    - FastAPI Depends() требует generator function
    - Эта функция адаптирует одно к другому
    '''
    async with db.get_session() as session:
        yield session
