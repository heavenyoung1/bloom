from datetime import datetime, date
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Date, DateTime, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin


if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM, ClientORM


class ClientPaymentORM(TimeStampMixin, Base):
    __tablename__ = 'client_payments'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )
    attorney_id: Mapped[int] = mapped_column(
        ForeignKey('attorneys.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )

    # Денежные поля
    paid: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    paid_str: Mapped[str] = mapped_column(String(512), nullable=False)

    # Даты
    pade_date: Mapped[date] = mapped_column(Date, nullable=False)
    paid_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    status: Mapped[str] = mapped_column(String(50), nullable=False)

    taxable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    condition: Mapped[str | None] = mapped_column(String(255))

    # Отношения
    attorney: Mapped['AttorneyORM'] = relationship(back_populates='client_payments')
    client: Mapped['ClientORM'] = relationship(back_populates='client_payments')