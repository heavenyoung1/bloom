from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from typing import Dict, Any

# Depends - это система внедрения зависимостей FastAPI
# Она автоматически вызывает функции и передаёт результат в параметры

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from backend.core.security import SecurityService
from backend.infrastructure.redis.session_storage import SessionStorage
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


security_scheme = HTTPBearer()


async def get_current_attorney(
    credentials: HTTPBasicCredentials = Depends(security_scheme),
) -> Dict[str, Any]:
    '''
    FastAPI Dependency для получения текущего адвоката.

    FLOW:
    1. Извлекаем токен из заголовка Authorization: Bearer <token>
    2. Декодируем JWT (SecurityService.decode_token)
    3. Проверяем сессию в Redis (SessionStorage.get_session)
    4. Возвращаем данные адвоката

    Returns:
        {'id': 123, 'email': 'attorney@example.com', 'name': 'John Doe'}
    '''

    token = credentials.credentials

    try:
        # 1. Проверяем JWT подпись (SecurityService)
        payload = SecurityService.decode_token(token)

        # 2. Проверяем сессию в Redis
        session = await SessionStorage.get_session(token)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Session expired',
            )

        # 3. Продлеваем TTL
        await SessionStorage.refresh_session_ttl(token)

        return session

    except ValueError as e:
        # SecurityService выбросил ошибку
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
