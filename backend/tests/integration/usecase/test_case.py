import pytest

from backend.application.usecases.case import (
    CreateCaseUseCase,
    UpdateCaseUseCase,
    GetCaseByIdUseCase,
    DeleteCaseUseCase,
    GetlAllCasesUseCase,
)
from backend.application.commands.case import (
    CreateCaseCommand,
    GetCaseByIdQuery,
    GetCasesForAttorneyQuery,
    DeleteCaseCommand,
)
from backend.core.logger import logger


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


@pytest.mark.asyncio
async def test_get_case(test_uow_factory, create_case_command):
    # Создаем UseCase с реальными репозиториями
    async with test_uow_factory.create() as uow:
        create_use_case = CreateCaseUseCase(test_uow_factory)
        result = await create_use_case.execute(create_case_command)
        assert result.id is not None
        saved_case_id = result.id
        
        cmd = GetCaseByIdQuery(
            case_id=saved_case_id
        )
        get_use_case = GetCaseByIdUseCase(uow)
        result = await get_use_case.execute(cmd)
        logger.info(f'РЕЗУЛЬТАТ1 {result}')

@pytest.mark.asyncio
async def test_get_all_case(test_uow_factory, create_case_command, verified_cases_list):
    async with test_uow_factory.create() as uow:
        for i in verified_cases_list:
            cmd = CreateCaseCommand(
                name=i.name,
                client_id=i.client_id,
                attorney_id=i.attorney_id,
                status=i.status,
                description=i.description,
            )
            create_use_case = CreateCaseUseCase(test_uow_factory)
            result = await create_use_case.execute(cmd)
            logger.info(f'РЕЗУЛЬТАТ2 {result}')
        assert result.id is not None
        owner_attorney_id = result.attorney_id

        cmd = GetCasesForAttorneyQuery(
            attorney_id=owner_attorney_id,
        )
        get_all_cases_use_case = GetlAllCasesUseCase(test_uow_factory)
        result = await get_all_cases_use_case.execute(cmd)
        logger.info(f'РЕЗУЛЬТАТ2 {result}')

@pytest.mark.asyncio
async def test_delete_case(test_uow_factory, create_case_command):
    # Создаем UseCase с реальными репозиториями
    async with test_uow_factory.create() as uow:
        create_use_case = CreateCaseUseCase(test_uow_factory)
        result = await create_use_case.execute(create_case_command)
        assert result.id is not None
        saved_case_id = result.id
        
        cmd = DeleteCaseCommand(
            case_id=saved_case_id
        )
        delete_use_case = DeleteCaseUseCase(uow)
        result = await delete_use_case.execute(cmd)
        logger.info(f'РЕЗУЛЬТАТ1 {result}')