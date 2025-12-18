import pytest
from httpx import AsyncClient, ASGITransport

from backend.main import app
from backend.core.dependencies import get_uow_factory, get_current_attorney_id


@pytest.fixture
async def http_client():
    '''
    Асинхронная pytest-фикстура, предоставляющая HTTP-клиент для тестирования ASGI-приложения.

    Использует httpx.AsyncClient с ASGITransport, чтобы выполнять запросы напрямую к приложению
    (без запуска реального HTTP-сервера, например, uvicorn). Это обеспечивает быстрые,
    надёжные и изолированные интеграционные тесты эндпоинтов FastAPI/Starlette.

    Преимущества перед starlette.testclient.TestClient:
        - Более богатый функционал httpx (таймауты, retry, следование редиректам и т.д.).
        - Полная совместимость API с реальными HTTP-запросами.
        - Отличная поддержка асинхронности.

    Пример использования в тесте:
        async def test_root_endpoint(http_client: AsyncClient):
            response = await http_client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}

    Возвращает:
        httpx.AsyncClient — настроенный асинхронный клиент, готовый к отправке запросов.

    Notes:
        - base_url='http://test' — произвольная заглушка, позволяет использовать относительные пути
          в тестах (например, client.get("/users/")).
        - Клиент автоматически закрывается после завершения теста благодаря async with.
        - Требует, чтобы тестируемое приложение (app) было ASGI-совместимым
          (FastAPI, Starlette, Quart и т.д.).
    '''
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as async_client:
        yield async_client


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
