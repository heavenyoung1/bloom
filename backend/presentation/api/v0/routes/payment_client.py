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
    PaymentClientResponse,
    FullPaymentResponse
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
    response_model=FullPaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создание платежа для клиента',
)
async def create_client_payment(
    request: PaymentClientCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        service = PaymentService(uow_factory)
        result = await service.create_payment(
            attorney_id=current_attorney_id,
            request=request,
        )
        return FullPaymentResponse(**result)
    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Сущность не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при создании платежа: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при создании платежа'
        )

@router.get(
    '/get-client-payment/{payment_id}',
    response_model=PaymentClientResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение платежа',
)
async def get_client_payment(
    payment_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        service = PaymentService(uow_factory)
        result = await service.get_client_payment(payment_id=payment_id)
        return result
    except EntityNotFoundException as e:
        logger.error(f'Платеж не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении платежа: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении платежа'
        )

@router.get(
    '/get-client-payment/attorneys/{attorney_id}',
    response_model=list[PaymentClientResponse],
    status_code=status.HTTP_200_OK,
    summary='Получение всех платежей для юриста',
)
async def get_all_client_payments_for_attorney(
    attorney_id: int,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        service = PaymentService(uow_factory)
        result = await service.get_all_payments_for_attorney(attorney_id=attorney_id)
        return result
    except Exception as e:
        logger.error(f'Ошибка при получении платежей: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении платежей'
        )


@router.put(
    '/update-client-payment/{payment_id}',
    response_model=PaymentClientResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление платежа',
)
async def update_client_payment(
    payment_id: int,
    request: PaymentClientUpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        service = PaymentService(uow_factory)
        result = await service.update_client_payment(
            attorney_id=current_attorney_id,
            payment_id=payment_id,
            request=request,
        )
        return result
    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Платеж не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при обновлении платежа: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении платежа'
        )

@router.delete(
    '/delete-client-payment/{payment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление платежа',
)
async def delete_client_payment(
    payment_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        service = PaymentService(uow_factory)
        await service.delete_payment(payment_id=payment_id)
    except EntityNotFoundException as e:
        logger.error(f'Платеж не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при удалении платежа: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении платежа'
        )
