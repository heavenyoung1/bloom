from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from backend.infrastructure.models.mixins import TimeStampMixin
from typing import TYPE_CHECKING

from backend.infrastructure.models._base import Base
from sqlalchemy import Integer, String as SQLString, Boolean

if TYPE_CHECKING:
    from backend.infrastructure.models import (
        Base,
        EventORM,
        ClientORM,
        DocumentORM,
        CaseORM,
    )


class AttorneyBase(Base):
    '''Промежуточный базовый класс для Attorney'''

    __abstract__ = True  # ← НЕ создавать отдельную таблицу

    # Поля от FastAPI Users
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        SQLString(320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(SQLString(1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AttorneyORM(AttorneyBase, TimeStampMixin):
    '''ORM модель юриста'''

    __tablename__ = 'attorneys'

    # Кастомные поля
    license_id: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    # Relationships
    clients: Mapped[list['ClientORM']] = relationship(
        back_populates='owner_attorney',
        cascade='save-update, merge',
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
