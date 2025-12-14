import pytest


# @pytest.mark.asyncio
# async def test_create_client(http_client, valid_client_dto):
#     payload = {
#         'name': 'Иван Иванов',
#         'type': True,
#         'email': 'client1@example.com',
#         'phone': '+79990001122',
#         'personal_info': 'паспорт ...',
#         'address': 'СПб',
#         'messenger': 'Telegram',
#         'messenger_handle': '@ivan',
#     }

#     r = await http_client.post('/api/v1/clients', json=payload)
#     assert r.status_code == 201, r.text

#     data = r.json()
#     assert data['id'] is not None
#     assert data['email'] == payload['email']
#     assert data['name'] == payload['name']
