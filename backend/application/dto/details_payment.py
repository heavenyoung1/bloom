
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from typing import Optional
from datetime import datetime

# ====== COMMANDS (write операции) ======

class PaymentCreateRequest(BaseModel):
    '''DTO для создания платежной информации юриста'''
    attorney_id: int
    inn: str
    index_address: str
    address: str
    bank_account: str
    correspondent_account: str
    bik: str
    bank_recipient: str
    kpp: Optional[str]  = None

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
                'bank_recipient': 'ПАО "Z - банк", лучший банк, филиал в Мухосранске',
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