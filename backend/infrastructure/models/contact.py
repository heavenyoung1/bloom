from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:

    from backend.infrastructure.models import CaseORM


class ContactORM(SQLModel, table=True):
    __tablename__ = 'contacts'  # Таблица 'Связаные с делом контакты'

    id: int = Field(primary_key=True)
    name: str = Field(max_length=100, description='ФИО полностью')
    personal_info: Optional[str] = Field(
        default=None, description='Паспорт', max_length=20
    )
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    case_id: int = Field(foreign_key='cases.id', index=True)

    # relationships
    case: Optional['CaseORM'] = Relationship(back_populates='contacts')
