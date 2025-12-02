# # backend/application/services/auth_service/app.py
# from contextlib import asynccontextmanager

# from fastapi import Depends, FastAPI

# from backend.application.dto.attorney import (
#     AttorneyCreate,
#     AttorneyRead,
#     AttorneyUpdate,
# )
# from backend.infrastructure.models.attorney import AttorneyORM
# from backend.application.services.auth_service_dor.users import (
#     auth_backend,
#     current_active_user,
#     fastapi_users,
# )

# # Делаем алиасы, чтобы сигнатуры совпадали с документацией
# UserCreate = AttorneyCreate
# UserRead = AttorneyRead
# UserUpdate = AttorneyUpdate


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # В твоём случае миграции делает Alembic, поэтому create_db_and_tables не нужен
#     yield


# app = FastAPI(lifespan=lifespan, title='Auth Service')


# # === Роуты аутентификации и управления пользователями ===

# # Логин / логаут (JWT)
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix='/auth',
#     tags=['auth'],
# )

# # Регистрация
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix='/auth',
#     tags=['auth'],
# )

# # Сброс пароля
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix='/auth',
#     tags=['auth'],
# )

# # Верификация email
# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix='/auth',
#     tags=['auth'],
# )

# # Управление пользователями (/users, /users/me и т.п.)
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix='/users',
#     tags=['users'],
# )


# # Пример защищённого маршрута — полностью как в доке
# @app.get('/authenticated-route')
# async def authenticated_route(user: AttorneyORM = Depends(current_active_user)):
#     return {'message': f'Hello {user.email}!'}
