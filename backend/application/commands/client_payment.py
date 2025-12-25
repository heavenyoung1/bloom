from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date

from backend.domain.entities.auxiliary import PaymentStatus


# ====== COMMANDS (write операции) ======
@dataclass
class CreateClientPaymentCommand:
    name: str
    client_id: int
    attorney_id: int
    paid: float
    paid_str: str
    pade_date: date
    paid_deadline: Optional[date]
    status: PaymentStatus = (
        PaymentStatus.issued
    )  # Дефолтное значение как в ClientPayment.create()
    taxable: bool = False
    condition: Optional[str] = None


@dataclass
class UpdateСlientPaymentCommand:
    payment_id: int
    name: Optional[str] = None
    client_id: Optional[int] = None
    attorney_id: Optional[int] = None  # зачем вот это передавать?
    paid: Optional[float] = None
    paid_str: Optional[str] = None
    pade_date: Optional[date] = None
    paid_deadline: Optional[date] = None
    taxable: Optional[bool] = None
    condition: Optional[str] = None
    status: Optional[PaymentStatus] = None


@dataclass
class DeleteСlientPaymentCommand:
    payment_id: int


@dataclass
class GetСlientPaymentByIdQuery:
    payment_id: int


@dataclass
class GetСlientPaymentForAttorneyQuery:
    attorney_id: int


@dataclass
class GetСlientPaymentForClientQuery:
    client_id: int


# Специфичный метод для быстрого обновления статуса
# Можно использовать обычный метод Update, но там идет перебор множества
# условий if, тут обновляется всего лишь одно поле
@dataclass
class UpdatePaymentCommand:
    '''Команда для обновления платежа (используется доменной сущностью)'''

    name: Optional[str] = None
    client_id: Optional[int] = None
    attorney_id: Optional[int] = None
    paid: Optional[float] = None
    paid_str: Optional[str] = None
    pade_date: Optional[date] = None
    paid_deadline: Optional[date] = None
    taxable: Optional[bool] = None
    condition: Optional[str] = None
    status: Optional[PaymentStatus] = None


@dataclass
class ChangePaymentStatusCommand:
    '''Команда для изменения статуса платежа (используется доменной сущностью)'''

    status: PaymentStatus


@dataclass
class ChangeСlientPaymentStatusCommand:
    payment_id: int
    status: PaymentStatus
