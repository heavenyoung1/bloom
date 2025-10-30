from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.infrastructure.models import Case
    from backend.infrastructure.models import Attorney


class Document(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    file_name: str = Field(max_length=300)
    storage_path: str = Field(max_length=1000)
    checksum: Optional[str] = Field(default=None, max_length=64) # Какая максимальная величина тут должна быть?

    case_id: Optional[int] = Field(default=None, foreign_key='cases.id', index=True)
    # Связь Attorney_id нужна, зачем?
    attorney_id: Optional[int] = Field(default=None, foreign_key='attorneys.id', index=True)

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # Отношения
    case: Optional['Case'] = Relationship(back_populates='documents')
    attorney: Optional['Attorney'] = Relationship(back_populates='documents')