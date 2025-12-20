from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator
from typing import Optional
from datetime import datetime
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


# ⚠️ Первый аргумент в Field (...) - эллипсис -> поле обязательно
# ⚠️ Если данные не заполнены, будет ошибка валидации.

# ============= FastAPI Users схемы =============


class RegisterRequest(BaseUserCreate):
    '''Запрос на регистрацию'''

    license_id: str = Field(
        ..., min_length=3, max_length=12, description='Номер удостоверения'
    )
    telegram_username: str = Field(min_length=4, max_length=50, description='Telegram никнейм')
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
                'telegram_username': 'advokat1234',
                'phone': '+79991234567',
                'password': 'SecurePass123!',
            }
        }
    )


class AttorneyResponse(BaseUser[int]):
    '''Ответ с данными юриста'''

    license_id: str
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    telegram_username: Optional[str]
    created_at: Optional[datetime]  # ✅ Не Optional (БД гарантирует значение)
    updated_at: Optional[datetime]  # ✅ Не Optional

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'id': 123,
                'email': 'ivan@example.com',
                'telegram_username': 'advokat1234',
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


class UpdateRequest(BaseUserUpdate):
    '''Схема для обновления профиля юриста'''

    license_id: Optional[str] = Field(default=None, min_length=3, max_length=12)
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=20)
    last_name: Optional[str] = Field(default=None, min_length=3, max_length=20)
    patronymic: Optional[str] = Field(default=None, min_length=3, max_length=20)
    email: Optional[EmailStr] = Field(default=None)
    telegram_username: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None, pattern=r'^\+7\d{10}$')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'license_id': '153/3232',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'patronymic': 'Сергеевич',
                'email': 'ivan@example.com',
                'telegram_username': 'advokat1234',
                'phone': '+79991234567',
            }
        }
    )


class LoginRequest(BaseModel):
    '''Запрос на логин'''

    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'email': 'ivan@example.com',
                'password': 'SecurePass123!',
            }
        }
    )

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'email': 'ivan@example.com',
                'password': 'SecurePass123!',
            }
        }
    )


class VerifyEmailRequest(BaseModel):
    '''Запрос на верификацию email'''

    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'email': 'ivan@example.com',
                'code': '000000',
            }
        }
    )


class ResendVerificationRequest(BaseModel):
    '''Повторная отправка кода'''

    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'email': 'ivan@example.com',
            }
        }
    )


class RefreshTokenRequest(BaseModel):
    '''Запрос на обновление access token'''

    refresh_token: str = Field(..., description='Refresh token для получения нового access token')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
            }
        }
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
    expires_in: int  # секунды


class AttorneyVerificationUpdateRequest(BaseModel):
    '''Запрос на изменение статуса верификации юриста.'''

    email: EmailStr
    is_verified: bool


class AttorneyVerificationResponse(BaseModel):
    '''Ответ по обновлённому статусу юриста.'''

    id: int
    email: EmailStr
    is_verified: bool
    token: str


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

# class ResetPasswordRequest(BaseModel):
#     '''DTO для запроса сброса пароля через email'''
#     email: EmailStr


class ResetPasswordConfirmDTO(BaseModel):
    '''DTO для подтверждения сброса пароля'''
    token: str = Field(..., description='Токен из письма')
    new_password: str = Field(..., min_length=8, description='Новый пароль')



class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'email': 'ivan@example.com',
            }
        }
    )

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=4, max_length=12)
    new_password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'email': 'ivan@example.com',
                'code': '000000',
                'new_password': 'Sobaka1234%'
            }
        }
    )

class PasswordResetResponse(BaseModel):
    ok: bool = True