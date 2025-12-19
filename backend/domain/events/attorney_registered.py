"""Доменное событие: регистрация адвоката."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AttorneyRegisteredEvent:
    """
    Доменное событие регистрации адвоката.
    Используется так же для сброса пароля!
    
    Используется для Outbox Pattern - гарантированной доставки
    уведомлений (email) после успешной регистрации.
    """
    
    attorney_id: int
    email: str
    first_name: str
    occurred_at: datetime
    
    def to_dict(self) -> dict:
        """Сериализация события в словарь для сохранения в Outbox."""
        return {
            'attorney_id': self.attorney_id,
            'email': self.email,
            'first_name': self.first_name,
            'occurred_at': self.occurred_at.isoformat(),
        }
    

