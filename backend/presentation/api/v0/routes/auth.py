from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.usecases.auth.sign_in import SignInUseCase
from backend.application.usecases.auth.sign_up import SignUpUseCase
from backend.application.usecases.auth.verify_email import VerifyEmailUseCase
from backend.application.usecases.auth.resend_verification import (
    ResendVerificationUseCase,
)

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
)
from backend.application.usecases.auth.sign_in import SignInUseCase
from backend.application.usecases.auth.sign_out import SignOutUseCase

from backend.application.commands.attorney import (
    RegisterAttorneyCommand,
    LoginAttorneyCommand,
    VerifyEmailCommand,
    ResendVerificationCommand,
)
from backend.application.services.auth_service import AuthService
from backend.core.dependencies import get_current_attorney_id
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

# ========== REGISTRATION ==========


@router.post(
    '/register',
    response_model=AttorneyResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация нового адвоката',
    responses={
        201: {'description': 'Успешная регистрация'},
        400: {'description': 'Email уже занят или ошибка валидации'},
    },
)
async def register(
    request: RegisterRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Регистрация нового адвоката.

    Flow:
    1. Валидация данных
    2. Создание адвоката
    3. Отправка кода верификации на email
    '''
    logger.info(f'Попытка регистрации: {request.email}')

    # 1. Парсим request в Command
    cmd = RegisterAttorneyCommand(
        license_id=request.license_id,
        first_name=request.first_name,
        last_name=request.last_name,
        patronymic=request.patronymic,
        email=request.email,
        phone=request.phone,
        password=request.password,
    )

    # 2. Создаем UseCase и выполняем
    use_case = SignUpUseCase(uow_factory)
    result = await use_case.execute(cmd)

    logger.info(f'Адвокат успешно зарегистрирован: {request.email}')
    return result


# ========== LOGIN ==========


@router.post(
    '/login',
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary='Вход в систему',
    responses={
        200: {'description': 'Успешный вход'},
        401: {'description': 'Неправильный email или пароль'},
        429: {'description': 'Слишком много попыток входа'},
    },
)
async def login(
    request: LoginRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Вход в систему (получение access и refresh токенов).

    Flow:
    1. Проверка rate limit
    2. Получение адвоката по email
    3. Проверка пароля
    4. Создание tokens
    5. Сохранение refresh token в Redis
    '''
    logger.info(f'Попытка входа: {request.email}')

    # 1. Парсим request в Command
    cmd = LoginAttorneyCommand(
        email=request.email,
        password=request.password,
    )

    # 2. Создаем UseCase и выполняем
    use_case = SignInUseCase(uow_factory)
    result = await use_case.execute(cmd)

    logger.info(f'Успешный вход: {request.email}')
    return result


# ========== LOGOUT ==========


@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    summary='Выход из системы',
    responses={
        200: {'description': 'Успешный выход'},
        401: {'description': 'Требуется авторизация'},
    },
)
async def logout(
    current_attorney_id: int = Depends(get_current_attorney_id),
    access_token: str = Depends(get_current_access_token),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Выход из системы.

    Flow:
    1. Добавить access token в чёрный список
    2. Удалить refresh token из Redis
    3. Залогировать выход

    Requires:
        - Authorization: Bearer <access_token>
    '''
    logger.info(f'Выход из системы: ID={current_attorney_id}')

    # Создаем UseCase и выполняем
    use_case = SignOutUseCase(uow_factory)
    result = await use_case.execute(current_attorney_id, access_token)

    logger.info(f'Успешный выход: ID={current_attorney_id}')
    return result


# ========== EMAIL VERIFICATION ==========


@router.post(
    '/verify-email',
    response_model=AttorneyResponse,
    status_code=status.HTTP_200_OK,
    summary='Верификация email',
    responses={
        200: {'description': 'Email успешно верифицирован'},
        400: {'description': 'Неправильный или истёкший код'},
    },
)
async def verify_email(
    request: VerifyEmailRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Верификация email по коду.

    Flow:
    1. Проверка кода верификации
    2. Пометить email как верифицированный
    3. Очистить код из Redis
    '''
    logger.info(f'Попытка верификации email: {request.email}')

    # 1. Парсим request в Command
    cmd = VerifyEmailCommand(
        email=request.email,
        code=request.code,
    )

    # 2. Создаем UseCase и выполняем
    use_case = VerifyEmailUseCase(uow_factory)
    result = await use_case.execute(cmd)

    logger.info(f'Email успешно верифицирован: {request.email}')
    return result


# ========== RESEND VERIFICATION ==========


@router.post(
    '/resend-verification',
    status_code=status.HTTP_200_OK,
    summary='Повторная отправка кода верификации',
    responses={
        200: {'description': 'Код отправлен на email'},
        400: {'description': 'Email не найден или уже верифицирован'},
    },
)
async def resend_verification(
    request: ResendVerificationRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Повторно отправить код верификации на email.

    Flow:
    1. Проверка существования адвоката
    2. Проверка что email не верифицирован
    3. Отправка нового кода
    '''
    logger.info(f'Повторная отправка кода: {request.email}')

    # 1. Парсим request в Command
    cmd = ResendVerificationCommand(email=request.email)

    # 2. Создаем UseCase и выполняем
    use_case = ResendVerificationUseCase(uow_factory)
    result = await use_case.execute(cmd)

    logger.info(f'Код повторно отправлен: {request.email}')
    return result
