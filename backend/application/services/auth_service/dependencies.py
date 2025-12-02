from fastapi import Depends

# Depends - это система внедрения зависимостей FastAPI
# Она автоматически вызывает функции и передаёт результат в параметры

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from backend.core.db.database import DataBaseConnection
from backend.infrastructure.models.attorney import AttorneyORM
from backend.core.settings import settings

# Один экземпляр подключения к БД (один engine + один sessionmaker)
db = DataBaseConnection()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.get_session() as session:
        yield session
