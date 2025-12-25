from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class CreateContactCommand:
    name: str
    personal_info: str
    phone: str
    email: str
    attorney_id: int
    case_id: int


@dataclass
class UpdateContactCommand:
    contact_id: int
    # attorney_id и case_id удалены - нельзя менять владельца и дело

    # PATCH — все поля опциональные
    name: Optional[str] = None
    personal_info: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


@dataclass
class DeleteContactCommand:
    contact_id: int


@dataclass
class GetContactByIdQuery:
    contact_id: int


@dataclass
class GetContactsForAttorneyQuery:
    attorney_id: int
