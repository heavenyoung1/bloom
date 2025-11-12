from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import Optional
from datetime import datetime

# Первый аргумент в Field (...) - эллипсис - что поле обязательно
# Если данные не заполнены, будет ошибка валидации.


class CreateAttorneyDTO(BaseModel):
    '''DTO для создания нового юриста'''

    license_id: str = Field(
        ..., min_length=3, max_length=12, description='Номер удостоверения'
    )
    first_name: str = Field(..., min_length=3, max_length=20, description='Имя')
    last_name: str = Field(..., min_length=3, max_length=20, description='Фамилия')
    patronymic: str = Field(..., min_length=3, max_length=20, description='Отчество')
    email: EmailStr = Field(..., to_lowercase=True, description='Email')
    phone: str = Field(
        ..., regex=r'^\+7\d{10}$', description='Телефон в формате +7XXXXXXXXXX'
    )
    password: SecretStr = Field(..., min_length=8, description='Минимум 8 символов')

    class Config:
        schema_extra = {
            'example': {
                'attorney_id': '153/3232',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'patronymic': 'Сергеевич',
                'email': 'ivan@example.com',
                'phone': '+79991234567',
                'password': 'SecurePass123!',
            }
        }


class UpdateAttorneyDTO(BaseModel):
    '''
    DTO для обновления юриста
    Если при обновлении указано любое из полей, оно будет обновлено!
    '''

    license_id: Optional[str] = Field(default=None, min_length=3, max_length=12)
    first_name: Optional[str] = Field(default=None, min_length=3, max_length=20)
    last_name: Optional[str] = Field(default=None, min_length=3, max_length=20)
    patronymic: Optional[str] = Field(default=None, min_length=3, max_length=20)
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[str] = Field(default=None, regex=r'^\+7\d{10}$')

    class Config:
        schema_extra = {
            'example': {
                'attorney_id': '153/3232',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'patronymic': 'Сергеевич',
                'email': 'ivan@example.com',
                'phone': '+79991234567',
            }
        }


class AttorneyResponseDTO(BaseModel):
    '''DTO для ответа: полная информация о юристе'''

    id: int
    license_id: str
    first_name: str
    last_name: str
    patronymic: str
    email: str
    phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        schema_extra = {
            'example': {
                'id': 123,
                'license_id': '153/3232',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'patronymic': 'Сергеевич',
                'email': 'ivan@example.com',
                'phone': '+79991234567',
                'is_active': True,
                'created_at': '2025-01-01T10:00:00',
                'updated_at': '2025-10-01T15:30:00',
            }
        }


# В текущей реализации ПОКА НЕ НУЖНО!
class AttorneyListItemDTO(BaseModel):
    '''DTO для списка юристов.'''

    id: int
    license_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    is_active: bool

    class Config:
        from_attributes = True


class LoginDTO(BaseModel):
    email: str
    password: str
