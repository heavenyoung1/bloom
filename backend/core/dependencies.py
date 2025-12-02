from fastapi import Depends

# Depends - это система внедрения зависимостей FastAPI
# Она автоматически вызывает функции и передаёт результат в параметры

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.db.database import DataBaseConnection
from backend.infrastructure.models.attorney import AttorneyORM
from backend.core.settings import settings
from backend.core.db.database import database  # Импортируем глобальный экземпляр


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.get_session() as session:
        yield session


async def get_uow_factory() -> UnitOfWorkFactory:
    '''Получить фабрику UoW'''
    return UnitOfWorkFactory(database)
