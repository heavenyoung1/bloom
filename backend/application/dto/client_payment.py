from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


from backend.domain.entities.auxiliary import PaymentStatus


class PaymentClientCreateRequest(BaseModel):
    '''DTO для создания клиентского платежа'''
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
    paid_deadline: date | None = Field(
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

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'Оплата юридических услуг по уголовному делу № 151093',
                'client_id': 777,
                'attorney_id': 777,
                'paid': 30000.05,
                'paid_str': 'Тридцать тысяч рублей, пять копеек',
                'pade_date': '2026.01.12',
                'paid_deadline': '2026.01.21',
                'taxable': False,
                'condition': 'Оплата производится в течение пяти дней с момента выставления счета.',
                'status': 'Выставлен',
            }   
        }
    )

class PaymentClientUpdateRequest(BaseModel):
    '''DTO для создания клиентского платежа'''
    name: str = Field(None, max_length=255)
    client_id: int = Field(None)
    attorney_id: int = Field(None)
    paid: float = Field(None)
    paid_str: str = Field(None)
    pade_date: date | None = Field(None)
    paid_deadline: date | None = Field(None)
    taxable: bool = Field(None)
    condition: Optional[str] = Field(None)
    status: PaymentStatus = Field(PaymentStatus.pending)

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'Оплата юридических услуг по уголовному делу № 151093',
                'client_id': 777,
                'attorney_id': 777,
                'paid': 30000.05,
                'paid_str': 'Тридцать тысяч рублей, пять копеек',
                'pade_date': '2026.01.12',
                'paid_deadline': '2026.01.21',
                'taxable': False,
                'condition': 'Оплата производится в течение пяти дней с момента выставления счета.',
                'status': 'Выставлен',
            }   
        }
    )


class PaymentClientResponse(BaseModel):
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
