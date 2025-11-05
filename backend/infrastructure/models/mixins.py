from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import event, Column
from sqlalchemy.types import DateTime
from sqlmodel import Field

class TimeStampMixin:
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: Optional[datetime] = Field(
            default=None,
            sa_column=Column(DateTime(timezone=True), nullable=False)
        )
    
    def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)

            @event.listens_for(cls, 'before_insert', propagate=True)
            def set_created(mapper, connection, target):
                now = datetime.now(timezone.utc)
                target.created_at = now
                target.updated_at = now

            @event.listens_for(cls, 'before_update', propagate=True)
            def set_updated(mapper, connection, target):
                target.updated_at = datetime.now(timezone.utc)