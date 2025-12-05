from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.usecases.auth.sign_in import SignInUseCase
from backend.application.usecases.auth.sign_up import SignUpUseCase
from backend.application.usecases.auth.verify_email import VerifyEmailUseCase
from backend.application.usecases.auth.resend_verification import (
    ResendVerificationUseCase,
)
from backend.application.services.auth_service import AuthService
from backend.core.dependencies import get_uow_factory
from backend.application.dto.attorney import (
    AttorneyResponse,
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    VerifyEmailRequest,
    ResendVerificationRequest,
)
from backend.core.logger import logger


router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post(
    '/register',
    response_model=AttorneyResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Register new attorney',
)
async def register(
    request: RegisterRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Регистрация нового юриста

    На этот email будет отправлен код верификации
    '''
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


@router.post('/verify-email')
async def verify_email(
    request: VerifyEmailRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Подтвердить email по коду

    Шаг 2 после регистрации
    '''
    try:
        use_case = VerifyEmailUseCase(uow_factory)
        return await use_case.execute(request)

    except ValueError as e:
        logger.error(f'Ошибка при верификации: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при верификации: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Verification failed',
        )


@router.post('/resend-verification')
async def resend_verification(
    request: ResendVerificationRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Повторно отправить код верификации

    Если не пришло письмо - используйте этот эндпоинт
    '''
    try:
        use_case = ResendVerificationUseCase(uow_factory)
        return await use_case.execute(request)

    except ValueError as e:
        logger.warning(f'Ошибка при повторной отправке: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f'Критическая ошибка: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Resend failed'
        )


@router.post('/login', response_model=TokenResponse)
async def login(
    request: LoginRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Вход в систему

    Returns access_token и refresh_token.
    Используйте access_token в заголовке Authorization: Bearer <token>
    '''
    try:
        use_case = SignInUseCase(uow_factory)
        return await use_case.execute(request)

    except ValueError as e:
        logger.error(f'Ошибка при входе: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f'Критическая ошибка при входе: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Login failed'
        )


@router.post('/refresh', response_model=TokenResponse)
async def refresh(
    body: dict, uow_factory: UnitOfWorkFactory = Depends(get_uow_factory)
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
            expires_in=15 * 60,
        )

    except ValueError as e:
        logger.error(f'Ошибка при refresh: {str(e)}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


async def logout(
    request: dict,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Выход из системы.

    Body:
    {
        'attorney_id': 123
    }
    '''
    try:
        attorney_id = request.get('attorney_id')

        if not attorney_id:
            raise ValueError('Missing attorney_id')

        auth_service = AuthService(uow_factory)
        await auth_service.logout(int(attorney_id))

        return {'message': 'Logged out successfully'}

    except ValueError as e:
        logger.warning(f'Logout error: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f'Error during logout: {str(e)}', exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Logout failed',
        )
