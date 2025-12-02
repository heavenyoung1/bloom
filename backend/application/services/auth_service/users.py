from fastapi_users import FastAPIUsers

from backend.infrastructure.models.attorney import AttorneyORM
from backend.application.services.auth_service.user_manager import get_user_manager
from backend.application.services.auth_service.strategy import auth_backend


fastapi_users = FastAPIUsers[AttorneyORM, int](
    get_user_manager,
    [auth_backend],
)

# Зависимость 'текущий активный пользователь'
current_active_user = fastapi_users.current_user(active=True)
