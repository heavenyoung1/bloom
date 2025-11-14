import pytest
from backend.infrastructure.mappers.case_mapper import CaseMapper
from backend.domain.entities.case import Case
from backend.infrastructure.models import CaseORM
from backend.infrastructure.models.case import CaseStatus


class TestCaseMapper:

    @pytest.fixture
    def sample_case_domain(self, persisted_attorney_id, persisted_client_id):
        return Case(
            id=123,
            name='Дело о краже',
            client_id=persisted_client_id,
            attorney_id=persisted_attorney_id,
            status=CaseStatus.IN_PROGRESS,
            description='Описание дела о краже',
        )

    @pytest.fixture
    def sample_case_orm(self, persisted_attorney_id, persisted_client_id):
        return CaseORM(
            id=123,
            name='Дело о краже',
            client_id=persisted_client_id,
            attorney_id=persisted_attorney_id,
            status=CaseStatus.IN_PROGRESS,
            description='Описание дела о краже',
        )

    def test_to_orm(self, sample_case_domain):
        orm = CaseMapper.to_orm(sample_case_domain)
        assert orm.id == sample_case_domain.id
        assert orm.name == sample_case_domain.name
        assert orm.client_id == sample_case_domain.client_id
        assert orm.attorney_id == sample_case_domain.attorney_id
        assert orm.status == sample_case_domain.status
        assert orm.description == sample_case_domain.description
        assert orm.created_at == sample_case_domain.created_at
        assert orm.updated_at == sample_case_domain.updated_at

    def test_to_domain(self, sample_case_orm):
        domain = CaseMapper.to_domain(sample_case_orm)
        assert domain.id == sample_case_orm.id
        assert domain.name == sample_case_orm.name
        assert domain.client_id == sample_case_orm.client_id
        assert domain.attorney_id == sample_case_orm.attorney_id
        assert domain.status == sample_case_orm.status
        assert domain.description == sample_case_orm.description
        assert domain.created_at == sample_case_orm.created_at
        assert domain.updated_at == sample_case_orm.updated_at
