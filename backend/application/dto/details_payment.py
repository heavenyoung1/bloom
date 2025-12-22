
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from typing import Optional
from datetime import datetime

# ====== COMMANDS (write операции) ======

class PaymentCreateRequest(BaseModel):
    '''DTO для создания платежной информации юриста'''
    inn: str
    attorney_id: int
    index_address: str
    address: str
    bank_account: str
    correspondent_account: str
    bik: str
    bank_recipient: str
    kpp: Optional[str]  = None


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