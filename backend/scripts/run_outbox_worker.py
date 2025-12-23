"""Скрипт для запуска Outbox воркера."""

import asyncio
from backend.infrastructure.workers import run_outbox_worker
from backend.core.logger import logger
from backend.core.db.database import database
from backend.infrastructure.redis.client import redis_client


async def main():
    """Главная функция с инициализацией подключений."""
    try:
        logger.info('[OUTBOX WORKER] Инициализация подключений...')

        # Подключиться к БД
        await database.connect()
        logger.info('[OUTBOX WORKER] БД подключена')

        # Подключиться к Redis
        await redis_client.connect()
        logger.info('[OUTBOX WORKER] Redis подключен')

        # Запустить воркер
        await run_outbox_worker()

    except KeyboardInterrupt:
        logger.info('[OUTBOX WORKER] Получен сигнал остановки')
    except Exception as e:
        logger.error(f'[OUTBOX WORKER] Критическая ошибка: {e}', exc_info=True)
        raise
    finally:
        # Закрыть подключения
        try:
            await redis_client.disconnect()
            logger.info('[OUTBOX WORKER] Redis отключен')
        except Exception as e:
            logger.error(f'[OUTBOX WORKER] Ошибка при отключении Redis: {e}')

        try:
            await database.dispose()
            logger.info('[OUTBOX WORKER] БД отключена')
        except Exception as e:
            logger.error(f'[OUTBOX WORKER] Ошибка при отключении БД: {e}')


if __name__ == '__main__':
    logger.info('[OUTBOX WORKER] Запуск воркера...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('[OUTBOX WORKER] Воркер остановлен пользователем')
    except Exception as e:
        logger.error(f'[OUTBOX WORKER] Критическая ошибка: {e}', exc_info=True)
        raise
