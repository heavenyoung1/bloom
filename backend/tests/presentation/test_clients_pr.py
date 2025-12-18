import pytest
from httpx import AsyncClient
from backend.core.logger import logger


class TestCreateClient:
    '''Тесты создания клиента'''

    @pytest.mark.asyncio
    async def test_create_client_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_client_dto,
    ):
        '''Успешное создание клиента авторизованным адвокатом'''
        # ======== ПОДГОТОВКА ========
        # Регистрируем и логиним адвоката
        register_payload = valid_attorney_dto.model_dump()
        await http_client.post('/api/v0/auth/register', json=register_payload)

        from backend.infrastructure.redis.client import redis_client
        from backend.infrastructure.redis.keys import RedisKeys

        email = register_payload['email']
        code = await redis_client._client.get(RedisKeys.email_verification_code(email))

        await http_client.post(
            '/api/v0/auth/verify-email',
            json={'email': email, 'code': code},
        )

        login_response = await http_client.post(
            '/api/v0/auth/login',
            json={'email': email, 'password': register_payload['password']},
        )

        access_token = login_response.json()['access_token']

        # ======== СОЗДАНИЕ КЛИЕНТА ========
        client_payload = valid_client_dto.model_dump()
        create_response = await http_client.post(
            '/api/v0/clients',
            json=client_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        logger.info(f'[CREATE CLIENT] Status: {create_response.status_code}')
        assert create_response.status_code == 201

        data = create_response.json()
        assert data['id'] is not None
        assert data['email'] == client_payload['email']
        assert data['name'] == client_payload['name']
        assert data['type'] == client_payload['type']

    @pytest.mark.asyncio
    async def test_create_client_without_auth(
        self,
        http_client: AsyncClient,
        valid_client_dto,
    ):
        '''Создание клиента без авторизации должно вернуть 401'''
        client_payload = valid_client_dto.model_dump()
        create_response = await http_client.post(
            '/api/v0/clients',
            json=client_payload,
        )

        assert create_response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_client_invalid_email(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_client_dto,
    ):
        '''Создание клиента с невалидным email'''
        # ======== SETUP ATTORNEY ========
        register_payload = valid_attorney_dto.model_dump()
        await http_client.post('/api/v0/auth/register', json=register_payload)

        from backend.infrastructure.redis.client import redis_client
        from backend.infrastructure.redis.keys import RedisKeys

        email = register_payload['email']
        code = await redis_client._client.get(RedisKeys.email_verification_code(email))

        await http_client.post(
            '/api/v0/auth/verify-email',
            json={'email': email, 'code': code},
        )

        login_response = await http_client.post(
            '/api/v0/auth/login',
            json={'email': email, 'password': register_payload['password']},
        )

        access_token = login_response.json()['access_token']

        # ======== INVALID CLIENT EMAIL ========
        client_payload = valid_client_dto.model_dump()
        client_payload['email'] = 'invalid-email'

        create_response = await http_client.post(
            '/api/v0/clients',
            json=client_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        assert create_response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_client_duplicate_email(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_client_dto,
    ):
        '''Создание клиента с duplicate email'''
        # ======== SETUP ATTORNEY ========
        register_payload = valid_attorney_dto.model_dump()
        await http_client.post('/api/v0/auth/register', json=register_payload)

        from backend.infrastructure.redis.client import redis_client
        from backend.infrastructure.redis.keys import RedisKeys

        email = register_payload['email']
        code = await redis_client._client.get(RedisKeys.email_verification_code(email))

        await http_client.post(
            '/api/v0/auth/verify-email',
            json={'email': email, 'code': code},
        )

        login_response = await http_client.post(
            '/api/v0/auth/login',
            json={'email': email, 'password': register_payload['password']},
        )

        access_token = login_response.json()['access_token']

        # ======== CREATE FIRST CLIENT ========
        client_payload = valid_client_dto.model_dump()
        create_response = await http_client.post(
            '/api/v0/clients',
            json=client_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        assert create_response.status_code == 201

        # ======== CREATE DUPLICATE ========
        create_duplicate = await http_client.post(
            '/api/v0/clients',
            json=client_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        assert create_duplicate.status_code == 400
