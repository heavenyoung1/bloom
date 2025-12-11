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
    use_case = CreateCaseUseCase(test_uow_factory)
    result = await use_case.execute(create_case_command)

    assert result.id is not None


@pytest.mark.asyncio
async def test_update_case(test_uow_factory, create_case_command, update_case_command):
    create_use_case = CreateCaseUseCase(test_uow_factory)
    created_case = await create_use_case.execute(create_case_command)
    assert created_case.id is not None

    # Обновляем кейс
    update_case_command.case_id = created_case.id
    update_use_case = UpdateCaseUseCase(test_uow_factory)
    updated_case = await update_use_case.execute(update_case_command)

    assert updated_case.id == created_case.id


@pytest.mark.asyncio
async def test_get_case_by_id(test_uow_factory, create_case_command):
    '''Тест получения кейса по ID'''
    # Создаем кейс
    create_use_case = CreateCaseUseCase(test_uow_factory)
    created_case = await create_use_case.execute(create_case_command)
    assert created_case.id is not None

    # Получаем кейс
    query = GetCaseByIdQuery(case_id=created_case.id)
    get_use_case = GetCaseByIdUseCase(test_uow_factory)
    retrieved_case = await get_use_case.execute(query)

    assert retrieved_case is not None
    assert retrieved_case.id == created_case.id


@pytest.mark.asyncio
async def test_get_all_case(test_uow_factory, create_case_command, verified_cases_list):
    attorney_id = verified_cases_list[0].attorney_id

    # Создаем кейсы
    create_use_case = CreateCaseUseCase(test_uow_factory)
    for case_data in verified_cases_list:
        cmd = CreateCaseCommand(
            name=case_data.name,
            client_id=case_data.client_id,
            attorney_id=case_data.attorney_id,
            status=case_data.status,
            description=case_data.description,
        )
        await create_use_case.execute(cmd)

    # Получаем все кейсы адвоката
    query = GetCasesForAttorneyQuery(attorney_id=attorney_id)
    get_all_cases_use_case = GetlAllCasesUseCase(test_uow_factory)
    cases = await get_all_cases_use_case.execute(query)

    assert cases is not None
    assert len(cases) >= len(verified_cases_list)


@pytest.mark.asyncio
async def test_delete_case(test_uow_factory, create_case_command):
    '''Тест удаления кейса'''
    # Создаем кейс
    create_use_case = CreateCaseUseCase(test_uow_factory)
    created_case = await create_use_case.execute(create_case_command)
    assert created_case.id is not None

    # Удаляем кейс
    cmd = DeleteCaseCommand(case_id=created_case.id)
    delete_use_case = DeleteCaseUseCase(test_uow_factory)
    result = await delete_use_case.execute(cmd)

    # Проверяем, что дело удалено
    assert result is True
    # НУЖНА ДО ПРОВЕРКА С GETUSECASE
    # СЕЙЧАС ТАМ ОШИБКА ПРИ ПОЛУЧЕНИИ NONE
