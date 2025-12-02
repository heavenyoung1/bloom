from fastapi_users.authentication import (
    JWTStrategy,
)

from backend.core.settings import settings


def get_jwt_strategy() -> JWTStrategy:
    '''JWT-стратегия для FastAPI Users.'''
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
        token_audience=['fastapi-users:auth'],
        algorithm=settings.algorithm,
    )
