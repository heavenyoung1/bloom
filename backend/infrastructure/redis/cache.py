import json
from typing import Callable, TypeVar, Awaitable

from redis.asyncio import Redis

T = TypeVar('T')


async def cached_json(
    redis: Redis,
    key: str,
    ttl: int,
    loader: Callable[[], Awaitable[dict | None]],
) -> dict | None:
    raw = await redis.get(key)
    if raw:
        return json.loads(raw)

    data = await loader()
    if data is None:
        return None

    await redis.set(key, json.dumps(data), ex=ttl)
    return data
