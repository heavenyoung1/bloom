import json
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from backend.domain.entities.session import RefreshSession
from backend.infrastructure.redis.interfaces.redis_storage import IRefreshSessionStore
from backend.infrastructure.redis.client import get_redis
from backend.core.settings import settings


class RedisRefreshSessionStore(IRefreshSessionStore):
    def __init__(self, redis):
        self.redis = redis

    @staticmethod
    def _key(jti: str) -> str:
        return f'auth:refresh:{jti}'

    @staticmethod
    def _user_sessions_key(user_id: UUID) -> str:
        return f'auth:user:{user_id}:sessions'

    async def save(self, session: RefreshSession) -> None:
        ttl = int((session.expires_at - datetime.utcnow()).total_seconds())
        data = json.dumps(
            {
                'jti': session.jti,
                'user_id': str(session.user_id),
                'user_agent': session.user_agent,
                'ip': session.ip,
                'expires_at': session.expires_at.isoformat(),
                'created_at': session.created_at.isoformat(),
            }
        )

        pipe = self.redis.pipeline()
        pipe.set(self._key(session.jti), data, ex=ttl)
        pipe.sadd(self._user_sessions_key(session.user_id), session.jti)
        pipe.execute()

    async def get(self, jti: str) -> Optional[RefreshSession]:
        raw = await self.redis.get(self._key(jti))
        if not raw:
            return None
        data = json.loads(raw)
        return RefreshSession(
            jti=data['jti'],
            user_id=UUID(data['user_id']),
            user_agent=data.get('user_agent'),
            ip=data.get('ip'),
            expires_at=datetime.fromisoformat(data['expires_at']),
            created_at=datetime.fromisoformat(data['created_at']),
        )

    async def delete(self, jti: str) -> None:
        # Вытащим user_id чтобы удалить из множества сессий
        raw = await self.redis.get(self._key(jti))
        pipe = self.redis.pipeline()
        if raw:
            data = json.loads(raw)
            pipe.srem(self._user_sessions_key(UUID(data['user_id'])), jti)
        pipe.delete(self._key(jti))
        await pipe.execute()

    async def delete_all_for_user(self, user_id: UUID) -> None:
        user_key = self._user_sessions_key(user_id)
        jtis = await self.redis.smembers(user_key)
        pipe = self.redis.pipeline()
        for jti in jtis:
            pipe.delete(self._key(jti))
        pipe.delete(user_key)
        await pipe.execute()

    async def list_for_user(self, user_id: UUID) -> List[RefreshSession]:
        user_key = self._user_sessions_key(user_id)
        jtis = await self.redis.smembers(user_key)
        sessions: List[RefreshSession] = []
        for jti in jtis:
            s = await self.get(jti)
            if s:
                sessions.append(s)
        return sessions
