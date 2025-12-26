from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

from backend.infrastructure.models.client import Messenger

# Первый аргумент в Field (...) - эллипсис - что поле обязательно
# Если данные не заполнены, будет ошибка валидации.


class ClientCreateRequest(BaseModel):
    '''
    DTO для создания нового клиента

    ВАЖНО: owner_attorney_id НЕ включен!
    Передаётся из JWT токена в API слое.
    '''

    name: str = Field(
        ..., max_length=100, description='Название для Юр.лица либо ФИО для Физ.лица'
    )
    type: bool = Field(
        default=True, description='Тип клиента: True — физ.лицо, False — юр.лицо'
    )
    email: Optional[EmailStr] = Field(default=None, description='Email (необязательно)')
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
            }
        }
    )


class ClientUpdateRequest(BaseModel):
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
    email: Optional[EmailStr] = Field(default=None, description='Email (необязательно)')
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

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'Иванов Иван Иванович',
                'type': True,
                'email': 'client777@example.com',
                'phone': '+79691234232',
                'personal_info': '7744 443443',
                'address': 'г. Москва, ул. Пушкина, д.1',
                'messenger': 'Telegram',
                'messenger_handle': '@client111',
            }
        }
    )


class ClientResponse(BaseModel):
    '''DTO для ответа: полная информация о деле'''

    id: int
    name: str
    type: bool
    email: Optional[str] = None  # email: str
    phone: str
    personal_info: str  # ИНН/ПАСПОРТ
    address: str
    messenger: Messenger
    messenger_handle: str
    owner_attorney_id: int

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ClientListItemDTO(BaseModel):
    '''DTO для списка клиентов'''

    id: int  # Подумать над этим, нужно ли оно
    name: str
    phone: str
    messenger_handle: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
