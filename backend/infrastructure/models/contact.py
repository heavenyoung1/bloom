from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models import CaseORM

class ContactORM(TimeStampMixin, Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    personal_info: Mapped[str] = mapped_column(String(20))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(50))

    case_id: Mapped[int] = mapped_column(ForeignKey('cases.id', ondelete='CASCADE'), nullable=False, index=True)
    case: Mapped['CaseORM'] = relationship(back_populates='contacts')
