"""Интерфейс репозитория для Outbox Pattern."""

from abc import abstractmethod
from typing import Sequence, Any


class IOutboxRepository:
    """Интерфейс репозитория для работы с Outbox."""
    
    @abstractmethod
    async def save_event(
        self, 
        event_type: str, 
        payload: dict
    ) -> None:
        """
        Сохранить событие в Outbox.
        
        Args:
            event_type: Тип события (например, 'attorney_registered')
            payload: Данные события в виде словаря
        """
        ...
    
    @abstractmethod
    async def get_pending_events(
        self, 
        limit: int = 10
    ) -> Sequence[Any]:
        """
        Получить события, ожидающие обработки.
        
        Args:
            limit: Максимальное количество событий
            
        Returns:
            Список событий со статусом PENDING
        """
        ...
    
    @abstractmethod
    async def mark_as_processing(
        self, 
        event_id: int
    ) -> None:
        """Пометить событие как обрабатываемое."""
        ...
    
    @abstractmethod
    async def mark_as_completed(
        self, 
        event_id: int
    ) -> None:
        """Пометить событие как успешно обработанное."""
        ...
    
    @abstractmethod
    async def mark_as_failed(
        self, 
        event_id: int, 
        error_message: str
    ) -> None:
        """
        Пометить событие как неудачное.
        
        Args:
            event_id: ID события
            error_message: Сообщение об ошибке
        """
        ...
    
    @abstractmethod
    async def increment_retry_count(
        self, 
        event_id: int
    ) -> int:
        """
        Увеличить счетчик попыток обработки.
        
        Returns:
            Новое значение счетчика
        """
        ...

