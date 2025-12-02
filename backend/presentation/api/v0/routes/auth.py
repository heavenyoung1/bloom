from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logger import logger
from backend.application.services.auth_service_dor.dependencies import get_uow_factory
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.usecases.auth.sign_in import SignInUseCase
from backend.application.usecases.auth.sign_up import SignUpUseCase
from backend.application.services.auth_service import AuthService
#from backend.application.services.auth_service_dor.database import get_user_db
from backend.application.dto.attorney import (
    AttorneyResponse,
    RegisterRequest,
    LoginRequest,
    UpdateRequest,
    TokenResponse,
)

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post(
    '/register', response_model=AttorneyResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest, uow_factory: UnitOfWorkFactory = Depends(get_uow_factory)
):
    '''Регистрация нового юриста'''
    try:
        use_case = SignUpUseCase(uow_factory)
        return await use_case.execute(request)

    except ValueError as e:
        logger.error(f'Ошибка валидации при регистрации: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f'Критическая ошибка при регистрации: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Registration failed',
        )


@router.post('/login', response_model=TokenResponse)
async def login(
    request: LoginRequest, uow_factory: UnitOfWorkFactory = Depends(get_uow_factory)
):
    '''Вход в систему'''
    try:
        use_case = SignInUseCase(uow_factory)
        return await use_case.execute(request)

    except ValueError as e:
        logger.error(f'Ошибка при входе: {str(e)}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logger.error(f'Критическая ошибка при входе: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Login failed'
        )


@router.post('/refresh', response_model=TokenResponse)
async def refresh(
    body: dict,  # {'refresh_token': '...', 'attorney_id': 123}
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''Обновить access token'''
    try:
        refresh_token = body.get('refresh_token')
        attorney_id = body.get('attorney_id')

        if not refresh_token or not attorney_id:
            raise ValueError('Missing refresh_token or attorney_id')

        service = AuthService(uow_factory)
        new_access_token = await service.refresh_access_token(
            refresh_token, attorney_id
        )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_token,
            expires_in=15 * 60,  # 15 минут
        )

    except ValueError as e:
        logger.error(f'Ошибка при refresh: {str(e)}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post('/logout')
async def logout(
    body: dict,  # {'attorney_id': 123}
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''Выход из системы'''
    try:
        attorney_id = body.get('attorney_id')
        if not attorney_id:
            raise ValueError('Missing attorney_id')

        service = AuthService(uow_factory)
        await service.logout(attorney_id)

        return {'message': 'Logged out successfully'}

    except Exception as e:
        logger.error(f'Ошибка при logout: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Logout failed'
        )
