from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from backend.infrastructure.models.billing import Subscription

class Payment(SQLModel, table=True):

    id: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key='subscriptions.id', index=True)
    value: int = Field(description='Значение платежа в рублях')

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    subscription: 'Subscription' = Relationship(back_populates='payments')