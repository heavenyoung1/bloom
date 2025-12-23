from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

from backend.application.usecases.payment_detail import (
    CreatePaymentDetailUseCase,
    GetPaymentDetailForAttorneyUseCase,
    GetPaymentDetailByIdUseCase,
    UpdatePaymentDetailUseCase,
    DeletePaymentDetailUseCase,
)

from backend.application.commands.payment_detail import (
    CreatePaymentDetailtCommand,
    UpdatePaymentDetailCommand,
    DeletePaymentDetailCommand,
    GetPaymentDelatilByIdQuery,
    GetPaymentDetailForAttorneyQuery,
)

from backend.application.dto.details_payment import (
    PaymentCreateRequest,
    PaymentDetailResponse,
)

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
)
from backend.core.logger import logger

router = APIRouter(prefix='/api/v0/payment-detaul', tags=['payment-detail'])

@router.post(
    '/create-payment-detail',
    response_model=PaymentDetailResponse,
    summary='Создание платежной информации',
)
async def create_payment_detail(
    request: PaymentCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    cmd = CreatePaymentDetailtCommand(
        attorney_id=current_attorney_id,
        inn = request.inn,
        index_address=request.index_address,
        address=request.address,
        bank_account=request.bank_account,
        correspondent_account=request.correspondent_account,
        bik=request.bik,
        bank_recipient=request.bank_recipient,
        kpp=request.kpp,
    )
    use_case = CreatePaymentDetailUseCase(uow_factory)
    result = await use_case.execute(cmd)

    logger.info(f'Платежная информация успешно создана: {result.attorney_id}')
    return result