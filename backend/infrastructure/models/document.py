from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.infrastructure.models import AttorneyORM, CaseORM


class DocumentORM(SQLModel, table=True):
    __tablename__ = 'documents'  # Таблица 'Связаные с делом Документы'

    id: int = Field(default=None, primary_key=True)
    file_name: str = Field(max_length=300)
    storage_path: str = Field(max_length=1000)
    checksum: Optional[str] = Field(
        default=None, max_length=64
    )  # Какая максимальная величина тут должна быть?

    case_id: Optional[int] = Field(default=None, foreign_key='cases.id', index=True)
    # Связь Attorney_id нужна, зачем?
    attorney_id: Optional[int] = Field(
        default=None, foreign_key='attorneys.id', index=True
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Отношения
    attorney: Optional['AttorneyORM'] = Relationship(back_populates='documents')
    case: Optional['CaseORM'] = Relationship(back_populates='documents')
