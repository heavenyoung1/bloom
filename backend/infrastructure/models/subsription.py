from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM, PaymentORM


class SubscriptionORM(SQLModel, table=True):
    __tablename__ = 'subscriptions'

    id: Optional[int] = Field(primary_key=True)
    attorney_id: int = Field(foreign_key='attorneys.id', index=True)
    status: bool = Field(description='True/False — Активность подписки')
    period_start: datetime
    period_end: datetime

    attorney: 'AttorneyORM' = Relationship(back_populates='subscriptions')
    payments: List['PaymentORM'] = Relationship(back_populates='subscription')
