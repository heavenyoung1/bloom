from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator


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
        description='Дата формирования платежа (формат: YYYY-MM-DD или YYYY.MM.DD)',
    )
    paid_deadline: date | None = Field(
        None,
        description='Срок оплаты (формат: YYYY-MM-DD или YYYY.MM.DD)',
    )

    @field_validator('pade_date', 'paid_deadline', mode='before')
    @classmethod
    def parse_date(cls, v: Union[str, date, None]) -> Optional[date]:
        '''Парсит дату из строки, поддерживает форматы YYYY-MM-DD и YYYY.MM.DD'''
        if v is None:
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            # Заменяем точки на дефисы для парсинга
            normalized = v.replace('.', '-')
            try:
                return date.fromisoformat(normalized)
            except ValueError:
                raise ValueError(f'Неверный формат даты: {v}. Используйте YYYY-MM-DD или YYYY.MM.DD')
        return v
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
                'pade_date': '2026-01-12',  # Поддерживаются форматы: YYYY-MM-DD или YYYY.MM.DD
                'paid_deadline': '2026-01-21',  # Поддерживаются форматы: YYYY-MM-DD или YYYY.MM.DD
                'taxable': False,
                'condition': 'Оплата производится в течение пяти дней с момента выставления счета.',
                'status': 'Выставлен',
            }   
        }
    )

class PaymentClientUpdateRequest(BaseModel):
    '''DTO для обновления клиентского платежа'''
    name: str = Field(None, max_length=255)
    client_id: int = Field(None)
    attorney_id: int = Field(None)
    paid: float = Field(None)
    paid_str: str = Field(None)
    pade_date: date | None = Field(None, description='Дата формирования платежа (формат: YYYY-MM-DD или YYYY.MM.DD)')
    paid_deadline: date | None = Field(None, description='Срок оплаты (формат: YYYY-MM-DD или YYYY.MM.DD)')
    taxable: bool = Field(None)
    condition: Optional[str] = Field(None)
    status: PaymentStatus = Field(PaymentStatus.pending)

    @field_validator('pade_date', 'paid_deadline', mode='before')
    @classmethod
    def parse_date(cls, v: Union[str, date, None]) -> Optional[date]:
        '''Парсит дату из строки, поддерживает форматы YYYY-MM-DD и YYYY.MM.DD'''
        if v is None:
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            # Заменяем точки на дефисы для парсинга
            normalized = v.replace('.', '-')
            try:
                return date.fromisoformat(normalized)
            except ValueError:
                raise ValueError(f'Неверный формат даты: {v}. Используйте YYYY-MM-DD или YYYY.MM.DD')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'Оплата юридических услуг по уголовному делу № 151093',
                'client_id': 777,
                'attorney_id': 777,
                'paid': 30000.05,
                'paid_str': 'Тридцать тысяч рублей, пять копеек',
                'pade_date': '2026-01-12',  # Поддерживаются форматы: YYYY-MM-DD или YYYY.MM.DD
                'paid_deadline': '2026-01-21',  # Поддерживаются форматы: YYYY-MM-DD или YYYY.MM.DD
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

    model_config = ConfigDict(from_attributes=True)


class FullPaymentResponse(BaseModel):
    '''DTO для полного ответа с данными платежа и платежными реквизитами (18 параметров)'''
    payment_id: int
    payment_name: str
    client_id: int
    attorney_id: int
    paid: float
    paid_str: str
    pade_date: date
    paid_deadline: Optional[date]
    status: PaymentStatus
    taxable: bool
    condition: Optional[str]
    inn: str
    kpp: Optional[str]
    index_address: str
    address: str
    bank_account: str
    corr_account: str
    bik: str
    bank_recipient: str
    pdf_path: Optional[str] = Field(
        None,
        description='Путь к сгенерированному PDF документу'
    )

    model_config = ConfigDict(from_attributes=True)