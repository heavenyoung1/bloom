from fastapi_users import FastAPIUsers

from backend.infrastructure.models.attorney import AttorneyORM
from backend.infrastructure.auth.user_manager import get_user_manager
from backend.infrastructure.auth.strategy import auth_backend


fastapi_users = FastAPIUsers[AttorneyORM, int](
    get_user_manager,
    [auth_backend],
)

# Depends для использования в роутерах
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
