import redis.asyncio as redis
from typing import Optional, Any
import json

from backend.core.settings import settings


class RedisClient:
    def __init__(self):
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        self._client = await redis.from_url(settings.redis_url, decode_responses=True)

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        ttl = ttl or settings.redis_default_ttl
        if isinstance(value, dict):
            value = json.dumps(value)
        return await self._client.setex(key, ttl, value)

    async def get(self, key: str) -> Optional[Any]:
        value = await self._client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    async def delete(self, key: str) -> bool:
        return bool(await self._client.delete(key))

    async def increment(self, key: str, amount: int = 1) -> int:
        return await self._client.incrby(key, amount)

    async def exists(self, key: str) -> bool:
        return bool(await self._client.exists(key))


redis_client = RedisClient()
