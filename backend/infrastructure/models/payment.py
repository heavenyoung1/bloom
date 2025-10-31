from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from backend.infrastructure.models import SubscriptionORM


class PaymentORM(SQLModel, table=True):
    __tablename__ = 'payments'  # Таблица 'Платежи'

    id: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key='subscriptions.id', index=True)
    value: int = Field(description='Значение платежа в рублях')

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    subscription: 'SubscriptionORM' = Relationship(back_populates='payments')
