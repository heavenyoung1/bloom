from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator
from typing import Optional
from datetime import datetime
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate

# ⚠️ Первый аргумент в Field (...) - эллипсис -> поле обязательно
# ⚠️ Если данные не заполнены, будет ошибка валидации.

# ============= FastAPI Users схемы =============


class AttorneyCreate(BaseUserCreate):
    '''Схема для регистрации нового юриста'''

    license_id: str = Field(
        ..., min_length=3, max_length=12, description='Номер удостоверения'
    )
    first_name: str = Field(..., min_length=2, max_length=50, description='Имя')
    last_name: str = Field(..., min_length=3, max_length=50, description='Фамилия')
    patronymic: str = Field(..., min_length=3, max_length=20, description='Отчество')
    phone: str = Field(
        ..., pattern=r'^\+7\d{10}$', description='Телефон в формате +7XXXXXXXXXX'
    )

    @field_validator('first_name', 'last_name', 'patronymic')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        '''Очистка имён от лишних пробелов'''
        if v:
            return v.strip().title()
        return v

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'license_id': '153/3232',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'patronymic': 'Сергеевич',
                'email': 'ivan@example.com',
                'phone': '+79991234567',
                'hashed_password': 'SecurePass123!',
            }
        }
    )


class AttorneyRead(BaseUser[int]):
    '''Схема для чтения данных юриста (после авторизации)'''

    license_id: str
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    created_at: datetime  # ✅ Не Optional (БД гарантирует значение)
    updated_at: datetime  # ✅ Не Optional

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'id': 123,
                'email': 'ivan@example.com',
                'license_id': '153/3232',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'patronymic': 'Сергеевич',
                'phone': '+79991234567',
                'is_active': True,
                'is_superuser': False,
                'is_verified': False,
                'created_at': '2025-01-01T10:00:00',
                'updated_at': '2025-01-01T10:00:00',
            }
        },
    )


class AttorneyUpdate(BaseUserUpdate):
    '''Схема для обновления профиля юриста'''

    license_id: Optional[str] = Field(default=None, min_length=3, max_length=12)
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=20)
    last_name: Optional[str] = Field(default=None, min_length=3, max_length=20)
    patronymic: Optional[str] = Field(default=None, min_length=3, max_length=20)
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[str] = Field(default=None, pattern=r'^\+7\d{10}$')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'license_id': '153/3232',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'patronymic': 'Сергеевич',
                'email': 'ivan@example.com',
                'phone': '+79991234567',
            }
        }
    )


# ============= ОРИГИНАЛЬНЫЕ DTO (оставляем для внутренней логики) =============
# ============= УДАЛИТЬ ПОСЛЕ ПРОВЕРОК!!! =============

# class CreateAttorneyDTO(BaseModel):
#     '''DTO для внутреннего использования в сервисах'''

#     license_id: str = Field(
#         ..., min_length=3, max_length=12, description='Номер удостоверения'
#     )
#     first_name: str = Field(..., min_length=3, max_length=20, description='Имя')
#     last_name: str = Field(..., min_length=3, max_length=20, description='Фамилия')
#     patronymic: str = Field(..., min_length=3, max_length=20, description='Отчество')
#     email: EmailStr = Field(
#         ..., description='Email'
#     )  # to_lowercase=True, -> deprecated
#     phone: str = Field(
#         ..., pattern=r'^\+7\d{10}$', description='Телефон в формате +7XXXXXXXXXX'
#     )
#     password: SecretStr = Field(..., min_length=8, description='Минимум 8 символов')

#     model_config = ConfigDict(
#         json_schema_extra={
#             'example': {
#                 'license_id': '153/3232',
#                 'first_name': 'Иван',
#                 'last_name': 'Петров',
#                 'patronymic': 'Сергеевич',
#                 'email': 'ivan@example.com',
#                 'phone': '+79991234567',
#                 'password': 'SecurePass123!',
#             }
#         }
#     )


# class UpdateAttorneyDTO(BaseModel):
#     '''DTO для обновления (внутреннее)'''

#     license_id: Optional[str] = Field(default=None, min_length=3, max_length=12)
#     first_name: Optional[str] = Field(default=None, min_length=3, max_length=20)
#     last_name: Optional[str] = Field(default=None, min_length=3, max_length=20)
#     patronymic: Optional[str] = Field(default=None, min_length=3, max_length=20)
#     email: Optional[EmailStr] = Field(default=None)
#     phone: Optional[str] = Field(default=None, pattern=r'^\+7\d{10}$')

#     model_config = ConfigDict(
#         json_schema_extra={
#             'example': {
#                 'license_id': '153/3232',
#                 'first_name': 'Иван',
#                 'last_name': 'Петров',
#                 'patronymic': 'Сергеевич',
#                 'email': 'ivan@example.com',
#                 'phone': '+79991234567',
#             }
#         }
#     )


# class AttorneyResponseDTO(BaseModel):
#     '''DTO для ответа (внутреннее)'''

#     id: int
#     license_id: str
#     first_name: str
#     last_name: str
#     patronymic: str
#     email: str
#     phone: str
#     is_active: bool
#     created_at: Optional[datetime]  # Делаем эти поля опциональными
#     updated_at: Optional[datetime]  # Делаем эти поля опциональными

#     model_config = ConfigDict(
#         from_attributes=True,
#         json_schema_extra={
#             'example': {
#                 'id': 123,
#                 'license_id': '153/3232',
#                 'first_name': 'Иван',
#                 'last_name': 'Петров',
#                 'patronymic': 'Сергеевич',
#                 'email': 'ivan@example.com',
#                 'phone': '+79991234567',
#                 'is_active': True,
#                 'created_at': '2025-01-01T10:00:00',
#                 'updated_at': '2025-10-01T15:30:00',
#             }
#         },
#     )

# ============= Дополнительные схемы =============


class ChangePasswordDTO(BaseModel):
    '''DTO для смены пароля'''

    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

    # ✅ Валидация нового пароля
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str, info) -> str:
        '''Новый пароль должен отличаться от старого'''
        if 'current_password' in info.data and v == info.data['current_password']:
            raise ValueError('Новый пароль должен отличаться от текущего')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'current_password': 'OldPass123!',
                'new_password': 'NewSecurePass456!',
            }
        }
    )


# ПОЧЕМУ СБРАСЫВАЕМ ЧЕРЕЗ EMAIL
class ResetPasswordRequestDTO(BaseModel):
    '''DTO для запроса сброса пароля через email'''

    email: EmailStr


class ResetPasswordConfirmDTO(BaseModel):
    '''DTO для подтверждения сброса пароля'''

    token: str = Field(..., description='Токен из письма')
    new_password: str = Field(..., min_length=8, description='Новый пароль')
