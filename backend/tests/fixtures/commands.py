import pytest

from backend.application.commands.case import CreateCaseCommand


@pytest.fixture
def create_case_command(sample_case_for_verified_attorney):
    return CreateCaseCommand(
        name='Дело о краже',
        client_id=sample_case_for_verified_attorney.client_id,  # Реальный ID из БД
        attorney_id=sample_case_for_verified_attorney.attorney_id,  # Реальный ID из БД
        status=sample_case_for_verified_attorney.status,
        description=sample_case_for_verified_attorney.description,
    )
