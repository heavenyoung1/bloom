import json
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from backend.domain.entities.session import RefreshSession
from backend.infrastructure.redis.interfaces.redis_storage import IRefreshSessionStore
from backend.infrastructure.redis.client import redis_client
from backend.core.settings import settings
from backend.core.logger import logger
from typing import Dict, Any

class SessionStorage:
    '''
    Управление сессиями в Redis.

    Ответственность:
    ✅ Создать сессию при логине
    ✅ Получить сессию при запросе
    ✅ Удалить сессию при логауте
    ✅ Продлить TTL при активности
    '''

    SESSION_PREFIX = 'session'

    @staticmethod
    def _make_key(token: str) -> str:
        '''Сделать ключ Redis из токена'''
        return f'{SessionStorage.SESSION_PREFIX}:{token}'

    @staticmethod
    async def create_session(
        token: str,
        attorney_id: int,
        attorney_email: str,
        attorney_name: str,
    ) -> None:
        '''
        Создать сессию при логине.

        Args:
            token: JWT access token
            attorney_id: ID адвоката
            attorney_email: Email адвоката
            attorney_name: Имя адвоката
        '''

        key = SessionStorage._make_key(token)
        session_data = {
            'id': attorney_id,
            'email': attorney_email,
            'name': attorney_name,
        }

        # Сохраняем в Redis на 15 минут
        await redis_client.set(key, session_data, ttl=15 * 60)  # 15 минут

        logger.info(f'Session created for attorney {attorney_id}')

    @staticmethod
    async def get_session(token: str) -> Optional[Dict[str, Any]]:
        '''
        Получить сессию по токену.

        Returns:
            Данные сессии или None если не найдена/истекла
        '''

        key = SessionStorage._make_key(token)
        session = await redis_client.get(key)

        if not session:
            logger.warning('Session not found or expired')
            return None

        return session

    @staticmethod
    async def invalidate_session(token: str) -> None:
        '''
        Удалить сессию (logout).
        '''

        key = SessionStorage._make_key(token)
        await redis_client.delete(key)
        logger.info('Session invalidated')

    @staticmethod
    async def refresh_session_ttl(token: str) -> None:
        '''
        Продлить жизнь сессии (при активности).
        '''

        session = await SessionStorage.get_session(token)
        if session:
            await SessionStorage.create_session(
                token=token,
                attorney_id=session['id'],
                attorney_email=session['email'],
                attorney_name=session['name'],
            )
