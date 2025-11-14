from backend.infrastructure.models.client import Messenger

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

# Первый аргумент в Field (...) - эллипсис - что поле обязательно
# Если данные не заполнены, будет ошибка валидации.


class CreateClientDTO(BaseModel):
    '''DTO для создания нового клиента'''

    name: str = Field(
        ..., max_length=100, description='Название для Юр.лица либо ФИО для Физ.лица'
    )
    type: bool = Field(
        default=True, description='Тип клиента: True — физ.лицо, False — юр.лицо'
    )
    email: Optional[EmailStr] = Field(
        default=None, to_lowercase=True, description='Email (необязательно)'
    )
    phone: str = Field(
        ..., pattern=r'^\+7\d{10}$', description='Телефон в формате +7XXXXXXXXXX'
    )
    personal_info: str = Field(
        ...,
        max_length=20,
        description='ИНН (для юр.лиц) или номер паспорта (для физ.лиц)',
    )
    address: str = Field(..., max_length=255, description='Почтовый адрес')
    messenger: Messenger
    messenger_handle: str = Field(..., min_length=4, max_length=50)
    owner_attorney_id: int = Field(
        ..., description='ID юриста, ответственного за клиента'
    )

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'Иванов Иван Иванович',
                'type': True,
                'email': 'client@example.com',
                'phone': '+79991234567',
                'personal_info': '1212 443443',
                'address': 'г. Москва, ул. Пушкина, д.1',
                'messenger': 'Telegram',
                'messenger_handle': '@client123',
                'owner_attorney_id': 1,
            }
        }
    )


class UpdateClientDTO(BaseModel):
    '''DTO для частичного обновления клиента (PATCH)'''

    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description='Название для юр.лица либо ФИО для физ.лица',
    )
    type: Optional[bool] = Field(
        default=None,
        description='Тип клиента: True — физ.лицо, False — юр.лицо (если требуется изменить)',
    )
    email: Optional[EmailStr] = Field(
        default=None, to_lowercase=True, description='Email (необязательно)'
    )
    phone: Optional[str] = Field(
        default=None,
        pattern=r'^\+7\d{10}$',
        description='Телефон в формате +7XXXXXXXXXX',
    )
    personal_info: Optional[str] = Field(
        default=None,
        max_length=20,
        description='ИНН (для юр.лиц) или номер паспорта (для физ.лиц)',
    )
    address: Optional[str] = Field(
        default=None, max_length=150, description='Почтовый адрес'
    )
    messenger: Messenger
    messenger_handle: Optional[str] = Field(default=None, max_length=50)
    owner_attorney_id: Optional[int] = Field(
        default=None, ge=1, description='ID юриста, ответственного за клиента '
    )


class ClientListItemDTO(BaseModel):
    '''DTO для списка клиентов'''

    id: int  # Подумать над этим, нужно ли оно
    name: str
    phone: str
    messenger_handle: str

    model_config = ConfigDict(from_attributes=True)
