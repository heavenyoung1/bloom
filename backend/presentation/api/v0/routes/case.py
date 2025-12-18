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
from backend.application.usecases.case.create import CreateCaseUseCase
from backend.application.usecases.case.get import GetCaseByIdUseCase
from backend.application.usecases.case.get_all import GetlAllCasesUseCase
from backend.application.usecases.case.update import UpdateCaseUseCase
from backend.application.usecases.case.delete import DeleteCaseUseCase

# ========== COMMANDS & QUERIES ==========
from backend.application.commands.case import (
    CreateCaseCommand,
    UpdateCaseCommand,
    DeleteCaseCommand,
    GetCaseByIdQuery,
    GetCasesForAttorneyQuery,
)

# ========== DTOs ==========
from backend.application.dto.case import (
    CaseCreateRequest,
    CaseUpdateRequest,
    CaseResponse,
)

# ========== Router ==========
router = APIRouter(prefix='/api/v0', tags=['cases'])

# ========== CASE ENDPOINTS ==========


@router.post(
    '/cases',
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового дела',
    responses={
        201: {'description': 'Дело успешно создано'},
        400: {'description': 'Ошибка валидации или клиент не найден'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Клиент не найден'},
    },
)
async def create_case(
    request: CaseCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Создание нового дела.

    Flow:
    1. Проверка что клиент существует и принадлежит адвокату
    2. Валидация данных дела
    3. Создание дела в БД
    4. Возврат данных дела

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(
            f'Попытка создания дела: {request.name} (адвокат={current_attorney_id})'
        )

        cmd = CreateCaseCommand(
            name=request.name,
            client_id=request.client_id,
            attorney_id=current_attorney_id,
            status=request.status,
            description=request.description,
        )

        use_case = CreateCaseUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Дело успешно создано: {request.name}')
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
            detail='Ошибка при создании дела',
        )


@router.get(
    '/cases/{case_id}',
    response_model=CaseResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение данных дела',
    responses={
        200: {'description': 'Данные дела'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Дело не найдено'},
    },
)
async def get_case(
    case_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение данных дела по ID.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение дела: ID={case_id}')

        cmd = GetCaseByIdQuery(case_id=case_id)
        use_case = GetCaseByIdUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result

    except EntityNotFoundException as e:
        logger.error(f'Дело не найдено: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении дела: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении дела',
        )


@router.get(
    '/cases',
    response_model=list[CaseResponse],
    status_code=status.HTTP_200_OK,
    summary='Получение всех дел адвоката',
    responses={
        200: {'description': 'Список дел'},
        401: {'description': 'Требуется авторизация'},
    },
)
async def list_cases(
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение списка всех дел текущего адвоката.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение списка дел: адвокат={current_attorney_id}')

        cmd = GetCasesForAttorneyQuery(attorney_id=current_attorney_id)
        use_case = GetlAllCasesUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result

    except EntityNotFoundException as e:
        logger.warning(f'Нет дел: {e}')
        return []  # Возвращаем пустой список вместо ошибки
    except Exception as e:
        logger.error(f'Ошибка при получении дел: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении дел',
        )


@router.put(
    '/cases/{case_id}',
    response_model=CaseResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление данных дела',
    responses={
        200: {'description': 'Дело успешно обновлено'},
        400: {'description': 'Ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Дело не найдено'},
    },
)
async def update_case(
    case_id: int,
    request: CaseUpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Обновление данных дела.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Обновление дела: ID={case_id}')

        cmd = UpdateCaseCommand(
            case_id=case_id,
            name=request.name,
            client_id=request.client_id,
            attorney_id=current_attorney_id,
            status=request.status,
            description=request.description,
        )

        use_case = UpdateCaseUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Дело успешно обновлено: ID={case_id}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Дело не найдено: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при обновлении дела: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении дела',
        )


@router.delete(
    '/cases/{case_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление дела',
    responses={
        204: {'description': 'Дело успешно удалено'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Дело не найдено'},
    },
)
async def delete_case(
    case_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Удаление дела.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Удаление дела: ID={case_id}')

        cmd = DeleteCaseCommand(case_id=case_id)
        use_case = DeleteCaseUseCase(uow_factory)
        await use_case.execute(cmd)

        logger.info(f'Дело успешно удалено: ID={case_id}')

    except EntityNotFoundException as e:
        logger.error(f'Дело не найдено: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при удалении дела: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении дела',
        )
