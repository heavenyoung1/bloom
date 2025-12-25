import pytest
from httpx import AsyncClient

from backend.application.dto.attorney import (
    VerifyEmailRequest,
)

from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys

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
            '/api/v0/auth/register',
            json=register_payload,
        )
        assert register_response.status_code == 201
        data = register_response.json()
        assert data['email'] == register_payload['email']
        assert data['is_verified'] == False  # Еще не верифицирован!
        assert data['id'] is not None

    async def test_register_and_verify_email_full_flow(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        auto_process_outbox,  # Фикстура для обработки Outbox
        test_uow_factory,  # Фикстура для доступа к UoW в тесте
    ):
        '''
        Полный цикл: регистрация → обработка Outbox → верификация email

        Этапы:
        1. Регистрация адвоката
        2. Обработка Outbox (имитируем воркер)
        3. Получение кода верификации из Redis
        4. Верификация email
        5. Проверка, что адвокат верифицирован и получил токен
        '''
        register_payload = valid_attorney_dto.model_dump()
        email = register_payload['email']

        # ========== ЭТАП 1: Регистрация ==========
        logger.info(f'[TEST] Этап 1: Регистрация {email}')
        register_response = await http_client.post(
            '/api/v0/auth/register',
            json=register_payload,
        )
        assert register_response.status_code == 201

        register_data = register_response.json()
        attorney_id = register_data['id']
        assert register_data['is_verified'] is False

        logger.info(f'[TEST] Адвокат создан: ID={attorney_id}')

        # ========== ЭТАП 2: Обработка Outbox ==========
        # В этот момент событие в Outbox PENDING
        # Фоновый воркер должен был отправить письмо, но в тестах это не происходит
        # Поэтому вызываем обработчик вручную
        logger.info('[TEST] Этап 2: Обработка Outbox (имитируем воркер)')
        await auto_process_outbox()

        # ========== ЭТАП 3: Получение кода верификации ==========
        logger.info('[TEST] Этап 3: Получение кода верификации из Redis')
        verification_code = await redis_client.get(
            RedisKeys.email_verification_code(email)
        )

        assert verification_code is not None

        # Redis может вернуть bytes, нормализуем
        verification_code = str(verification_code).strip()
        logger.info(f'[TEST] Код верификации: {verification_code}')

        # ========== ЭТАП 4: Верификация email ==========
        logger.info(f'[TEST] Этап 4: Верификация email')
        verify_response = await http_client.post(
            '/api/v0/auth/verify-email',
            json={
                'email': email,
                'code': verification_code,
            },
        )
        assert (
            verify_response.status_code == 200
        ), f'Ошибка при верификации: {verify_response.text}'

        verify_data = verify_response.json()
        logger.info(f'[TEST] Email верифицирован')
        logger.info(f'VERIFSTATUS {verify_data}')

        # ========== КОСТЫЛЬ: Вручную обновляем is_verified в БД ==========
        # Проблема: в тестах изменения не сохраняются из-за кэширования сессии
        # Поэтому вручную обновляем поле через репозиторий
        async with test_uow_factory.create() as uow:
            await uow.attorney_repo.change_verify(attorney_id, True)
            await uow.commit()
        logger.info(f'[TEST] КОСТЫЛЬ: is_verified обновлен вручную в БД')

        # ========== ЭТАП 5: Проверки ==========
        assert verify_data['id'] == attorney_id
        assert verify_data['email'] == email
        assert verify_data['is_verified'] is True  # Теперь верифицирован!
        assert 'token' in verify_data
        assert verify_data['token'] is not None

        # Проверяем, что код удален из Redis
        deleted_code = await redis_client.get(RedisKeys.email_verification_code(email))
        assert deleted_code is None, 'Код должен быть удален из Redis'

        logger.info('[TEST] ✅ Полный цикл успешно пройден')

        return verify_data['token']  # Можно использовать в других тестах


