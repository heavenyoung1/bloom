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
    '''Получить фабрику UoW'''
    return UnitOfWorkFactory(database)

# ========== JWT AUTHENTICATION ==========

security = HTTPBearer()


async def get_current_attorney(
    credentials: HTTPBasicCredentials = Depends(security),
) -> Dict[str, Any]:
    '''
    Получить текущего юриста из JWT токена.
    
    Используется в Depends() для защиты эндпоинтов.
    
    Args:
        credentials: Автоматически извлекаются из заголовка Authorization: Bearer <token>
    
    Returns:
        Декодированный payload с attorney_id и другими данными
    
    Raises:
        HTTPException 401: Если токен невалиден или истёк
    
    Example:
        @router.get('/profile')
        async def get_profile(
            current_attorney: dict = Depends(get_current_attorney)
        ):
            attorney_id = current_attorney['sub']
            return await get_attorney_by_id(attorney_id)
    '''
    
    token = credentials.credentials
    
    try:
        # Декодируем JWT токен
        payload = SecurityService.decode_token(token)
        
        # Проверяем, что это access токен (не refresh)
        if not SecurityService.verify_token_type(payload, 'access'):
            logger.warning('Попытка использовать refresh token вместо access token')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type. Use access token',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        
        attorney_id: str = payload.get('sub')
        if attorney_id is None:
            logger.warning('Token payload missing subject')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token invalid',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        
        return payload
        
    except ValueError as e:
        logger.warning(f'JWT validation error: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except Exception as e:
        logger.error(f'Unexpected error during token verification: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
