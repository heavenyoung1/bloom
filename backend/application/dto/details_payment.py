
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from typing import Optional
from datetime import datetime

# ====== COMMANDS (write операции) ======

class PaymentDetailCreateRequest(BaseModel):
    '''DTO для создания платежной информации юриста'''
    inn: str = Field(..., max_length=12)
    index_address: str = Field(..., max_length=6)
    address: str = Field(..., max_length=255)
    bank_account: str = Field(..., max_length=20)
    correspondent_account: str = Field(..., max_length=20)
    bik: str = Field(..., max_length=9)
    bank_recipient: str = Field(..., max_length=255)
    kpp: Optional[str]  = Field(None, max_length=9)
# Как правильно передать KPP

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'inn': '1234567843',
                'index_address': '241099',
                'address': 'г. Санкт-Петербург, ул. Площадь Восстания, д.10, кв. 54',
                'bank_account': '12345678912345678921',
                'correspondent_account': '14680414794257063165',
                'bik': '987654319',
                'bank_recipient': 'ПАО "Z - банк", лудший банк, филиал в Мухосранске',
                'kpp': '123456754',
            }
        }
    )

class PaymentDetailUpdateRequest(BaseModel):
    '''DTO для обновления платежной информации юриста'''
    attorney_id: int = Field(
        ...,
        gt=0,
        description='ID юриста, ответственного за клиента',
    )
    inn: str = Field(None, max_length=12)
    index_address: str = Field(None, max_length=6)
    address: str = Field(None, max_length=255)
    bank_account: str = Field(None, max_length=20)
    correspondent_account: str = Field(None, max_length=20)
    bik: str = Field(None, max_length=9)
    bank_recipient: str = Field(None, max_length=255)
    kpp: Optional[str]  = Field(None, max_length=9)

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'inn': '1234567890',
                'attorney_id': 777,
                'index_address': '241033',
                'address': 'г. Санкт-Петербург, ул. Площадь Восстания, д.10, кв. 55',
                'bank_account': '12345678912345678912',
                'correspondent_account': '14680414794257063170',
                'bik': '987654321',
                'bank_recipient': 'ПАО "O - банк", плохой банк, филиал в Мухосранске',
                'kpp': '123456789',
            }
        }
    )



class PaymentDetailResponse(BaseModel):
    id: int                         # ID платежной информации
    attorney_id: int                # Владелец платежа - юрист
    inn: str                        # ИНН получателя
    kpp: Optional[str]              # КПП
    index_address: str              # Индекс адреса
    address: str                    # Адрес 
    bank_account: str               # Номер расчетного счета
    correspondent_account: str      # Корреспондентский счет
    bik: str                        # БИК
    bank_recipient: str             # Банк-получатель

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)