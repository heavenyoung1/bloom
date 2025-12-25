import json
from typing import Optional, Union
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.infrastructure.models.outbox import OutboxEventType
from backend.application.services.verification_service import VerificationService
from backend.tests.fixtures.uow import test_uow_factory

from backend.core.logger import logger

async def process_outbox_events(uow_factory: test_uow_factory) -> None:
    '''
    Обработать все pending события из Outbox синхронно.

    Используется в тестах для имитации работы фонового воркера.
    Получает события → обрабатывает → фиксирует результат.

    Args:
        uow_factory: Фабрика UnitOfWork (реальная или тестовая)

    Raises:
        Exception: Если обработка события завершилась с ошибкой
    '''
    async with uow_factory.create() as uow:
        # 1. Получаем все PENDING события
        events = await uow.outbox_repo.get_pending_events(limit=100)

        if not events:
            logger.debug('[OUTBOX HELPER] Нет событий для обработки')
            return

        logger.info(f'[OUTBOX HELPER] Найдено {len(events)} событий для обработки')

        # 2. Обрабатываем каждое событие
        for event in events:
            try:
                logger.info(f'[OUTBOX HELPER] Обрабатываем событие: ID={event.id}, type={event.event_type}')
                
                # Помечаем как обрабатываемое
                await uow.outbox_repo.mark_as_processing(event.id)
                await uow.commit()

                # Обрабатываем в зависимости от типа события
                if event.event_type == OutboxEventType.ATTORNEY_REGISTERED.value:
                    await _handle_attorney_registered(event)

                # ℹ️ Добавь обработчики для других типов событий здесь:
                # elif event.event_type == OutboxEventType.SOME_OTHER_EVENT.value:
                #     await _handle_some_other_event(event)

                # Помечаем как успешно обработанное
                await uow.outbox_repo.mark_as_completed(event.id)
                await uow.commit()
                
                logger.info(f'[OUTBOX HELPER] Событие обработано успешно: ID={event.id}')

            except Exception as e:
                logger.error(f'[OUTBOX HELPER] Ошибка при обработке события ID={event.id}: {e}')
                # Помечаем как ошибку
                await uow.outbox_repo.mark_as_failed(event.id, str(e))
                await uow.commit()
                # Пробрасываем ошибку дальше (для осведомленности в тестах)
                raise


async def _handle_attorney_registered(event) -> None:
    '''
    Обработчик события AttorneyRegisteredEvent.

    Отправляет код верификации на email адвоката.

    Args:
        event: Событие из Outbox
    '''
    try:
        # Парсим payload
        payload = json.loads(event.payload)
        email = payload['email']
        first_name = payload['first_name']

        logger.info(f'[OUTBOX HANDLER] Отправляем код верификации: {email}')

        # Отправляем код верификации
        # (в реальности это отправит письмо, в тестах положит код в Redis)
        try:
            success = await VerificationService.send_verification_code(
                email=email,
                first_name=first_name,
            )

            if not success:
                logger.warning(
                    f'[OUTBOX HANDLER] Ошибка отправки кода верификации для {email}, '
                    f'но код сохранен в Redis'
                )
                # Код уже в Redis, письмо отправится позже (retry)
                return

            logger.info(f'[OUTBOX HANDLER] Код верификации отправлен: {email}')
            
        except Exception as e:
            # Если отправка письма упала, но код уже в Redis - это OK
            # Письмо отправится позже (в реальной системе через retry mechanism)
            logger.warning(
                f'[OUTBOX HANDLER] Ошибка отправки письма для {email}: {e}, '
                f'но код верификации сохранен в Redis'
            )
            # Не пробрасываем - код все равно доступен для верификации
            return

    except json.JSONDecodeError as e:
        logger.error(f'[OUTBOX HANDLER] Ошибка парсинга payload: {e}')
        raise
    except Exception as e:
        logger.error(f'[OUTBOX HANDLER] Ошибка обработки события: {e}')
        raise
