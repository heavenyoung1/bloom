from fastapi import APIRouter, Depends, HTTPException, status
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

from backend.application.usecases.payment_detail import (
    CreatePaymentDetailUseCase,
    GetPaymentDetailForAttorneyUseCase,
    GetPaymentDetailByIdUseCase,
    UpdatePaymentDetailUseCase,
    DeletePaymentDetailUseCase,
)

from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)

from backend.application.commands.payment_detail import (
    CreatePaymentDetailCommand,
    UpdatePaymentDetailCommand,
    DeletePaymentDetailCommand,
    GetPaymentDetailByIdQuery,
    GetPaymentDetailForAttorneyQuery,
)

from backend.application.dto.details_payment import (
    PaymentDetailCreateRequest,
    PaymentDetailUpdateRequest,
    PaymentDetailResponse,
)

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
)
from backend.core.logger import logger

router = APIRouter(prefix='/api/v0/payment-detail', tags=['payment-detail'])

@router.post(
    '/create-payment-detail',
    response_model=PaymentDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создание платежной информации',
)
async def create_payment_detail(
    request: PaymentDetailCreateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        cmd = CreatePaymentDetailCommand(
            attorney_id=current_attorney_id,
            inn=request.inn,
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

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Платежная информация не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при создании платежной информации: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при создании платежной информации',
        )

@router.get(
    '/payment-detail/{payment_detail_id}',
    response_model=PaymentDetailResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение платежной информации',
    responses={
        200: {'description': 'Данные платежной информации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Платежная информация не найдена'},
    },
)
async def get_payment_detail(
    payment_detail_id: int,
    #current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        cmd = GetPaymentDetailByIdQuery(payment_detail_id=payment_detail_id)
        use_case = GetPaymentDetailByIdUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Платежная информация успешно получена: {result.attorney_id}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Платежная информация не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении платежной информации: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении платежной информации',
        )
    
@router.get(
    '/payment-detail/attorneys/{attorney_id}',
    response_model=PaymentDetailResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение платежной информации',
    responses={
        200: {'description': 'Данные платежной информации'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Платежная информация не найдена'},
    },
)
async def get_payment_detail_for_attorney(
    attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        cmd = GetPaymentDetailForAttorneyQuery(attorney_id=attorney_id)
        use_case = GetPaymentDetailForAttorneyUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Платежная информация для юриста успешно получена: {result.attorney_id}')
        return result

    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Платежная информация не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при получении платежной информации: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении платежной информации',
        )

@router.put(
    '/update-payment-detail/{payment_detail_id}',
    response_model=PaymentDetailResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление платежной информации',
)
async def update_payment_detail(
    payment_detail_id: int,
    request: PaymentDetailUpdateRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        # Проверяем, что attorney_id из запроса совпадает с текущим юристом
        if request.attorney_id and request.attorney_id != current_attorney_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Нет прав для обновления платежной информации другого юриста'
            )
        
        cmd = UpdatePaymentDetailCommand(
            payment_detail_id=payment_detail_id,
            attorney_id=current_attorney_id,
            inn=request.inn,
            index_address=request.index_address,
            address=request.address,
            bank_account=request.bank_account,
            correspondent_account=request.correspondent_account,
            bik=request.bik,
            bank_recipient=request.bank_recipient,
            kpp=request.kpp,
        )
        use_case = UpdatePaymentDetailUseCase(uow_factory)
        result = await use_case.execute(cmd)

        logger.info(f'Платежная информация успешно обновлена: {result.attorney_id}')
        return result
    except ValidationException as e:
        logger.error(f'Ошибка валидации: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        logger.error(f'Платежная информация не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при обновлении платежной информации: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при обновлении платежной информации',
        )

@router.delete(
    '/delete-payment-detail/{payment_detail_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление платежной информации',
    responses={
        204: {'description': 'Платежная информация успешно удалена'},
        401: {'description': 'Требуется авторизация'},
        404: {'description': 'Платежная информация не найдена'},
    },
)
async def delete_payment_detail(
    payment_detail_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    '''
    Удаление платежной информации.

    Requires:
        - Authorization: Bearer <access_token>
    '''
    try:
        logger.info(f'Удаление платежной информации: ID={payment_detail_id}')

        cmd = DeletePaymentDetailCommand(payment_detail_id=payment_detail_id)
        use_case = DeletePaymentDetailUseCase(uow_factory)
        await use_case.execute(cmd)

        logger.info(f'Платежная информация успешно удалена: ID={payment_detail_id}')

    except EntityNotFoundException as e:
        logger.error(f'Платежная информация не найдена: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f'Ошибка при удалении платежной информации: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при удалении платежной информации',
        )