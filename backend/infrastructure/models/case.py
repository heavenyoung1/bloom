from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import BIT
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.models import Event
    from backend.infrastructure.models import Client
    from backend.infrastructure.models import Contact
    from backend.infrastructure.models import Document
    from backend.infrastructure.models import Attorney


class Case(SQLModel, table=True):

    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    client_id: int = Field(foreign_key='clients.id', index=True)
    attorney_id: int = Field(default=None, foreign_key='attorneys.id', index=True)
    status: str = Field(max_length=50, description='Статус делопроизводства')
    description: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # Отношения
    client: Optional['Client'] = Relationship(back_populates='cases')
    attorney: Optional['Attorney'] = Relationship(back_populates='cases')
    contacts: List['Contact'] = Relationship(
        back_populates='case', sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
    documents: List['Document'] = Relationship(back_populates='case')
    events: List['Event'] = Relationship(back_populates='case')
