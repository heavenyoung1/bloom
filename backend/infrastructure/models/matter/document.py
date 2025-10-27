from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from backend.infrastructure.models.crm import Client
    from backend.infrastructure.models.matter import Case
    from backend.infrastructure.models.indentity import Attorney


class Document(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    file_name: str = Field(max_length=300)
    storage_path: str = Field(max_length=1000)
    checksum: Optional[str] = Field(default=None, max_length=64) # Какая максимальная величина тут должна быть?

    client_id: Optional[int] = Field(default=None, foreign_key='clients.id', index=True)
    case_id: Optional[int] = Field(default=None, foreign_key='cases.id', index=True)
    attorney_id: Optional[int] = Field(default=None, foreign_key='attorneys.id', index=True)

    created_at: datetime = Field(default_factory=datetime.now(tz=None)) # type: ignore

    # relations
    client: Optional[Client] = Relationship(back_populates='documents')
    case: Optional[Case] = Relationship(back_populates='documents')
    attorney: Optional[Attorney] = Relationship(back_populates='documents')