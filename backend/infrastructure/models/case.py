from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from backend.infrastructure.models import (
        AttorneyORM,
        ClientORM,
        ContactORM,
        DocumentORM,
        EventORM,
    )


class CaseORM(TimeStampMixin, Base):
    __tablename__ = 'cases'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False, index=True
    )
    attorney_id: Mapped[int] = mapped_column(
        ForeignKey('attorneys.id', ondelete='RESTRICT'), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    # Отношения
    attorney: Mapped['AttorneyORM'] = relationship(back_populates='cases')
    client: Mapped['ClientORM'] = relationship(back_populates='cases')

    contact: Mapped['ContactORM'] = relationship(
        back_populates='case', cascade='all, delete-orphan'
    )
    documents: Mapped[list['DocumentORM']] = relationship(
        back_populates='case', cascade='all, delete-orphan'
    )
    events: Mapped[list['EventORM']] = relationship(
        back_populates='case', cascade='all, delete-orphan'
    )
