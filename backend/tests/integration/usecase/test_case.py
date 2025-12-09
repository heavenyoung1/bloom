import pytest

from backend.application.usecases.case.create import CreateCaseUseCase
from backend.application.commands.case import CreateCaseCommand


@pytest.mark.asyncio
async def test_create_case(test_uow_factory, create_case_command):
    # Создаем UseCase с реальными репозиториями
    async with test_uow_factory.create() as uow:
        use_case = CreateCaseUseCase(test_uow_factory)
        # Передаем экземпляр CreateCaseCommand
        result = await use_case.execute(create_case_command)

        assert result.id is not None
