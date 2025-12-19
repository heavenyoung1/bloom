"""ORM модель для Outbox Pattern."""

from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum
from backend.infrastructure.models._base import Base
from backend.infrastructure.models.mixins import TimeStampMixin


class OutboxStatus(str, Enum):
    """Статусы обработки события в Outbox."""
    
    PENDING = 'pending'  # Ожидает обработки
    PROCESSING = 'processing'  # В процессе обработки
    COMPLETED = 'completed'  # Успешно обработано
    FAILED = 'failed'  # Ошибка обработки


class OutboxEventType(str, Enum):
    """Типы событий в Outbox."""
    
    ATTORNEY_REGISTERED = 'attorney_registered'  # Регистрация адвоката


class OutboxORM(TimeStampMixin, Base):
    """ORM модель для таблицы outbox."""
    
    __tablename__ = 'outbox'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    payload: Mapped[str] = mapped_column(Text, nullable=False)  # JSON строка
    status: Mapped[str] = mapped_column(
        String(20), 
        nullable=False, 
        default=OutboxStatus.PENDING.value,
        index=True
    )
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

