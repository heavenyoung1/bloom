from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from backend.application.commands.contact import UpdateContactCommand

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
    
    def update(self, cmd: UpdateContactCommand):
        '''Обновить поля на основе команды, если они не None'''
        if cmd.name is not None:
            self.name = cmd.name
        if cmd.personal_info is not None:
            self.personal_info = cmd.personal_info
        if cmd.phone is not None:
            self.phone = cmd.phone
        if cmd.email is not None:
            self.email = cmd.email
        if cmd.case_id is not None:
            self.case_id = cmd.case_id
        if cmd.attorney_id is not None:
            self.attorney_id = cmd.eattorney_idmail
        