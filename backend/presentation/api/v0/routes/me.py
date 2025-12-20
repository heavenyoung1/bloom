from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
)
from backend.core.logger import logger
from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)

# ========== USE CASES ==========
from backend.application.usecases.auth.update_addtorney import UpdateAttorneyUseCase
from backend.application.usecases.auth.delete_attorney import DeleteAttorneyAccountUseCase

# ========== COMMANDS & QUERIES ==========
from backend.application.commands.attorney import (
    UpdateAttorneyCommand,
    DeleteAttorneyAccountCommand,
)

# ========== DTOs ==========
from backend.application.dto.attorney import (
    AttorneyResponse,
    UpdateRequest,
)

# ========== Router ==========
router = APIRouter(prefix='/api/v0', tags=['me'])


# ========== GET PROFILE ==========
@router.get(
    '/me',
    response_model=AttorneyResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение профиля текущего адвоката',
    responses={
        200: {'description': 'Профиль адвоката'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Адвокат не найден'},
    },
)
async def get_me(
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Получение профиля текущего адвоката.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Получение профиля: ID={current_attorney_id}')

        async with uow_factory.create() as uow:
            attorney = await uow.attorney_repo.get(current_attorney_id)
            if not attorney:
                raise EntityNotFoundException(
                    f'Адвокат с ID {current_attorney_id} не найден'
                )

            return AttorneyResponse.model_validate(attorney)

    except EntityNotFoundException as e:
        logger.error(f'Адвокат не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении профиля: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении профиля',
        )


# ========== UPDATE PROFILE ==========
@router.patch(
    '/me',
    response_model=AttorneyResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление профиля адвоката',
    responses={
        200: {'description': 'Профиль успешно обновлен'},
        400: {'description': 'Ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Адвокат не найден'},
    },
)
async def update_me(
    request: UpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Обновление профиля адвоката (PATCH - частичное обновление).

    Можно обновить только переданные поля:
    - first_name
    - last_name
    - patronymic
    - phone
    - license_id
    - telegram_username

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Обновление профиля: ID={current_attorney_id}')

        # 1. Парсим request в Command
        cmd = UpdateAttorneyCommand(
            attorney_id=current_attorney_id,
            first_name=request.first_name,
            last_name=request.last_name,
            patronymic=request.patronymic,
            phone=request.phone,
            license_id=request.license_id,
            telegram_username=request.telegram_username,
            email=request.email,
        )

        # 2. Создаем UseCase и выполняем
        use_case = UpdateAttorneyUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Профиль успешно обновлен: ID={current_attorney_id}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Адвокат не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при обновлении профиля: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении профиля',
        )


# ========== DELETE ACCOUNT ==========
class DeleteAccountRequest(BaseModel):
    '''Запрос на удаление аккаунта'''
    password: str = Field(..., min_length=1, description='Пароль для подтверждения')


@router.delete(
    '/me',
    status_code=status.HTTP_200_OK,
    summary='Удаление аккаунта адвоката',
    responses={
        200: {'description': 'Аккаунт успешно удален'},
        400: {'description': 'Неправильный пароль'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Адвокат не найден'},
    },
)
async def delete_me(
    request: DeleteAccountRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    access_token: str = Depends(get_current_access_token),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Удаление аккаунта адвоката.

    Требуется подтверждение паролем для безопасности.
    Удаление происходит каскадно (все связанные данные).

    Requires:
        - Authorization: Bearer <access_token>
        - password: пароль для подтверждения (в теле запроса)
    '''
    try:
        logger.info(f'Попытка удаления аккаунта: ID={current_attorney_id}')

        # 1. Парсим request в Command
        cmd = DeleteAttorneyAccountCommand(
            attorney_id=current_attorney_id,
            password=request.password,
        )

        # 2. Создаем UseCase и выполняем
        use_case = DeleteAttorneyAccountUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.warning(f'Аккаунт успешно удален: ID={current_attorney_id}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Адвокат не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при удалении аккаунта: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении аккаунта',
        )

