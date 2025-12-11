from backend.core.exceptions import ValidationException

import pytest
import re


class TestAttorneyPolicy:
    @pytest.mark.asyncio
    async def test_validate_on_create(
        self, attorney_repo_mock, valid_attorney_dto, attorney_validator
    ):
        '''Тест для успешной валидации, когда данные корректны'''

        # Мокаем методы репозитория
        attorney_repo_mock.get_by_email.return_value = None
        attorney_repo_mock.get_by_license_id.return_value = None
        attorney_repo_mock.get_by_phone.return_value = None

        await attorney_validator.on_register(valid_attorney_dto)

        attorney_repo_mock.get_by_email.assert_called_once_with(
            valid_attorney_dto.email
        )
        attorney_repo_mock.get_by_license_id.assert_called_once_with(
            valid_attorney_dto.license_id
        )
        attorney_repo_mock.get_by_phone.assert_called_once_with(
            valid_attorney_dto.phone
        )

    @pytest.mark.asyncio
    async def test_validate_on_create_email_taken(
        self, attorney_validator, attorney_repo_mock, valid_attorney_dto
    ):
        '''Тест для случая, когда email уже занят'''

        # Мокаем методы репозитория
        attorney_repo_mock.get_by_email.return_value = True
        attorney_repo_mock.get_by_license_id.return_value = None
        attorney_repo_mock.get_by_phone.return_value = None

        # Проверяем, что выбрасывается исключение для email
        with pytest.raises(
            ValidationException,
            match=f'Email {valid_attorney_dto.email} уже зарегистрирован',
        ):
            await attorney_validator.on_register(valid_attorney_dto)

        attorney_repo_mock.get_by_email.assert_called_once_with(
            valid_attorney_dto.email
        )

    @pytest.mark.asyncio
    async def test_validate_on_create_license_id_taken(
        self, attorney_validator, attorney_repo_mock, valid_attorney_dto
    ):
        '''Тест для случая, когда номер удостоверения уже занят'''

        # Мокаем методы репозитория
        attorney_repo_mock.get_by_email.return_value = None
        attorney_repo_mock.get_by_license_id.return_value = True
        attorney_repo_mock.get_by_phone.return_value = None

        # Проверяем, что выбрасывается исключение для email
        with pytest.raises(
            ValidationException,
            match=f'Номер Удостоверения адвоката {valid_attorney_dto.license_id} уже зарегистрирован',
        ):
            await attorney_validator.on_register(valid_attorney_dto)

        attorney_repo_mock.get_by_license_id.assert_called_once_with(
            valid_attorney_dto.license_id
        )

    @pytest.mark.asyncio
    async def test_validate_on_create_phone_taken(
        self, attorney_validator, attorney_repo_mock, valid_attorney_dto
    ):
        '''Тест для случая, когда номер телефона уже занят'''

        # Мокаем методы репозитория
        attorney_repo_mock.get_by_email.return_value = None
        attorney_repo_mock.get_by_license_id.return_value = None
        attorney_repo_mock.get_by_phone.return_value = True

        # Проверяем, что выбрасывается исключение для email
        with pytest.raises(
            ValidationException,
            match=re.escape(f'Номер телефона {valid_attorney_dto.phone} уже занят'),
        ):
            await attorney_validator.on_register(valid_attorney_dto)

        attorney_repo_mock.get_by_phone.assert_called_once_with(
            valid_attorney_dto.phone
        )
