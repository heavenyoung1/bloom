import pytest

from backend.application.commands.case import (
    CreateCaseCommand,
    UpdateCaseCommand
    )


@pytest.fixture
def create_case_command(sample_case_for_verified_attorney):
    return CreateCaseCommand(
        name='Дело о краже',
        client_id=sample_case_for_verified_attorney.client_id,  # Реальный ID из БД
        attorney_id=sample_case_for_verified_attorney.attorney_id,  # Реальный ID из БД
        status=sample_case_for_verified_attorney.status,
        description=sample_case_for_verified_attorney.description,
    )

@pytest.fixture
def update_case_command(sample_case_for_verified_attorney):
    return UpdateCaseCommand(
        case_id=None,
        name='Дело о падении камня',
        client_id=sample_case_for_verified_attorney.client_id,  # Реальный ID из БД
        attorney_id=sample_case_for_verified_attorney.attorney_id,  # Реальный ID из БД
        status=sample_case_for_verified_attorney.status,
        description='Произошло что-то непонятное',
    )
