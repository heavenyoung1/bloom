import pytest
from backend.infrastructure.mappers.attorney_mapper import AttorneyMapper
from backend.domain.entities.attorney import Attorney
from backend.infrastructure.models import AttorneyORM


class TestAttorneyMapper:

    @pytest.fixture
    def sampleattorney_domain(self):
        return Attorney(
            id=None,
            license_id='322/4767',
            first_name='Иван',
            last_name='Петров',
            patronymic='Сергеевич',
            email='ivan.petrov@example.com',
            phone='+79991112233',
            password_hash='hashed_password_123',
            is_active=True,
        )

    @pytest.fixture
    def sampleattorney_orm(self):
        return AttorneyORM(
            id=None,
            license_id='322/4767',
            first_name='Иван',
            last_name='Петров',
            patronymic='Сергеевич',
            email='ivan.petrov@example.com',
            phone='+79991112233',
            password_hash='hashed_password_123',
            is_active=True,
        )

    def test_to_orm(self, sampleattorney_domain):
        orm = AttorneyMapper.to_orm(sampleattorney_domain)
        assert orm.id == sampleattorney_domain.id
        assert orm.license_id == sampleattorney_domain.license_id
        assert orm.first_name == sampleattorney_domain.first_name
        assert orm.last_name == sampleattorney_domain.last_name
        assert orm.patronymic == sampleattorney_domain.patronymic
        assert orm.email == sampleattorney_domain.email
        assert orm.phone == sampleattorney_domain.phone
        assert orm.password_hash == sampleattorney_domain.password_hash
        assert orm.is_active == sampleattorney_domain.is_active
        assert orm.created_at == sampleattorney_domain.created_at

    def test_to_domain(self, sampleattorney_orm):
        domain = AttorneyMapper.to_domain(sampleattorney_orm)
        assert domain.id == sampleattorney_orm.id
        assert domain.license_id == sampleattorney_orm.license_id
        assert domain.first_name == sampleattorney_orm.first_name
        assert domain.last_name == sampleattorney_orm.last_name
        assert domain.patronymic == sampleattorney_orm.patronymic
        assert domain.email == sampleattorney_orm.email
        assert domain.phone == sampleattorney_orm.phone
        assert domain.password_hash == sampleattorney_orm.password_hash
        assert domain.is_active == sampleattorney_orm.is_active
        assert domain.created_at == sampleattorney_orm.created_at
