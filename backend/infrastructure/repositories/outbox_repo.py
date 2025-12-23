"""Репозиторий для работы с Outbox."""

import json
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from backend.core.logger import logger
from backend.core.exceptions import DatabaseErrorException
from backend.infrastructure.models.outbox import (
    OutboxORM,
    OutboxStatus,
    OutboxEventType,
)
from backend.application.interfaces.repositories.outbox_repo import IOutboxRepository
from datetime import datetime, timezone


class OutboxRepository(IOutboxRepository):
    """Репозиторий для работы с Outbox таблицей."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_event(self, event_type: str, payload: dict) -> None:
        """Сохранить событие в Outbox."""
        try:
            outbox_event = OutboxORM(
                event_type=event_type,
                payload=json.dumps(payload, ensure_ascii=False),
                status=OutboxStatus.PENDING.value,
                retry_count=0,
            )

            self.session.add(outbox_event)
            await self.session.flush()

            logger.info(
                f'[OUTBOX] Событие сохранено: type={event_type}, id={outbox_event.id}'
            )

        except SQLAlchemyError as e:
            logger.error(f'[OUTBOX] Ошибка при сохранении события: {e}')
            raise DatabaseErrorException(f'Ошибка при сохранении события в Outbox: {e}')

    async def get_pending_events(self, limit: int = 10) -> Sequence[OutboxORM]:
        """Получить события, ожидающие обработки."""
        try:
            stmt = (
                select(OutboxORM)
                .where(OutboxORM.status == OutboxStatus.PENDING.value)
                .order_by(OutboxORM.created_at.asc())
                .limit(limit)
            )

            result = await self.session.execute(stmt)
            events = result.scalars().all()

            logger.debug(f'[OUTBOX] Найдено {len(events)} событий для обработки')
            return events

        except SQLAlchemyError as e:
            logger.error(f'[OUTBOX] Ошибка при получении событий: {e}')
            raise DatabaseErrorException(f'Ошибка при получении событий из Outbox: {e}')

    async def mark_as_processing(self, event_id: int) -> None:
        """Пометить событие как обрабатываемое."""
        try:
            stmt = (
                update(OutboxORM)
                .where(OutboxORM.id == event_id)
                .values(status=OutboxStatus.PROCESSING.value)
            )
            await self.session.execute(stmt)
            await self.session.flush()

            logger.debug(f'[OUTBOX] Событие {event_id} помечено как PROCESSING')

        except SQLAlchemyError as e:
            logger.error(f'[OUTBOX] Ошибка при обновлении статуса: {e}')
            raise DatabaseErrorException(f'Ошибка при обновлении статуса события: {e}')

    async def mark_as_completed(self, event_id: int) -> None:
        """Пометить событие как успешно обработанное."""
        try:
            stmt = (
                update(OutboxORM)
                .where(OutboxORM.id == event_id)
                .values(
                    status=OutboxStatus.COMPLETED.value,
                    processed_at=datetime.now(timezone.utc),
                )
            )
            await self.session.execute(stmt)
            await self.session.flush()

            logger.info(f'[OUTBOX] Событие {event_id} успешно обработано')

        except SQLAlchemyError as e:
            logger.error(f'[OUTBOX] Ошибка при пометке как completed: {e}')
            raise DatabaseErrorException(
                f'Ошибка при пометке события как completed: {e}'
            )

    async def mark_as_failed(self, event_id: int, error_message: str) -> None:
        """Пометить событие как неудачное."""
        try:
            stmt = (
                update(OutboxORM)
                .where(OutboxORM.id == event_id)
                .values(
                    status=OutboxStatus.FAILED.value,
                    error_message=error_message[:1000],  # Ограничение длины
                )
            )
            await self.session.execute(stmt)
            await self.session.flush()

            logger.warning(
                f'[OUTBOX] Событие {event_id} помечено как FAILED: {error_message}'
            )

        except SQLAlchemyError as e:
            logger.error(f'[OUTBOX] Ошибка при пометке как failed: {e}')
            raise DatabaseErrorException(f'Ошибка при пометке события как failed: {e}')

    async def increment_retry_count(self, event_id: int) -> int:
        """Увеличить счетчик попыток обработки."""
        try:
            # Получаем текущее значение
            stmt = select(OutboxORM).where(OutboxORM.id == event_id)
            result = await self.session.execute(stmt)
            event = result.scalar_one_or_none()

            if not event:
                raise DatabaseErrorException(f'Событие {event_id} не найдено')

            new_count = event.retry_count + 1

            # Обновляем счетчик и сбрасываем статус на PENDING для повторной попытки
            update_stmt = (
                update(OutboxORM)
                .where(OutboxORM.id == event_id)
                .values(
                    retry_count=new_count,
                    status=OutboxStatus.PENDING.value,
                    error_message=None,
                )
            )
            await self.session.execute(update_stmt)
            await self.session.flush()

            logger.debug(
                f'[OUTBOX] Счетчик попыток для события {event_id}: {new_count}'
            )
            return new_count

        except SQLAlchemyError as e:
            logger.error(f'[OUTBOX] Ошибка при увеличении счетчика: {e}')
            raise DatabaseErrorException(f'Ошибка при увеличении счетчика попыток: {e}')
