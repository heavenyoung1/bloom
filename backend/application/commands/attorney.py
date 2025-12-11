from dataclasses import dataclass
from typing import Optional


# ====== AUTH COMMANDS (write операции) ======


@dataclass
class RegisterAttorneyCommand:
    '''Регистрация нового адвоката'''
    license_id: str
    first_name: str
    last_name: str
    patronymic: Optional[str]
    email: str
    phone: Optional[str]
    password: str  # plaintext, будет захеширован в UseCase


@dataclass
class LoginAttorneyCommand:
    '''Вход в систему'''
    email: str
    password: str


@dataclass
class VerifyEmailCommand:
    '''Верификация email'''
    email: str
    code: str


@dataclass
class ResendVerificationCommand:
    '''Повторно отправить код верификации'''
    email: str


@dataclass
class RefreshTokenCommand:
    '''Обновить access token'''
    refresh_token: str


# ====== PROFILE COMMANDS (write операции) ======


@dataclass
class UpdateAttorneyCommand:
    '''Обновление профиля адвоката'''
    attorney_id: int
    
    # PATCH — все поля опциональные
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    license_id: Optional[str] = None


@dataclass
class ChangePasswordCommand:
    '''Изменение пароля'''
    attorney_id: int
    old_password: str
    new_password: str


@dataclass
class DeleteAttorneyAccountCommand:
    '''Удаление учетной записи'''
    attorney_id: int
    password: str  # подтверждение пароля


# ====== QUERIES (read операции) ======


@dataclass
class GetAttorneyByIdQuery:
    attorney_id: int


@dataclass
class GetAttorneyByEmailQuery:
    email: str