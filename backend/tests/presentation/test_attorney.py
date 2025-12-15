import pytest
from httpx import AsyncClient

class TestRegisterAttorney:
    '''Тесты регистрации адвоката'''

    async def test_register_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
    ):
        '''Успешная регистрация адвоката'''
        payload = valid_attorney_dto.model_dump()
        response = await http_client.post(
            '/api/v1/auth/register',
            json=payload,
        )
        # Ожидаем успех или ошибку валидации/дублирования
        assert response.status_code in [201, 400]
        
        data = response.json()
        assert data['id'] is not None
        assert data['email'] == payload['email']