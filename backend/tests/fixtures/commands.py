import pytest

from backend.application.commands.case import CreateCaseCommand


@pytest.fixture
def create_case_command(sample_case):
    return CreateCaseCommand(
        name='Дело о краже',
        client_id=sample_case.client_id,  # Реальный ID из БД
        attorney_id=sample_case.attorney_id,  # Реальный ID из БД
        status=sample_case.status,
        description=sample_case.description,
    )
