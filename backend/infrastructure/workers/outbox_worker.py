"""Воркер для обработки событий из Outbox."""

import asyncio
import json
from typing import Optional
from datetime import datetime, timezone

from backend.core.logger import logger
from backend.core.db.database import database
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.infrastructure.models.outbox import OutboxEventType, OutboxStatus
from backend.application.services.verification_service import VerificationService


class OutboxWorker:
    """
    Воркер для обработки событий из Outbox.
    
    Читает события со статусом PENDING, обрабатывает их и обновляет статусы.
    Работает в бесконечном цикле с интервалом между проверками.
    """
    
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        batch_size: int = 10,
        poll_interval: float = 5.0,
        max_retries: int = 3,
    ):
        """
        Args:
            uow_factory: Фабрика для создания UnitOfWork
            batch_size: Количество событий для обработки за раз
            poll_interval: Интервал между проверками (в секундах)
            max_retries: Максимальное количество попыток обработки
        """
        self.uow_factory = uow_factory
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self._running = False
    
    async def start(self) -> None:
        """Запустить воркер."""
        self._running = True
        logger.info('[OUTBOX WORKER] Воркер запущен')
        
        while self._running:
            try:
                await self._process_batch()
            except Exception as e:
                logger.error(f'[OUTBOX WORKER] Критическая ошибка: {e}', exc_info=True)
            
            await asyncio.sleep(self.poll_interval)
    
    async def stop(self) -> None:
        """Остановить воркер."""
        self._running = False
        logger.info('[OUTBOX WORKER] Воркер остановлен')
    
    async def _process_batch(self) -> None:
        """Обработать батч событий."""
        async with self.uow_factory.create() as uow:
            # Получаем события для обработки
            events = await uow.outbox_repo.get_pending_events(limit=self.batch_size)
            
            if not events:
                return
            
            logger.info(f'[OUTBOX WORKER] Найдено {len(events)} событий для обработки')
            
            for event in events:
                try:
                    await self._process_event(uow, event)
                except Exception as e:
                    logger.error(
                        f'[OUTBOX WORKER] Ошибка при обработке события {event.id}: {e}',
                        exc_info=True
                    )
    
    async def _process_event(self, uow, event) -> None:
        """Обработать одно событие."""
        # Помечаем как обрабатываемое
        await uow.outbox_repo.mark_as_processing(event.id)
        await uow.commit()
        
        try:
            # Обрабатываем событие в зависимости от типа
            if event.event_type == OutboxEventType.ATTORNEY_REGISTERED.value:
                await self._handle_attorney_registered(event)
            else:
                logger.warning(
                    f'[OUTBOX WORKER] Неизвестный тип события: {event.event_type}'
                )
                await uow.outbox_repo.mark_as_failed(
                    event.id,
                    f'Неизвестный тип события: {event.event_type}'
                )
                await uow.commit()
                return
            
            # Помечаем как успешно обработанное
            await uow.outbox_repo.mark_as_completed(event.id)
            await uow.commit()
            
            logger.info(f'[OUTBOX WORKER] Событие {event.id} успешно обработано')
        
        except Exception as e:
            error_msg = str(e)
            logger.error(
                f'[OUTBOX WORKER] Ошибка обработки события {event.id}: {error_msg}'
            )
            
            # Увеличиваем счетчик попыток
            retry_count = await uow.outbox_repo.increment_retry_count(event.id)
            
            if retry_count >= self.max_retries:
                # Превышен лимит попыток - помечаем как failed
                await uow.outbox_repo.mark_as_failed(
                    event.id,
                    f'Превышен лимит попыток ({self.max_retries}): {error_msg}'
                )
                logger.warning(
                    f'[OUTBOX WORKER] Событие {event.id} помечено как FAILED '
                    f'после {retry_count} попыток'
                )
            else:
                # Возвращаем в PENDING для повторной попытки
                logger.info(
                    f'[OUTBOX WORKER] Событие {event.id} будет повторно обработано '
                    f'(попытка {retry_count}/{self.max_retries})'
                )
            
            await uow.commit()
    
    async def _handle_attorney_registered(self, event) -> None:
        """Обработать событие регистрации адвоката."""
        try:
            payload = json.loads(event.payload)
            email = payload['email']
            first_name = payload['first_name']
            
            logger.info(
                f'[OUTBOX WORKER] Отправка кода верификации для {email}'
            )
            
            # Отправляем код верификации
            await VerificationService.send_verification_code(
                email=email,
                first_name=first_name,
            )
            
            logger.info(
                f'[OUTBOX WORKER] Код верификации отправлен для {email}'
            )
        
        except KeyError as e:
            raise ValueError(f'Отсутствует обязательное поле в payload: {e}')
        except Exception as e:
            raise Exception(f'Ошибка при отправке email: {e}')


async def run_outbox_worker() -> None:
    """Запустить Outbox воркер (для использования в отдельном процессе)."""
    uow_factory = UnitOfWorkFactory(database)
    worker = OutboxWorker(uow_factory)
    
    try:
        await worker.start()
    except KeyboardInterrupt:
        logger.info('[OUTBOX WORKER] Получен сигнал остановки')
    finally:
        await worker.stop()

