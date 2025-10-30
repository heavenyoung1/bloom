from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.infrastructure.models import Payment
    from backend.infrastructure.models import Attorney

class Subscription(SQLModel, table=True):

    id: Optional[int] = Field(primary_key=True)
    attorney_id: int = Field(foreign_key='attorneys.id', index=True)
    status: bool = Field(description='True/False — Активность подписки')
    period_start: datetime
    period_end: datetime

    attorney: 'Attorney' = Relationship(back_populates='subscriptions')
    payments: List['Payment'] = Relationship(back_populates='subscription')