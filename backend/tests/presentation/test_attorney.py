import pytest
from httpx import AsyncClient

from backend.application.dto.attorney import (
    VerifyEmailRequest,
)
from backend.core.logger import logger


class TestRegisterAttorney:
    '''Тесты регистрации адвоката'''

    async def test_register_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
    ):
        '''Успешная регистрация адвоката'''
        register_payload = valid_attorney_dto.model_dump()
        register_response = await http_client.post(
            '/api/v1/auth/register',
            json=register_payload,
        )
        # Ожидаем успех или ошибку валидации/дублирования
        assert register_response.status_code in [201, 400]

        data = register_response.json()
        assert data['id'] is not None
        assert data['email'] == register_payload['email']


# ========== LOGIN TESTS ==========


class TestLoginAttorney:
    '''Тесты входа адвоката'''

    async def test_login_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_login_attorney_dto,
    ):
        '''Успешный вход в систему'''
        # ======== РЕГИСТРАЦИЯ ========
        register_payload = valid_attorney_dto.model_dump()
        register_response = await http_client.post(
            '/api/v1/auth/register',
            json=register_payload,
        )
        assert register_response.status_code in [201, 400]

        data = register_response.json()
        assert data['id'] is not None
        assert data['email'] == register_payload['email']

        # ======== ВЕРИФИКАЦИЯ EMAIL ========
        from backend.infrastructure.redis.client import redis_client
        from backend.infrastructure.redis.keys import RedisKeys

        email = register_payload['email']

        # Используем правильный ключ из RedisKeys
        verification_key = RedisKeys.email_verification_code(email)
        verification_code = await redis_client._client.get(verification_key)

        logger.debug(f'[VERIFICATION] Key: {verification_key}')
        logger.debug(f'[VERIFICATION CODE] {verification_code}')
        logger.debug(f'[REDIS STORE] {redis_client._client.store}')

        assert verification_code is not None, f'Код верификации не найден для {email}'

        verify_response = await http_client.post(
            '/api/v1/auth/verify-email',
            json={
                'email': email,
                'code': verification_code,
            },
        )
        logger.debug(f'[VERIFY RESPONSE] Status: {verify_response.status_code}')
        assert (
            verify_response.status_code == 200
        ), f'Ошибка верификации: {verify_response.json()}'

        # ======== АВТОРИЗАЦИЯ ========
        login_payload = valid_login_attorney_dto.model_dump()
        login_response = await http_client.post(
            '/api/v1/auth/login',
            json=login_payload,
        )

        logger.debug(f'[LOGIN RESPONSE] Status: {login_response.status_code}')
        assert (
            login_response.status_code == 200
        ), f'Ошибка входа: {login_response.json()}'

        login_data = login_response.json()
        assert 'access_token' in login_data
        assert 'refresh_token' in login_data
        assert 'token_type' in login_data
        assert login_data['token_type'] == 'bearer'

    async def test_resend_verification(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
    ):
        # ===== REGISTER =====
        payload = valid_attorney_dto.model_dump()
        await http_client.post('/api/v1/auth/register', json=payload)

        from backend.infrastructure.redis.client import redis_client
        from backend.infrastructure.redis.keys import RedisKeys

        email = payload['email']
        key = RedisKeys.email_verification_code(email)

        old_code = await redis_client._client.get(key)
        assert old_code is not None

        # ===== RESEND =====
        resend_response = await http_client.post(
            '/api/v1/auth/resend-verification',
            json={'email': email},
        )

        assert resend_response.status_code == 200

        new_code = await redis_client._client.get(key)
        assert new_code is not None
        assert new_code != old_code

    async def test_logout(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
    ):
        # ===== REGISTER → VERIFY → LOGIN =====
        payload = valid_attorney_dto.model_dump()
        await http_client.post('/api/v1/auth/register', json=payload)

        from backend.infrastructure.redis.client import redis_client
        from backend.infrastructure.redis.keys import RedisKeys

        email = payload["email"]
        code = await redis_client._client.get(RedisKeys.email_verification_code(email))

        await http_client.post(
            '/api/v1/auth/verify-email',
            json={'email': email, 'code': code},
        )

        login_response = await http_client.post(
            '/api/v1/auth/login',
            json={'email': email, 'password': payload['password']},
        )

        tokens = login_response.json()
        access_token = tokens['access_token']

        # ===== LOGOUT =====
        logout_response = await http_client.post(
            '/api/v1/auth/logout',
            headers={'Authorization': f'Bearer {access_token}'},
        )

        assert logout_response.status_code == 200

class TestResendVerification:
    async def test_resend_verification_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
    ):
        # ======== РЕГИСТРАЦИЯ (email ещё НЕ верифицирован) ========
        from backend.infrastructure.redis.keys import RedisKeys
        from backend.infrastructure.redis.client import redis_client
        register_payload = valid_attorney_dto.model_dump()
        r = await http_client.post("/api/v1/auth/register", json=register_payload)
        assert r.status_code == 201, r.text

        email = register_payload["email"]
        key = RedisKeys.email_verification_code(email)

        old_code = await redis_client._client.get(key)
        assert old_code is not None, f"Старый код не найден в Redis для {email}"

        # ======== RESEND ========
        resend_response = await http_client.post(
            "/api/v1/auth/resend-verification",
            json={"email": email},
        )
        assert resend_response.status_code == 200, resend_response.text

        new_code = await redis_client._client.get(key)
        assert new_code is not None, f"Новый код не найден в Redis для {email}"
        assert new_code != old_code, "Код не изменился после resend-verification"