from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import BIT
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models.crm import Client
    from backend.infrastructure.models.matter import Document
    from backend.infrastructure.models.indentity import Attorney

class Case(SQLModel, table=True):

    id: int = Field(primary_key=True)
    client_id: int = Field(foreign_key='clients.id', index=True)
    attorney_id: int = Field(default=None, foreign_key='attorneys.id', index=True)
    name: str = Field(max_length=255)
    status: bool = Field(BIT,description='Статус делопроизводства')
    description: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.now(tz=None)) # type: ignore

    # relations
    client: Client = Relationship(back_populates='cases')
    attorney: Optional['Attorney'] = Relationship(back_populates='cases')
    documents: List['Document'] = Relationship(back_populates='case')