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
from backend.application.usecases.contact import (
    CreateContactUseCase,
    UpdateContactUseCase,
    GetContactByIdUseCase,
    GetAllContactsUseCase,
    DeleteContactUseCase,
)

# ========== COMMANDS & QUERIES ==========
from backend.application.commands.contact import (
    CreateContactCommand,
    GetContactByIdQuery,
    GetContactsForAttorneyQuery,
    UpdateContactCommand,
    DeleteContactCommand,
)

# ========== DTOs ==========
from backend.application.dto.contact import (
    ContactCreateRequest,
    ContactUpdateRequest,
    ContactResponse,
)

# ========== Router ==========
router = APIRouter(prefix='/api/v0', tags=['contacts'])

# ========== CONTACT ENDPOINTS ==========


@router.post(
    '/contacts',
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового контакта',
    responses={
        201: {'description': 'Контакт успешно создан'},
        400: {'description': 'Ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Дело не найдено'},
    },
)
async def create_contact(
    request: ContactCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Создание нового контакта, связанного с делом.

    Flow:
    1. Валидация данных
    2. Проверка что дело существует и принадлежит адвокату
    3. Создание контакта
    4. Возврат данных контакта

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(
            f'Создание контакта: {request.name} '
            f'для дела {request.case_id} (адвокат={current_attorney_id})'
        )

        cmd = CreateContactCommand(
            name=request.name,
            personal_info=request.personal_info or '',
            phone=request.phone or '',
            email=request.email or '',
            attorney_id=current_attorney_id,
            case_id=request.case_id,
        )

        use_case = CreateContactUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Контакт успешно создан: {request.name}')
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
            detail='Ошибка при создании контакта',
        )


@router.get(
    '/contacts/{contact_id}',
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение данных контакта',
    responses={
        200: {'description': 'Данные контакта'},
        401: {'description': 'Требуется авторизация'},
        403: {'description': 'Нет доступа к контакту'},
        404: {'description': 'Контакт не найден'},
    },
)
async def get_contact(
    contact_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение данных контакта по ID.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение контакта: ID={contact_id}')

        cmd = GetContactByIdQuery(contact_id=contact_id)
        use_case = GetContactByIdUseCase(uow_factory)
        result = await use_case.execute(cmd)

        # Проверка прав доступа (если use case не делает это сам)
        if result.attorney_id != current_attorney_id:
            raise AccessDeniedException('У вас нет доступа к этому контакту')

        return result

    except EntityNotFoundException as e:
        logger.error(f'Контакт не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccessDeniedException as e:
        logger.error(f'Нет доступа: {e}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении контакта: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении контакта',
        )


@router.get(
    '/contacts',
    response_model=list[ContactResponse],
    status_code=status.HTTP_200_OK,
    summary='Получение всех контактов адвоката',
    responses={
        200: {'description': 'Список контактов'},
        401: {'description': 'Требуется авторизация'},
    },
)
async def list_contacts(
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение списка всех контактов текущего адвоката.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение списка контактов: адвокат={current_attorney_id}')

        cmd = GetContactsForAttorneyQuery(attorney_id=current_attorney_id)
        use_case = GetAllContactsUseCase(uow_factory)
        result = await use_case.execute(cmd)

        return result

    except Exception as e:
        logger.error(f'Ошибка при получении контактов: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении контактов',
        )


@router.put(
    '/contacts/{contact_id}',
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление данных контакта',
    responses={
        200: {'description': 'Контакт успешно обновлен'},
        400: {'description': 'Ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
        403: {'description': 'Нет доступа к контакту'},
        404: {'description': 'Контакт не найден'},
    },
)
async def update_contact(
    contact_id: int,
    request: ContactUpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Обновление данных контакта.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Обновление контакта: ID={contact_id}')

        cmd = UpdateContactCommand(
            contact_id=contact_id,
            name=request.name,
            personal_info=request.personal_info,
            phone=request.phone,
            email=request.email,
        )

        use_case = UpdateContactUseCase(uow_factory)
        result = await use_case.execute(cmd, attorney_id=current_attorney_id)

        logger.info(f'Контакт успешно обновлен: ID={contact_id}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Контакт не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccessDeniedException as e:
        logger.error(f'Нет доступа: {e}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при обновлении контакта: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении контакта',
        )


@router.delete(
    '/contacts/{contact_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление контакта',
    responses={
        204: {'description': 'Контакт успешно удален'},
        401: {'description': 'Требуется авторизация'},
        403: {'description': 'Нет доступа к контакту'},
        404: {'description': 'Контакт не найден'},
    },
)
async def delete_contact(
    contact_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Удаление контакта.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Удаление контакта: ID={contact_id}')

        cmd = DeleteContactCommand(contact_id=contact_id)
        use_case = DeleteContactUseCase(uow_factory)
        await use_case.execute(cmd, attorney_id=current_attorney_id)

        logger.info(f'Контакт успешно удален: ID={contact_id}')

    except EntityNotFoundException as e:
        logger.error(f'Контакт не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccessDeniedException as e:
        logger.error(f'Нет доступа: {e}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при удалении контакта: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении контакта',
        )
