from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

from backend.application.dto.attorney import (
    UpdateRequest,
    AttorneyResponse,
)

from backend.application.usecases.auth.update_addtorney import UpdateAttorneyUseCase

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
)

from backend.application.commands.attorney import (
    UpdateAttorneyCommand,
)

from backend.core.logger import logger
from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
)

# ========== Router ==========
router = APIRouter(prefix='/api/v0', tags=['attorney'])


# ========== UPDATE PROFILE ==========
@router.patch(
    '/attorney/me',
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
async def update_attorney_profile(
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
    - email

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