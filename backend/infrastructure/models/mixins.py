from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import event, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import DateTime
from sqlmodel import Field

class TimeStampMixin:
    created_at: datetime = Field(
        sa_column=mapped_column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()  # дефолт на уровне БД
        )
    )
    updated_at: datetime = Field(
        sa_column=mapped_column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now()
        )
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