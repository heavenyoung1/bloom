from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

from backend.application.services.payment_service import PaymentService
from backend.application.interfaces.repositories.local_storage import IFileStorage

from backend.application.usecases.payment_client import (
    CreatePaymentUseCase,
    DeletePaymentUseCase,
    UpdatePaymentUseCase,
    ChangeStatusPaymentUseCase,
    GetPaymentByIdUseCase,
    GetAllPaymentsUseCase,
)

from backend.application.commands.client_payment import (
    CreateClientPaymentCommand,
    UpdateСlientPaymentCommand,
    DeleteСlientPaymentCommand,
    GetСlientPaymentByIdQuery,
    GetСlientPaymentForAttorneyQuery,
    GetСlientPaymentForClientQuery,
    ChangeClientPaymentStatusCommand,
)

from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)

from backend.application.dto.client_payment import (
    PaymentClientCreateRequest,
    PaymentClientUpdateRequest,
    PaymentClientResponse,
    FullPaymentResponse,
    PaymentClientChangeStatusRequest,
)

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
    get_file_storage,
)

from backend.core.logger import logger

router = APIRouter(prefix='/api/v0', tags=['client_payment'])


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
    file_storage: IFileStorage = Depends(get_file_storage),
):
    try:
        service = PaymentService(uow_factory, file_storage)
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
            detail='Ошибка при создании платежа',
        )


@router.get(
    '/get-client-payment/{payment_id}',
    response_model=PaymentClientResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение платежа',
)
async def get_client_payment(
    payment_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
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
            detail='Ошибка при получении платежа',
        )


@router.get(
    '/get-client-payment/attorneys/{attorney_id}',
    response_model=list[PaymentClientResponse],
    status_code=status.HTTP_200_OK,
    summary='Получение всех платежей для юриста',
)
async def get_all_client_payments_for_attorney(
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        service = PaymentService(uow_factory)
        result = await service.get_all_payments_for_attorney(attorney_id=get_current_attorney_id)
        return result
    except Exception as e:
        logger.error(f'Ошибка при получении платежей: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении платежей',
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
            detail='Ошибка при обновлении платежа',
        )

@router.put(
    '/change-status-client-payment/{payment_id}',
    response_model=PaymentClientResponse,
    status_code=status.HTTP_200_OK,
    summary='Изменение статуса платежа',
)
async def change_status_client_payment(
    payment_id: int,
    request: PaymentClientChangeStatusRequest,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
):
    try:
        cmd = ChangeClientPaymentStatusCommand(
            payment_id=payment_id,
            status=request.status,
        )
        use_case = ChangeStatusPaymentUseCase(uow_factory)
        result = await use_case.execute(cmd)
        
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
            detail='Ошибка при обновлении платежа',
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
            detail='Ошибка при удалении платежа',
        )


@router.get(
    '/download-payment-pdf/{payment_id}',
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    summary='Скачивание PDF документа платежа',
)
async def download_payment_pdf(
    payment_id: int,
    current_attorney_id: int = Depends(get_current_attorney_id),
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
    file_storage: IFileStorage = Depends(get_file_storage),
):
    '''
    Скачивание PDF документа для платежа.
    PDF должен быть сгенерирован при создании платежа.
    '''
    try:
        # Получаем информацию о платеже
        service = PaymentService(uow_factory, file_storage)
        payment = await service.get_client_payment(payment_id)

        # Проверяем, что платеж принадлежит текущему юристу
        if payment.attorney_id != current_attorney_id:
            raise AccessDeniedException('Нет доступа к этому платежу')

        # Стандартный путь к PDF файлу
        pdf_path = f'payments/{payment_id}/invoice_{payment_id}.pdf'

        try:
            # Пытаемся прочитать файл из хранилища
            pdf_bytes = await file_storage.get_file(pdf_path)
        except FileNotFoundError:
            # Если файл не найден, пытаемся сгенерировать его заново
            logger.info(
                f'PDF файл не найден, генерируем заново для платежа {payment_id}'
            )

            async with uow_factory.create() as uow:
                # Получаем entity объекты
                payment_entity = await uow.payment_repo.get(payment_id)
                payment_detail_entity = await uow.payment_detail_repo.get_for_attorney(
                    current_attorney_id
                )

                if not payment_entity or not payment_detail_entity:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Не удалось получить данные для генерации PDF',
                    )

                # Создаем генератор PDF
                from backend.infrastructure.pdf.pdf_generator import PDFGenerator

                pdf_generator = PDFGenerator()

                # Генерируем PDF
                pdf_bytes = pdf_generator.fill_invoice_template(
                    payment=payment_entity, payment_detail=payment_detail_entity
                )

                # Сохраняем PDF
                pdf_path = await file_storage.save_file(
                    file_path=pdf_path, file_content=pdf_bytes
                )

        # Возвращаем файл
        from pathlib import Path
        import tempfile

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_file_path = tmp_file.name

        return FileResponse(
            path=tmp_file_path,
            filename=f'invoice_{payment_id}.pdf',
            media_type='application/pdf',
            background=lambda: Path(
                tmp_file_path
            ).unlink(),  # Удаляем временный файл после отправки
        )

    except EntityNotFoundException as e:
        logger.error(f'Платеж не найден: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccessDeniedException as e:
        logger.error(f'Доступ запрещен: {e}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except FileNotFoundError as e:
        logger.error(f'PDF файл не найден: {e}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='PDF документ не найден'
        )
    except Exception as e:
        logger.error(f'Ошибка при скачивании PDF: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при скачивании PDF документа',
        )
