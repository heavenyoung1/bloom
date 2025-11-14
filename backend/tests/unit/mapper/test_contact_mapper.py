import pytest
from backend.infrastructure.mappers.contact_mapper import ContactMapper
from backend.domain.entities.contact import Contact
from backend.infrastructure.models import ContactORM


class TestContactMapper:

    @pytest.fixture
    def sample_contact_domain(self, persisted_case):
        return Contact(
            id=None,
            name='Иван Иванович Петров',
            personal_info='1234567890',
            phone='+79991234567',
            email='ivan@example.com',
            case_id=persisted_case,
        )

    @pytest.fixture
    def sample_contact_orm(self, persisted_case):
        return ContactORM(
            id=None,
            name='Иван Иванович Петров',
            personal_info='1234567890',
            phone='+79991234567',
            email='ivan@example.com',
            case_id=persisted_case,
        )

    def test_to_orm(self, sample_contact_domain):
        orm = ContactMapper.to_orm(sample_contact_domain)
        assert orm.id == sample_contact_domain.id
        assert orm.name == sample_contact_domain.name
        assert orm.personal_info == sample_contact_domain.personal_info
        assert orm.phone
