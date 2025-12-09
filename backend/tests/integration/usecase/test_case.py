import pytest

from backend.application.usecases.case import (
    CreateCaseUseCase,
    UpdateCaseUseCase,

)
from backend.application.commands.case import CreateCaseCommand


@pytest.mark.asyncio
async def test_create_case(test_uow_factory, create_case_command):
    # Создаем UseCase с реальными репозиториями
    async with test_uow_factory.create() as uow:
        use_case = CreateCaseUseCase(test_uow_factory)
        # Передаем экземпляр CreateCaseCommand
        result = await use_case.execute(create_case_command)

        assert result.id is not None

@pytest.mark.asyncio
async def test_update_case(test_uow_factory, create_case_command, update_case_command):
    # Создаем UseCase с реальными репозиториями
    async with test_uow_factory.create() as uow:
        create_use_case = CreateCaseUseCase(test_uow_factory)
        result = await create_use_case.execute(create_case_command)
        assert result.id is not None
        
        # Теперь добавляем ID для обновления
        update_case_command.case_id = result.id  # Устанавливаем ID для обновления

        update_use_case = UpdateCaseUseCase(test_uow_factory)
        updated_result = await update_use_case.execute(update_case_command)
        assert updated_result.id is not None
        assert updated_result.id == result.id  # Проверяем, что ID совпадает
