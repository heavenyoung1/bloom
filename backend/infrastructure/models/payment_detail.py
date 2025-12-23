from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin

if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM


class PaymentDetailORM(TimeStampMixin, Base):
    __tablename__ = 'payment_details'

    id: Mapped[int] = mapped_column(primary_key=True)

    attorney_id: Mapped[int] = mapped_column(
        ForeignKey('attorneys.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
        unique=True,
    )

    inn: Mapped[str] = mapped_column(String(12), nullable=False)        
    kpp: Mapped[str | None] = mapped_column(String(9))

    index_address: Mapped[str] = mapped_column(String(6), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    bank_account: Mapped[str] = mapped_column(String(20), nullable=False)
    correspondent_account: Mapped[str] = mapped_column(String(20), nullable=False)
    bik: Mapped[str] = mapped_column(String(9), nullable=False)
    bank_recipient: Mapped[str] = mapped_column(String(255), nullable=False)

    # Связь
    attorney: Mapped['AttorneyORM'] = relationship(back_populates='payment_detail')
