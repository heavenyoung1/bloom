from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Contact:
    id: int
    name: str
    personal_info: str  # ИНН/ПАСПОРТ
    phone: str
    email: str

    case_id: str
    attorney_id: int

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        name: str,
        personal_info: str,
        phone: str,
        email: str,
        case_id: str,
        attorney_id: int,
    ) -> 'Contact':
        return Contact(
            name=name,
            personal_info=personal_info,
            phone=phone,
            email=email,
            case_id=case_id,
            attorney_id=attorney_id,
        )
