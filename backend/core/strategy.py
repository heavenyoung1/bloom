from fastapi_users.authentication import (
    JWTStrategy,
)

from backend.core.settings import settings


def get_jwt_strategy() -> JWTStrategy:
    '''JWT-стратегия для FastAPI Users.'''
    return JWTStrategy(
        secret=settings.JWT_SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        token_audience=['fastapi-users:auth'],
        algorithm=settings.JWT_ALGORITHM,
    )
