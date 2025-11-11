# backend/infrastructure/models/document.py
from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM, CaseORM


class DocumentORM(TimeStampMixin, Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(300), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[str | None] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(500))

    case_id: Mapped[int] = mapped_column(
        ForeignKey('cases.id', ondelete='SET NULL'), index=True
    )
    attorney_id: Mapped[int] = mapped_column(
        ForeignKey('attorneys.id', ondelete='SET NULL'), index=True
    )

    case: Mapped['CaseORM'] = relationship(back_populates='documents')
    attorney: Mapped['AttorneyORM'] = relationship(back_populates='documents')
