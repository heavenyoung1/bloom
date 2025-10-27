from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:

    from backend.infrastructure.models.crm import Contact
    from backend.infrastructure.models.matter import Case, Document
    from backend.infrastructure.models.indentity import Attorney

class Client(SQLModel, table=True):

    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    type: bool = Field(description='True: Физ.лицо / False: Юр.лицо')
    email: Optional[str] = Field(max_length=255, index=True)
    phone: str = Field(max_length=50)
    personal_info: str = Field(default=None, description='ИНН для компании / Серия-Номер паспорта для человека', max_length=12)
    address: Optional[str] = Field(default=None, max_length=500)
    messenger_type: bool = Field(description='True: Telegram / False: WhatsApp')
    messenger_handle: Optional[str] = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.now(tz=None)) # type: ignore

    owner_attorney_id: Optional[int] = Field(
        default=None, foreign_key='attorneys.id', index=True
    )

    # relations
    owner_attorney: Optional[Attorney] = Relationship(back_populates='clients')
    contacts: List['Contact'] = Relationship(back_populates='client', sa_relationship_kwargs={'cascade': 'all, delete-orphan'})
    cases: List['Case'] = Relationship(back_populates='client')
    documents: List['Document'] = Relationship(back_populates='client')