from dataclasses import dataclass
from datetime import datetime

@dataclass
class Client:
    id: int
    name: str
    type: bool
    email: str
    phone: str
    personal_info: str #ИНН/ПАСПОРТ
    address: str
    messenger_type: str
    messenger_handle: str
    owner_attorney_id: str
    created_at: datetime