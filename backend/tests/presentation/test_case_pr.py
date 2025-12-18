import pytest
from httpx import AsyncClient
from backend.core.logger import logger


class TestCreateCase:
    '''Тесты создания дела'''

    @pytest.mark.asyncio
    async def test_create_case_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_client_dto,
        valid_case_dto,
    ):
        '''Успешное создание дела авторизованным адвокатом'''
        # ======== ПОДГОТОВКА ========
        # Регистрируем и логиним адвоката
        register_payload = valid_attorney_dto.model_dump()
        register_response = await http_client.post(
            '/api/v0/auth/register', json=register_payload
        )
        attorney_id = register_response.json()['id']
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
        client_id = create_response.json()['id']

        logger.info(f'[CREATE CLIENT] Status: {create_response.status_code}')
        assert create_response.status_code == 201

        data = create_response.json()
        assert data['id'] is not None
        assert data['email'] == client_payload['email']
        assert data['name'] == client_payload['name']
        assert data['type'] == client_payload['type']

        # ======== СОЗДАНИЕ ДЕЛА ========
        valid_case_dto.attorney_id = attorney_id
        valid_case_dto.client_id = client_id
        case_payload = valid_case_dto.model_dump()
        create_case_response = await http_client.post(
            '/api/v0/cases',
            json=case_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )
        data = create_case_response.json()
        logger.debug(f'Данные из ответа - DATA!! {data}')
        logger.debug(f'Данные из DTO - для сравнения!! {valid_case_dto}')
        assert data['name'] == valid_case_dto.name
        assert data['client_id'] == valid_case_dto.client_id
        assert data['attorney_id'] == valid_case_dto.attorney_id
        assert data['description'] == valid_case_dto.description


class TestFullCase:
    '''Тесты создания, получения, обновления, удаления дела!!!'''

    @pytest.mark.asyncio
    async def test_get_case_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_client_dto,
        valid_case_dto,
    ):
        '''Успешное создание дела авторизованным адвокатом'''
        # ======== ПОДГОТОВКА ========
        # Регистрируем и логиним адвоката
        register_payload = valid_attorney_dto.model_dump()
        register_response = await http_client.post(
            '/api/v0/auth/register', json=register_payload
        )
        attorney_id = register_response.json()['id']
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
        client_id = create_response.json()['id']

        logger.info(f'[CREATE CLIENT] Status: {create_response.status_code}')
        assert create_response.status_code == 201

        data = create_response.json()
        assert data['id'] is not None
        assert data['email'] == client_payload['email']
        assert data['name'] == client_payload['name']
        assert data['type'] == client_payload['type']

        # ======== СОЗДАНИЕ ДЕЛА ========
        valid_case_dto.attorney_id = attorney_id
        valid_case_dto.client_id = client_id
        case_payload = valid_case_dto.model_dump()
        create_case_response = await http_client.post(
            '/api/v0/cases',
            json=case_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert create_response.status_code == 201

        data = create_case_response.json()
        case_id = create_case_response.json()['id']
        logger.debug(f'Данные из ответа - DATA!! {data}')
        logger.debug(f'Данные из DTO - для сравнения!! {valid_case_dto}')
        assert data['name'] == valid_case_dto.name
        assert data['client_id'] == valid_case_dto.client_id
        assert data['attorney_id'] == valid_case_dto.attorney_id
        assert data['description'] == valid_case_dto.description

        # ======== ПОЛУЧЕНИЕ ДЕЛА ========
        get_response = await http_client.get(
            f'/api/v0/cases/{case_id}',
            headers={'Authorization': f'Bearer {access_token}'},
        )

        assert get_response.status_code == 200
        data = get_response.json()
        assert data['id'] == case_id
        assert data['name'] == case_payload['name']
        assert data['client_id'] == client_id

        # ======== ОБНОВЛЕНИЕ ДЕЛА ========
        update_payload = valid_case_dto.model_dump()
        update_payload['name'] = 'Обновленное имя уголовного дела для теста'
        update_payload['status'] = 'Завершено'
        update_payload['description'] = 'Обновленное описание уголовного дела для теста'

        update_case_response = await http_client.put(
            f'/api/v0/cases/{case_id}',
            json=update_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        assert update_case_response.status_code == 200
        data = update_case_response.json()
        assert data['id'] == case_id
        assert data['name'] == 'Обновленное имя уголовного дела для теста'
        assert data['status'] == 'Завершено'
        assert data['description'] == 'Обновленное описание уголовного дела для теста'

        # ======== УДАЛЕНИЕ ДЕЛА ========
        delete_case_response = await http_client.delete(
            f'/api/v0/cases/{case_id}',
            headers={'Authorization': f'Bearer {access_token}'},
        )

        assert delete_case_response.status_code == 204

        # ======== VERIFY DELETION ========
        get_response = await http_client.get(
            f'/api/v0/cases/{case_id}',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert get_response.status_code == 404
