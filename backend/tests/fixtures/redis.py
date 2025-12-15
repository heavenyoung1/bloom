import pytest


class FakeRedisBackend:
    '''Минимальный async-заменитель для redis.asyncio.Redis (только то, что нужно твоему RedisClient).'''
    def __init__(self):
        self.store = {}

    async def setex(self, key, ttl, value):
        # ttl игнорируем (для тестов ок)
        self.store[key] = value
        return True

    async def get(self, key):
        return self.store.get(key)

    async def delete(self, key):
        return 1 if self.store.pop(key, None) is not None else 0

    async def incrby(self, key, amount):
        cur = int(self.store.get(key, 0))
        cur += amount
        self.store[key] = str(cur)
        return cur

    async def exists(self, key):
        return 1 if key in self.store else 0

    async def expire(self, key, ttl):
        # Для тестов просто проверяем, что ключ существует
        # В реальном Redis устанавливает TTL на существующий ключ
        return 1 if key in self.store else 0

    async def close(self):
        return None


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    '''
    Делает redis_client 'подключенным' в тестах, без реального Redis.
    '''
    from backend.infrastructure.redis.client import redis_client

    redis_client._client = FakeRedisBackend()
    yield
    redis_client._client = None