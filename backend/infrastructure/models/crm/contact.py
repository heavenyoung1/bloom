from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:

    from backend.infrastructure.models.crm import Client

class Contact(SQLModel, table=True):

    id: int = Field(primary_key=True)
    name: str = Field(max_length=255, description='ФИО полностью')
    personal_info: Optional[str] = Field(default=None, description='Паспорт', max_length=12)
    phone: Optional[str] = Field(default=None, max_length=12)
    email: Optional[str] = Field(default=None, max_length=50)
    client_id: int = Field(foreign_key='clients.id', index=True)
    created_at: datetime = Field(default_factory=datetime.now(tz=None)) # type: ignore

    # relations
    client: Client = Relationship(back_populates='contacts')