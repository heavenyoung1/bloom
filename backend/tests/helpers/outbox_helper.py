"""Утилиты для работы с Outbox в тестах."""

import json
from typing import Optional
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.infrastructure.models.outbox import OutboxEventType
from backend.application.services.verification_service import VerificationService


async def process_outbox_events(uow_factory: Optional[UnitOfWorkFactory] = None):
    """
    Обработать все pending события из Outbox синхронно.
    
    Используется в тестах для имитации работы воркера.
    
    Args:
        uow_factory: Фабрика UnitOfWork (если None, будет использована из database)
    """
    # Если фабрика не передана, используем из database (для интеграционных тестов)
    if uow_factory is None:
        from backend.core.db.database import database
        uow_factory = UnitOfWorkFactory(database)
    
    async with uow_factory.create() as uow:
        # Получаем все pending события
        events = await uow.outbox_repo.get_pending_events(limit=100)
        
        if not events:
            return
        
        for event in events:
            try:
                # Помечаем как обрабатываемое
                await uow.outbox_repo.mark_as_processing(event.id)
                await uow.commit()
                
                # Обрабатываем событие
                if event.event_type == OutboxEventType.ATTORNEY_REGISTERED.value:
                    payload = json.loads(event.payload)
                    email = payload['email']
                    first_name = payload['first_name']
                    
                    # Отправляем код верификации
                    await VerificationService.send_verification_code(
                        email=email,
                        first_name=first_name,
                    )
                
                # Помечаем как успешно обработанное
                await uow.outbox_repo.mark_as_completed(event.id)
                await uow.commit()
            
            except Exception as e:
                # В тестах просто логируем ошибку
                await uow.outbox_repo.mark_as_failed(event.id, str(e))
                await uow.commit()
                raise

