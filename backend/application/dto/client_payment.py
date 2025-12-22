from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


from backend.domain.entities.auxiliary import PaymentStatus


@dataclass
class PaymentCreateRequest():
    name: str = Field(
        ...,
        max_length=255, 
        description='Наименование услуги',
        )
    client_id: int = Field(
        ...,
        gt=0,
        description='ID клиента, которому создать платеж',
    )
    attorney_id: int = Field(
        ...,
        gt=0,
        description='Владелец платежа',
    )
    paid: float = Field(
        ...,
        description='Сумма платежа (ЦИФРАМИ)',
    )
    paid_str: str = Field(
        ...,
        description='Сумма платежа (ПРОПИСЬЮ)',
    )
    pade_date: date | None = Field(
        ...,
        description='Дата формирования платежа',
    )
    paid_deadline: datetime | None = Field(
        None,
        description='Срок оплаты',
    )
    taxable: bool = Field(
        None,
    )
    condition: Optional[str] = Field(
        None,
    )
    status: PaymentStatus = Field(
        PaymentStatus.pending,
        description='Статус платежа',
    )

class PaymentResponse(BaseModel):
    '''DTO для ответа: полная информация о платеже'''
    id: int
    name: str
    client_id: int
    attorney_id: int
    paid: float
    paid_str: str
    pade_date: date
    paid_deadline: Optional[datetime]
    status: PaymentStatus
    taxable: bool = False
    condition: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
