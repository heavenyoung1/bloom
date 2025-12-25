import pytest
from httpx import AsyncClient, ASGITransport

from backend.main import app
from backend.core.dependencies import get_uow_factory, get_current_attorney_id
from backend.core.logger import logger

@pytest.fixture
async def http_client(session, test_uow_factory):
    '''
    HTTP клиент для тестов с переопределением зависимостей.
    
    ✅ Использует ТОЛЬКО тестовую БД (session фикстура)
    ✅ Переопределяет get_uow_factory на test_uow_factory
    '''
    
    # Получаем get_uow_factory из app
    from backend.core.dependencies import get_uow_factory
    
    # Переопределяем зависимость
    app.dependency_overrides[get_uow_factory] = lambda: test_uow_factory
    
    logger.info('[HTTP CLIENT] Переопределена зависимость get_uow_factory')
    
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as async_client:
        yield async_client
    
    # Убираем переопределение
    app.dependency_overrides.clear()
    logger.info('[HTTP CLIENT] Зависимости восстановлены')

@pytest.fixture(autouse=True)
def override_uow_factory(test_uow_factory):
    async def _override_get_uow_factory():
        return test_uow_factory

    app.dependency_overrides[get_uow_factory] = _override_get_uow_factory
    yield
    app.dependency_overrides.pop(get_uow_factory, None)


# @pytest.fixture(autouse=True)
# def override_auth():
#     async def _override_current_attorney_id():
#         return 1

#     app.dependency_overrides[get_current_attorney_id] = _override_current_attorney_id
#     yield
#     app.dependency_overrides.pop(get_current_attorney_id, None)
