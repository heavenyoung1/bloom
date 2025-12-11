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
from backend.core.logger import logger

# ========== ASYNC SESSION ==========


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.get_session() as session:
        yield session


# ========== UOW FACTORY ==========


async def get_uow_factory() -> UnitOfWorkFactory:
    '''
    Получить фабрику UnitOfWork для использования в UseCase'ах.

    Используется в каждом Router'е для передачи в UseCase.

    Returns:
        UnitOfWorkFactory для работы с БД
    '''
    return UnitOfWorkFactory(database)


# ========== JWT AUTHENTICATION ==========

security = HTTPBearer()


async def get_current_attorney_id(
    credentials: HTTPBasicCredentials = Depends(security),
) -> int:
    '''
    Получить ID текущего адвоката из JWT токена.

    Используется в Depends() для защиты эндпоинтов.

    Args:
        credentials: Автоматически извлекаются из заголовка Authorization: Bearer <token>

    Returns:
        attorney_id как int

    Raises:
        HTTPException 401: Если токен невалиден, истёк или неправильного типа

    Example:
        @router.get('/profile')
        async def get_profile(
            current_attorney_id: int = Depends(get_current_attorney_id)
        ):
            return await get_attorney(current_attorney_id)
    '''
    token = credentials.credentials

    try:
        # 1. Декодируем JWT токен
        payload = SecurityService.decode_token(token)

        # 2. Проверяем, что это access токен (не refresh)
        if not SecurityService.verify_token_type(payload, 'access'):
            logger.warning(
                f'Попытка использовать неправильный тип токена: '
                f'{payload.get('type')}'
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неправильный тип токена. Используйте access token',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        # 3. Получаем attorney_id из токена
        attorney_id_str = SecurityService.get_subject_from_token(payload)
        attorney_id = int(attorney_id_str)

        logger.debug(f'Attorney {attorney_id} автентифицирован')
        return attorney_id

    except ValueError as e:
        logger.warning(f'JWT validation error: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Невалидный или истёкший токен',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    except Exception as e:
        logger.error(f'Unexpected error during token verification: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось верифицировать учетные данные',
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def get_current_access_token(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    '''
    Получить текущий access token (для logout и т.д.).

    Returns:
        access token как строка
    '''
    return credentials.credentials
