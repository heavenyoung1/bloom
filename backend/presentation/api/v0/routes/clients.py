from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
)
from backend.core.logger import logger
from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)

# ========== USE CASES ==========
from backend.application.usecases.client.create import CreateClientUseCase
from backend.application.usecases.client.get import GetClientByIdUseCase
from backend.application.usecases.client.get_all import GetClientsForAttorneyUseCase
from backend.application.usecases.client.update import UpdateClientUseCase
from backend.application.usecases.client.delete import DeleteClientUseCase

from backend.application.usecases.case.create import CreateCaseUseCase
from backend.application.usecases.case.get import GetCaseByIdUseCase
from backend.application.usecases.case.get_all import GetlAllCasesUseCase
from backend.application.usecases.case.update import UpdateCaseUseCase
from backend.application.usecases.case.delete import DeleteCaseUseCase

# ========== COMMANDS & QUERIES ==========
from backend.application.commands.client import (
    CreateClientCommand,
    UpdateClientCommand,
    DeleteClientCommand,
    GetClientByIdQuery,
    GetClientsForAttorneyQuery,
)


# ========== DTOs ==========
from backend.application.dto.client import (
    ClientCreateRequest,
    ClientUpdateRequest,
    ClientResponse,
)


# ========== Router ==========
router = APIRouter(prefix='/api/v0', tags=['clients'])


# ========== CLIENT ENDPOINTS ==========
@router.post(
    '/clients',
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового клиента',
    responses={
        201: {'description': 'Клиент успешно создан'},
        400: {'description': 'Email уже зарегистрирован или ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
    },
)
async def create_client(
    request: ClientCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Создание нового клиента.

    Flow:
    1. Валидация данных
    2. Проверка что email не занят
    3. Создание клиента, привязанного к адвокату
    4. Возврат данных клиента

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Создание клиента: {request.email} (юрист={current_attorney_id})')
        cmd = CreateClientCommand(
            name=request.name,
            type=request.type,
            email=request.email,
            phone=request.phone,
            personal_info=request.personal_info,
            address=request.address,
            messenger=request.messenger,
            messenger_handle=request.messenger_handle,
            owner_attorney_id=current_attorney_id,
        )
        use_case = CreateClientUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Клиент успешно создан: {request.email}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Сущность не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при создании клиента',
        )


@router.get(
    '/clients/{client_id}',
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение данных клиента',
    responses={
        200: {'description': 'Данные клиента'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Клиент не найден'},
    },
)
async def get_client(
    client_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение данных клиента по ID.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение клиента: ID={client_id}')

        cmd = GetClientByIdQuery(client_id=client_id)
        use_case = GetClientByIdUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result

    except EntityNotFoundException as e:
        logger.error(f'Клиент не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении клиента: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении клиента',
        )


@router.get(
    '/clients',
    response_model=list[ClientResponse],
    status_code=status.HTTP_200_OK,
    summary='Получение всех клиентов адвоката',
    responses={
        200: {'description': 'Список клиентов'},
        401: {'description': 'Требуется авторизация'},
    },
)
async def list_clients(
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение списка всех клиентов текущего адвоката.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение списка клиентов: адвокат={current_attorney_id}')

        cmd = GetClientsForAttorneyQuery(owner_attorney_id=current_attorney_id)
        use_case = GetClientsForAttorneyUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result

    except Exception as e:
        logger.error(f'Ошибка при получении клиентов: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении клиентов',
        )


@router.put(
    '/clients/{client_id}',
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление данных клиента',
    responses={
        200: {'description': 'Клиент успешно обновлен'},
        400: {'description': 'Ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Клиент не найден'},
    },
)
async def update_client(
    client_id: int,
    request: ClientUpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Обновление данных клиента.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Обновление клиента: ID={client_id}')

        cmd = UpdateClientCommand(
            client_id=client_id,
            name=request.name,
            type=request.type,
            email=request.email,
            phone=request.phone,
            personal_info=request.personal_info,
            address=request.address,
            messenger=request.messenger,
            messenger_handle=request.messenger_handle,
            owner_attorney_id=current_attorney_id,
        )

        use_case = UpdateClientUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Клиент успешно обновлен: ID={client_id}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Клиент не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при обновлении клиента: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении клиента',
        )


@router.delete(
    '/clients/{client_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление клиента',
    responses={
        204: {'description': 'Клиент успешно удален'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Клиент не найден'},
    },
)
async def delete_client(
    client_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Удаление клиента.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Удаление клиента: ID={client_id}')

        cmd = DeleteClientCommand(client_id=client_id)
        use_case = DeleteClientUseCase(uow_factory)
        await use_case.execute(cmd)

        logger.info(f'Клиент успешно удален: ID={client_id}')

    except EntityNotFoundException as e:
        logger.error(f'Клиент не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при удалении клиента: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении клиента',
        )
