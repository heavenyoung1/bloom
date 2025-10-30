from dataclasses import dataclass
from datetime import datetime

@dataclass
class Contact:
    id: int
    name: str
    personal_info: str #ИНН/ПАСПОРТ
    phone: str
    email: str
    case_id: str
    created_at: datetime