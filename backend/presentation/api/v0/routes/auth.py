from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.usecases.auth.sign_in import SignInUseCase
from backend.application.usecases.auth.sign_up import SignUpUseCase
from backend.application.usecases.auth.verify_email import VerifyEmailUseCase
from backend.application.usecases.auth.resend_verification import (
    ResendVerificationUseCase,
)
from backend.application.usecases.auth.forgot_password import ForgotPasswordUseCase
from backend.application.usecases.auth.reset_password import ResetPasswordUseCase
from backend.application.services.token_management_service import TokenManagementService

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
)
from backend.application.usecases.auth.sign_in import SignInUseCase
from backend.application.usecases.auth.sign_out import SignOutUseCase
from backend.application.usecases.auth.refresh_token import RefreshTokenUseCase
from backend.application.usecases.auth.change_password import ChangePasswordUseCase

from backend.application.commands.attorney import (
    RegisterAttorneyCommand,
    LoginAttorneyCommand,
    VerifyEmailCommand,
    ResendVerificationCommand,
    ForgotPasswordCommand,
    ResetPasswordCommand,
    RefreshTokenCommand,
    ChangePasswordCommand,
)

# from backend.application.services.auth_service import AuthService
from backend.core.dependencies import get_current_attorney_id
from backend.core.dependencies import get_uow_factory
from backend.application.dto.attorney import (
    AttorneyResponse,
    AttorneyVerificationResponse,
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    VerifyEmailRequest,
    ResendVerificationRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    PasswordResetResponse,
    RefreshTokenRequest,
    ChangePasswordDTO,
)
from backend.core.logger import logger


router = APIRouter(prefix='/api/v0/auth', tags=['auth'])

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
    3. Сохранение события в Outbox (для асинхронной отправки email)
    
    Отправка email происходит через Outbox воркер (гарантированная доставка).
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
    # UseCase сам сохранит событие в Outbox в той же транзакции
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


# ========== REFRESH TOKEN ==========


@router.post(
    '/refresh',
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление access token',
    responses={
        200: {'description': 'Access token успешно обновлен'},
        400: {'description': 'Невалидный или истёкший refresh token'},
        401: {'description': 'Refresh token не найден'},
    },
)
async def refresh_token(
    request: RefreshTokenRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Обновление access token по refresh token.

    Flow:
    1. Декодирование refresh token
    2. Проверка типа токена (должен быть 'refresh')
    3. Проверка что refresh token существует в Redis
    4. Создание нового access token
    5. Возврат нового access token (refresh token остается прежним)

    Requires:
        - refresh_token в теле запроса
    '''
    logger.info('Попытка обновления access token')

    # 1. Парсим request в Command
    cmd = RefreshTokenCommand(refresh_token=request.refresh_token)

    # 2. Создаем UseCase и выполняем
    use_case = RefreshTokenUseCase(uow_factory)
    result = await use_case.execute(cmd)

    logger.info('Access token успешно обновлен')
    return result


# ========== CHANGE PASSWORD ==========


@router.post(
    '/change-password',
    status_code=status.HTTP_200_OK,
    summary='Изменение пароля',
    responses={
        200: {'description': 'Пароль успешно изменен'},
        400: {'description': 'Неправильный текущий пароль или ошибка валидации'},
        401: {'description': 'Требуется авторизация'},
    },
)
async def change_password(
    request: ChangePasswordDTO,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Изменение пароля адвоката.

    Flow:
    1. Проверка текущего пароля
    2. Валидация нового пароля
    3. Хеширование и сохранение нового пароля

    Requires:
        - Authorization: Bearer <access_token>
    '''
    logger.info(f'Попытка изменения пароля: ID={current_attorney_id}')

    # 1. Парсим request в Command
    cmd = ChangePasswordCommand(
        attorney_id=current_attorney_id,
        old_password=request.current_password,
        new_password=request.new_password,
    )

    # 2. Создаем UseCase и выполняем
    use_case = ChangePasswordUseCase(uow_factory)
    result = await use_case.execute(cmd)

    logger.info(f'Пароль успешно изменен: ID={current_attorney_id}')
    return result


# ========== EMAIL VERIFICATION ==========


@router.post(
    '/verify-email',
    response_model=AttorneyVerificationResponse,
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

@router.post(
    '/forgot-password',
    status_code=status.HTTP_200_OK,
    summary='Отправка кода верификации для сброса пароля ',
    responses={
        200: {'description': 'Код отправлен на email'},
        400: {'description': 'Email не найден'},
    },
)
async def forgot_password(
    request: ForgotPasswordRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    logger.info(f'Отправка кода для сброса пароля: {request.email}')

    # 1. Парсим request в Command
    cmd = ForgotPasswordCommand(email=request.email)

    # 2. Создаем UseCase и выполняем
    token_service = TokenManagementService()
    use_case = ForgotPasswordUseCase(uow_factory, token_service)
    await use_case.execute(cmd)

    logger.info(f'Код отправлен: {request.email}')
    return {'ok': True}

@router.post(
    '/reset-password',
    response_model=PasswordResetResponse,
    status_code=status.HTTP_200_OK,
    summary='Сброс пароля по коду верификации',
    responses={
        200: {'description': 'Пароль успешно сброшен'},
        400: {'description': 'Неверный код или email не найден'},
    },
)
async def reset_password(
    request: ResetPasswordRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    logger.info(f'Сброс пароля для: {request.email}')

    # 1. Парсим request в Command
    cmd = ResetPasswordCommand(
        email=request.email,
        code=request.code,
        new_password=request.new_password
    )

    # 2. Создаем UseCase и выполняем
    token_service = TokenManagementService()
    use_case = ResetPasswordUseCase(uow_factory, token_service)
    result = await use_case.execute(cmd)

    logger.info(f'Пароль сброшен: {request.email}')
    return result