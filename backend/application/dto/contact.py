from backend.infrastructure.models.client import Messenger
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

# Первый аргумент в Field (...) - эллипсис - что поле обязательно
# Если данные не заполнены, будет ошибка валидации.


class CreateContactDTO(BaseModel):
    '''DTO для создания связанного контакта - как правило - доверителя.'''

    name: str = Field(..., min_length=1, max_length=100)
    personal_info: Optional[str] = Field(
        None, max_length=20, description='ИНН или паспорт'
    )
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    case_id: int

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'Петров Пётр Петрович',
                'personal_info': '12345678901234',
                'phone': '+79991234567',
                'email': 'contact@example.com',
                'case_id': 1,
            }
        }
    )


class UpdateContactDTO(BaseModel):
    '''DTO для обновления контакта'''

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    personal_info: Optional[str] = Field(None, max_length=20)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None


class ContactResponseDTO(BaseModel):
    '''DTO для ответа: полная информация о контакте'''

    id: int
    name: str
    personal_info: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    case_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
