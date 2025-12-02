from fastapi import HTTPException, status, Request
from backend.core.settings import settings
from backend.infrastructure.redis.client import get_redis


async def rate_limit_login(request: Request):
    redis = await get_redis()
    client_ip = request.client.host
    key = f'rl:login:{client_ip}'

    # atomically: INCR + set TTL
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, settings.LOGIN_RATE_PERIOD_SECONDS)

    if current > settings.LOGIN_RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Too many login attempts, try again later.',
        )
