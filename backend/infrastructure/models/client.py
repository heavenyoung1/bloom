from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.domain.entities.auxiliary import Messenger
from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM, CaseORM


class ClientORM(TimeStampMixin, Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[bool] = mapped_column(nullable=False)  # True: физлицо / False: юрлицо
    email: Mapped[str | None] = mapped_column(String(50), index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    personal_info: Mapped[str] = mapped_column(String(20))  # ИНН или паспорт
    address: Mapped[str] = mapped_column(String(255))
    messenger: Mapped[Messenger] = mapped_column(String)  # enum можно добавить позже
    messenger_handle: Mapped[str] = mapped_column(String(50))

    owner_attorney_id: Mapped[int] = mapped_column(
        ForeignKey('attorneys.id', ondelete='RESTRICT'), nullable=False, index=True
    )

    # связи
    owner_attorney: Mapped['AttorneyORM'] = relationship(back_populates='clients')
    cases: Mapped[list['CaseORM']] = relationship(
        back_populates='client', cascade='all, delete-orphan'
    )
