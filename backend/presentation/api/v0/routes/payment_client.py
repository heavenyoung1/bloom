from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

from backend.application.services.payment_service import PaymentService

from backend.application.usecases.payment_client import (
    CreatePaymentUseCase,
    DeletePaymentUseCase,
    UpdatePaymentUseCase,
    GetPaymentByIdUseCase,
    GetAllPaymentsUseCase,
)

from backend.application.commands.client_payment import (
    CreateClientPaymentCommand,
    UpdateСlientPaymentCommand,
    DeleteСlientPaymentCommand,
    GetСlientPaymentByIdQuery,
    GetСlientPaymentForAttorneyQuery,
    GetСlientPaymentForClientQuery
)

from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)

from backend.application.dto.client_payment import  (
    PaymentClientCreateRequest,
    PaymentClientUpdateRequest,
    PaymentClientResponse
)

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
)

from backend.core.logger import logger

router = APIRouter(prefix='/api/v0/client_payment', tags=['client_payment'])

@router.post(
    '/create-client-payment',
    response_model=PaymentClientResponse, #ТУТ БУДЕТ DTO СУЩНОСТЬ ПОЛНОСТЬЮ ОПИСЫВАЩАЯ ВСЕ ПОЛЯ ИЗ ВОЗВРАТ
    status_code=status.HTTP_200_OK,
    summary='Создание платежа для клиента',
)
async def create_client_payment(
    request: PaymentClientCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        service = PaymentService(uow_factory)
        result = service.create_payment(
            attorney_id=current_attorney_id,
            request=request,
        )
    except:
        # КАКАЯ ТУТ ОШИБКА БУДЕТ?
        pass

@router.get(
    '/get-client-payment/{payment_id}',
    response_model=PaymentClientResponse, #ТУТ БУДЕТ DTO СУЩНОСТЬ ПОЛНОСТЬЮ ОПИСЫВАЩАЯ ВСЕ ПОЛЯ ИЗ ВОЗВРАТ
    status_code=status.HTTP_200_OK,
    summary='Получение платежа',
)
async def get_client_payment(
    payment_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    service = PaymentService(uow_factory)
    service.get_client_payment(payment_id=payment_id)

@router.get(
    '/get-client-payment/attorneys/{attorney_id}',
    response_model=PaymentClientResponse, #ТУТ БУДЕТ DTO СУЩНОСТЬ ПОЛНОСТЬЮ ОПИСЫВАЩАЯ ВСЕ ПОЛЯ ИЗ ВОЗВРАТ
    status_code=status.HTTP_200_OK,
    summary='Получение платежа',
)
async def get_all_client_payments_for_attorney(
    attorney_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    service = PaymentService(uow_factory)
    service.get_all_payments_for_attorney(attorney_id=attorney_id)


@router.put(
    '/update-client-payment/{payment_id}',
    response_model=PaymentClientResponse, #ТУТ БУДЕТ DTO СУЩНОСТЬ ПОЛНОСТЬЮ ОПИСЫВАЩАЯ ВСЕ ПОЛЯ ИЗ ВОЗВРАТ
    status_code=status.HTTP_200_OK,
    summary='Обновление платежа',
)
async def update_client_payment(
    payment_id: int,
    request: PaymentClientUpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    service = PaymentService(uow_factory)
    service.update_client_payment(payment_id=payment_id)
