from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING

from backend.infrastructure.models._base import Base

if TYPE_CHECKING:
    from backend.infrastructure.models import (
        Base,
        EventORM,
        ClientORM,
        DocumentORM,
        CaseORM,
    )


class AttorneyORM(TimeStampMixin, Base):
    __tablename__ = 'attorneys'

    id: Mapped[int] = mapped_column(primary_key=True)
    # НУЖНО НАЗВАНИЕ ПОМЕНЯТЬ!!!
    license_id: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )  # номер удостоверения
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 1:N
    clients: Mapped[list['ClientORM']] = relationship(
        back_populates='owner_attorney',
        cascade='save-update, merge',  # не удаляем клиентов вместе с адвокатом
        passive_deletes=True,
    )
    cases: Mapped[list['CaseORM']] = relationship(
        back_populates='attorney',
        cascade='save-update, merge',
        passive_deletes=True,
    )
    documents: Mapped[list['DocumentORM']] = relationship(
        back_populates='attorney',
        cascade='save-update, merge',
        passive_deletes=True,
    )
    events: Mapped[list['EventORM']] = relationship(
        back_populates='attorney',
        cascade='save-update, merge',
        passive_deletes=True,
    )
