import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from backend.core.logger import logger
from backend.domain.entities.auxiliary import EventType


class TestCreateEvent:
    '''Тесты создания события'''

    @pytest.mark.asyncio
    async def test_create_event_success(
        self,
        http_client: AsyncClient,
        valid_attorney_dto,
        valid_client_dto,
        valid_case_dto,
        valid_event_dto,
        signed_attorney,
        me_attorney,
    ):
        '''Успешное создание события авторизованным юристом'''
        access_token = signed_attorney['access_token']
        attorney_id = me_attorney['id']

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
        client_id = data['id']
        assert client_id is not None

        # ======== СОЗДАНИЕ ДЕЛА ========
        #valid_case_dto.attorney_id = attorney_id ДРУГАЯ ПРОВЕРКА ДОЛЖНА БЫТЬ!
        valid_case_dto.client_id = client_id
        case_payload = valid_case_dto.model_dump()
        create_case_response = await http_client.post(
            '/api/v0/cases',
            json=case_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )
        data = create_case_response.json()
        case_id = data['id']

        # ======== СОЗДАНИЕ СОБЫТИЯ ========
        #valid_event_dto.attorney_id = attorney_id
        valid_event_dto.case_id = case_id
        event_payload = valid_event_dto.model_dump(mode='json')

        create_event_response = await http_client.post(
            '/api/v0/events',
            json=event_payload,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        logger.info(f'[CREATE EVENT] Status: {create_event_response.status_code}')
        assert create_event_response.status_code == 201

        data = create_event_response.json()
        assert data['id'] is not None
        assert data['name'] == event_payload['name']
        assert data['description'] == event_payload['description']
        assert data['case_id'] == case_id
        assert data['attorney_id'] == attorney_id