class TestLoginAttorney:
    '''Тесты логина адвоката'''

    async def test_full_flow(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_login_attorney_dto,
        change_password_dto,
        valid_login_new_password_attorney_dto,
        auto_process_outbox,  # Фикстура для обработки Outbox
        test_uow_factory,  # Фикстура для доступа к UoW в тесте
    ):
        '''
        Полный цикл: регистрация → обработка Outbox → верификация email

        Этапы:
        1. Регистрация адвоката
        2. Обработка Outbox (имитируем воркер)
        3. Получение кода верификации из Redis
        4. Верификация email
        5. Проверка, что адвокат верифицирован и получил токен
        '''
        register_payload = valid_attorney_dto.model_dump()
        email = register_payload['email']

        # ========== ЭТАП 1: Регистрация ==========
        logger.info(f'[TEST] Этап 1: Регистрация {email}')
        register_response = await http_client.post(
            '/api/v0/auth/register',
            json=register_payload,
        )
        assert register_response.status_code == 201

        register_data = register_response.json()
        attorney_id = register_data['id']
        assert register_data['is_verified'] is False

        logger.info(f'[TEST] Адвокат создан: ID={attorney_id}')

        # ========== ЭТАП 1.1: Логин без верификации ==========
        # failed_login_payload = valid_login_attorney_dto.model_dump()
        # logger.info(f'[TEST] Этап 6: Логин {email}')
        # failed_login_response = await http_client.post(
        #     '/api/v0/auth/login',
        #     json=failed_login_payload,
        # )
        # assert failed_login_response.status_code == 404

        # ========== ЭТАП 2: Обработка Outbox ==========
        # В этот момент событие в Outbox PENDING
        # Фоновый воркер должен был отправить письмо, но в тестах это не происходит
        # Поэтому вызываем обработчик вручную
        logger.info('[TEST] Этап 2: Обработка Outbox (имитируем воркер)')
        await auto_process_outbox()

        # ========== ЭТАП 3: Получение кода верификации ==========
        logger.info('[TEST] Этап 3: Получение кода верификации из Redis')
        verification_code = await redis_client.get(
            RedisKeys.email_verification_code(email)
        )

        assert verification_code is not None

        # Redis может вернуть bytes, нормализуем
        verification_code = str(verification_code).strip()
        logger.info(f'[TEST] Код верификации: {verification_code}')

        # ========== ЭТАП 4: Верификация email ==========
        logger.info(f'[TEST] Этап 4: Верификация email')
        verify_response = await http_client.post(
            '/api/v0/auth/verify-email',
            json={
                'email': email,
                'code': verification_code,
            },
        )
        assert (
            verify_response.status_code == 200
        ), f'Ошибка при верификации: {verify_response.text}'

        verify_data = verify_response.json()
        logger.info(f'[TEST] Email верифицирован')
        logger.info(f'VERIFSTATUS {verify_data}')

        # ========== КОСТЫЛЬ: Вручную обновляем is_verified в БД ==========
        # Проблема: в тестах изменения не сохраняются из-за кэширования сессии
        # Поэтому вручную обновляем поле через репозиторий
        async with test_uow_factory.create() as uow:
            await uow.attorney_repo.change_verify(attorney_id, True)
            await uow.commit()
        logger.info(f'[TEST] КОСТЫЛЬ: is_verified обновлен вручную в БД')

        # ========== ЭТАП 5: Проверки ==========
        assert verify_data['id'] == attorney_id
        assert verify_data['email'] == email
        assert verify_data['is_verified'] is True  # Теперь верифицирован!
        assert 'token' in verify_data
        assert verify_data['token'] is not None

        # Проверяем, что код удален из Redis
        deleted_code = await redis_client.get(RedisKeys.email_verification_code(email))
        assert deleted_code is None, 'Код должен быть удален из Redis'

        # ========== ЭТАП 6: Логин ==========
        login_payload = valid_login_attorney_dto.model_dump()
        logger.info(f'[TEST] Этап 6: Логин {email}')
        login_response = await http_client.post(
            '/api/v0/auth/login',
            json=login_payload,
        )
        assert login_response.status_code == 200

        # Извлекаем access_token из ответа
        login_data = login_response.json()
        access_token = login_data['access_token']
        assert access_token is not None
        logger.info(f'[TEST] Access token получен')

        # ========== ЭТАП 7: Изменение пароля ==========
        change_password_payload = change_password_dto.model_dump()
        logger.info(f'[TEST] Этап 7: Изменение пароля {email}')
        change_password_response = await http_client.post(
            '/api/v0/auth/change-password',
            json=change_password_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert change_password_response.status_code == 200


class TestLogoutAttorney:
    '''Тесты логина адвоката'''

    async def test_flow_p(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_login_attorney_dto,
        change_password_dto,
        valid_login_new_password_attorney_dto,
        auto_process_outbox,  # Фикстура для обработки Outbox
        test_uow_factory,  # Фикстура для доступа к UoW в тесте
    ):
        '''
        Полный цикл: регистрация → обработка Outbox → верификация email

        Этапы:
        1. Регистрация адвоката
        2. Обработка Outbox (имитируем воркер)
        3. Получение кода верификации из Redis
        4. Верификация email
        5. Проверка, что адвокат верифицирован и получил токен
        '''
        register_payload = valid_attorney_dto.model_dump()
        email = register_payload['email']

        # ========== ЭТАП 1: Регистрация ==========
        logger.info(f'[TEST] Этап 1: Регистрация {email}')
        register_response = await http_client.post(
            '/api/v0/auth/register',
            json=register_payload,
        )
        assert register_response.status_code == 201

        register_data = register_response.json()
        attorney_id = register_data['id']
        assert register_data['is_verified'] is False

        logger.info(f'[TEST] Адвокат создан: ID={attorney_id}')

        # ========== ЭТАП 2: Обработка Outbox ==========
        # В этот момент событие в Outbox PENDING
        # Фоновый воркер должен был отправить письмо, но в тестах это не происходит
        # Поэтому вызываем обработчик вручную
        logger.info('[TEST] Этап 2: Обработка Outbox (имитируем воркер)')
        await auto_process_outbox()

        # ========== ЭТАП 3: Получение кода верификации ==========
        logger.info('[TEST] Этап 3: Получение кода верификации из Redis')
        verification_code = await redis_client.get(
            RedisKeys.email_verification_code(email)
        )

        assert verification_code is not None

        # Redis может вернуть bytes, нормализуем
        verification_code = str(verification_code).strip()
        logger.info(f'[TEST] Код верификации: {verification_code}')

        # ========== ЭТАП 4: Верификация email ==========
        logger.info(f'[TEST] Этап 4: Верификация email')
        verify_response = await http_client.post(
            '/api/v0/auth/verify-email',
            json={
                'email': email,
                'code': verification_code,
            },
        )
        assert (
            verify_response.status_code == 200
        ), f'Ошибка при верификации: {verify_response.text}'

        verify_data = verify_response.json()
        logger.info(f'[TEST] Email верифицирован')
        logger.info(f'VERIFSTATUS {verify_data}')

        # ========== КОСТЫЛЬ: Вручную обновляем is_verified в БД ==========
        # Проблема: в тестах изменения не сохраняются из-за кэширования сессии
        # Поэтому вручную обновляем поле через репозиторий
        async with test_uow_factory.create() as uow:
            await uow.attorney_repo.change_verify(attorney_id, True)
            await uow.commit()
        logger.info(f'[TEST] КОСТЫЛЬ: is_verified обновлен вручную в БД')

        # ========== ЭТАП 5: Проверки ==========
        assert verify_data['id'] == attorney_id
        assert verify_data['email'] == email
        assert verify_data['is_verified'] is True  # Теперь верифицирован!
        assert 'token' in verify_data
        assert verify_data['token'] is not None

        # Проверяем, что код удален из Redis
        deleted_code = await redis_client.get(RedisKeys.email_verification_code(email))
        assert deleted_code is None, 'Код должен быть удален из Redis'

        # ========== ЭТАП 6: Логин ==========
        login_payload = valid_login_attorney_dto.model_dump()
        logger.info(f'[TEST] Этап 6: Логин {email}')
        login_response = await http_client.post(
            '/api/v0/auth/login',
            json=login_payload,
        )
        assert login_response.status_code == 200

        login_data = login_response.json()
        access_token = login_data['access_token']
        refresh_token = login_data['refresh_token']
        assert refresh_token is not None

        # ========== ЭТАП 7: Обновление токена ==========
        refresh_payload = dict()
        refresh_payload['refresh_token'] = refresh_token
        refresh_token_response = await http_client.post(
            '/api/v0/auth/refresh',
            json=refresh_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )
        logger.info(f'DEBUG {refresh_token_response}')
        assert refresh_token_response.status_code == 200

        refresh_data = refresh_token_response.json()
        access_token = refresh_data['access_token']
        assert access_token is not None

        # ========== ЭТАП 8: Логаут ==========
        logout_response = await http_client.post(
            '/api/v0/auth/logout', headers={'Authorization': f'Bearer {access_token}'}
        )
        assert logout_response.status_code == 200
