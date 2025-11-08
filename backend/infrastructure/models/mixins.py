from __future__ import annotations
from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy.orm import declared_attr
from sqlalchemy import event  # <-- вот так


class TimeStampMixin:
    @declared_attr
    def created_at(cls):
        return sa.Column(
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls):
        return sa.Column(
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        )

    @classmethod
    def __declare_last__(cls):
        @event.listens_for(cls, "before_insert", propagate=True)
        def _set_created(mapper, connection, target):
            now = datetime.now(timezone.utc)
            if getattr(target, "created_at", None) is None:
                target.created_at = now
            target.updated_at = now

        @event.listens_for(cls, "before_update", propagate=True)
        def _set_updated(mapper, connection, target):
            target.updated_at = datetime.now(timezone.utc)
