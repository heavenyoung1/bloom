from fastapi import APIRouter, Depends

from backend.infrastructure.auth import (
    fastapi_users,
    auth_backend,
    current_active_user,
)
from backend.application.dto.attorney import (
    AttorneyRead,
    AttorneyCreate,
    AttorneyUpdate,
)
from backend.infrastructure.models.attorney import AttorneyORM

router = APIRouter(tags=['Authentication'])

# Register
router.include_router(
    fastapi_users.get_register_router(AttorneyRead, AttorneyCreate),
    prefix='/auth',
)

# Login/Logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth',
)

# Reset password
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
)

# Verify email
router.include_router(
    fastapi_users.get_verify_router(AttorneyRead),
    prefix='/auth',
)

# User profile management
router.include_router(
    fastapi_users.get_users_router(AttorneyRead, AttorneyUpdate),
    prefix='/users',
)


@router.get('/users/me', response_model=AttorneyRead)
async def get_current_user(
    user: AttorneyORM = Depends(current_active_user),
):
    '''Получить данные текущего авторизованного юриста'''
    return user
