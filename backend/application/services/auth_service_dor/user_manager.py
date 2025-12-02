# from typing import Optional, AsyncGenerator

# from fastapi import Depends, Request
# from fastapi_users import BaseUserManager, IntegerIDMixin
# from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

# from backend.infrastructure.models.attorney import AttorneyORM
# from backend.application.services.auth_service.database import get_user_db
# from backend.core.logger import logger
# from backend.core.settings import settings


# class UserManager(IntegerIDMixin, BaseUserManager[AttorneyORM, int]):
#     '''
#     Менеджер пользователей для Attorney.
#     Управляет регистрацией, сбросом пароля, верификацией email.
#     '''

#     # Секретный код для сброса пароля
#     reset_password_token_secret = settings.secret_key

#     # Секретный код для кодирования токена подтверждения
#     verification_token_secret = settings.secret_key

#     # ==== ХУКИ ИЗ ДОКУМЕНТАЦИИ FASTAPIUSERS ====

#     async def on_after_register(
#         self, user: AttorneyORM, request: Optional[Request] = None
#     ):
#         '''Колбэк после успешной регистрации'''
#         logger.info(f'Юрист зарегистрирован: {user.email} (ID: {user.id})')
#         # TODO: отправка email

#     # async def on_after_forgot_password(
#     #     self, user: AttorneyORM, token: str, request: Optional[Request] = None
#     # ):
#     #     '''Колбэк при запросе сброса пароля'''
#     #     logger.info(f'Запрос сброса пароля для: {user.email}')
#     #     # TODO: Отправить email с токеном
#     #     # await send_reset_password_email(user.email, token)

#     # async def on_after_request_verify(
#     #     self, user: AttorneyORM, token: str, request: Optional[Request] = None
#     # ):
#     #     '''Колбэк при запросе верификации email'''
#     #     logger.info(f'Запрос верификации: {user.email}')
#     #     # TODO: Отправить email с токеном верификации
#     #     # await send_verification_email(user.email, token)


# async def get_user_manager(
#     user_db: SQLAlchemyUserDatabase[AttorneyORM, int] = Depends(get_user_db),
# ) -> AsyncGenerator[UserManager, None]:
#     '''
#     Dependency для получения UserManager.

#     Используется FastAPI Users для создания роутеров аутентификации.
#     '''
#     yield UserManager(user_db)
