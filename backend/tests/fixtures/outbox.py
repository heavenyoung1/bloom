'''Фикстуры для работы с Outbox в тестах.'''

import pytest
from backend.tests.helpers.outbox_helper import process_outbox_events
from backend.core.logger import logger


@pytest.fixture
def auto_process_outbox(test_uow_factory):
    '''
    Фикстура для обработки Outbox событий в тестах.

    Возвращает асинхронную функцию для обработки PENDING событий из Outbox,
    имитируя работу фонового воркера.

    Использование:
        async def test_something(http_client, auto_process_outbox, valid_attorney_dto):
            # 1. Регистрация (создает событие в Outbox)
            await http_client.post('/api/v0/auth/register', json=valid_attorney_dto.model_dump())

            # 2. Обработаем Outbox события (имитируем воркер)
            await auto_process_outbox()

            # 3. Теперь код верификации в Redis, письмо 'отправлено'
            response = await http_client.post('/api/v0/auth/verify-email', json={...})
    '''

    async def _process():
        '''Обработать все PENDING события из Outbox.'''
        logger.info('[TEST] Начинаем обработку Outbox')
        
        # Используем тестовую фабрику UoW
        await process_outbox_events(test_uow_factory)
        
        logger.info('[TEST] Обработка Outbox завершена')

    return _process
