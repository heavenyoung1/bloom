import pytest
from backend.infrastructure.mappers.client_mapper import ClientMapper
from backend.domain.entities.client import Client
from backend.infrastructure.models import ClientORM
from backend.infrastructure.models.client import Messenger

class TestClientMapper:

    @pytest.fixture
    def sample_client_domain(self, persisted_attorney_id):
        return Client(
            id=456,
            name='Иван Иванович Петров',
            type=True,
            email='ivan@example.com',
            phone='+79991234567',
            personal_info='1234567890',
            address='Москва, ул. Тверская, 1',
            messenger=Messenger.TG,
            messenger_handle='ivan123',
            owner_attorney_id=persisted_attorney_id
        )

    @pytest.fixture
    def sample_client_orm(self, persisted_attorney_id):
        return ClientORM(
            id=456,
            name='Иван Иванович Петров',
            type=True,
            email='ivan@example.com',
            phone='+79991234567',
            personal_info='1234567890',
            address='Москва, ул. Тверская, 1',
            messenger=Messenger.TG,
            messenger_handle='ivan123',
            owner_attorney_id=persisted_attorney_id
        )

    def test_to_orm(self, sample_client_domain):
        orm = ClientMapper.to_orm(sample_client_domain)
        assert orm.id == sample_client_domain.id
        assert orm.name == sample_client_domain.name
        assert orm.type == sample_client_domain.type
        assert orm.email == sample_client_domain.email
        assert orm.phone == sample_client_domain.phone
        assert orm.personal_info == sample_client_domain.personal_info
        assert orm.address == sample_client_domain.address
        assert orm.messenger == sample_client_domain.messenger
        assert orm.messenger_handle == sample_client_domain.messenger_handle
        assert orm.created_at == sample_client_domain.created_at
        assert orm.owner_attorney_id == sample_client_domain.owner_attorney_id

    def test_to_domain(self, sample_client_orm):
        domain = ClientMapper.to_domain(sample_client_orm)
        assert domain.id == sample_client_orm.id
        assert domain.name == sample_client_orm.name
        assert domain.type == sample_client_orm.type
        assert domain.email == sample_client_orm.email
        assert domain.phone == sample_client_orm.phone
        assert domain.personal_info == sample_client_orm.personal_info
        assert domain.address == sample_client_orm.address
        assert domain.messenger == sample_client_orm.messenger
        assert domain.messenger_handle == sample_client_orm.messenger_handle
        assert domain.created_at == sample_client_orm.created_at
        assert domain.owner_attorney_id == sample_client_orm.owner_attorney_id
