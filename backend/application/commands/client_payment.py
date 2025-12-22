from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date

from backend.domain.entities.auxiliary import PaymentStatus

# ====== COMMANDS (write операции) ======
@dataclass
class CreatePaymentCommand:
    name: str
    client_id: int
    attorney_id: int
    paid: float
    paid_str: str
    pade_date: date
    paid_deadline: Optional[datetime]
    taxable: bool = False
    condition: Optional[str] = None
    status: PaymentStatus # В entites назначается дефолтное значение! проверить

@dataclass
class UpdatePaymentCommand:
    payment_id: int
    name: Optional[str] = None
    client_id: Optional[int] = None
    attorney_id: Optional[int] = None
    paid: Optional[float] = None
    paid_str: Optional[str] = None
    pade_date: Optional[date] = None
    paid_deadline: Optional[datetime] = None
    taxable: Optional[bool] = None
    condition: Optional[str] = None
    status: Optional[PaymentStatus] = None

@dataclass
class DeletePaymentCommand:
    payment_id: int

@dataclass
class GetPaymentByIdQuery:
    payment_id: int

@dataclass
class GetPaymentsForAttorneyQuery:
    attorney_id: int


# Специфичный метод для быстрого обновления статуса
# Можно использовать обычный метод Update, но там идет перебор множества
# условий if, тут обновляется всего лишь одно поле
@dataclass
class ChangePaymentStatusCommand:
    payment_id: int
    status: PaymentStatus







