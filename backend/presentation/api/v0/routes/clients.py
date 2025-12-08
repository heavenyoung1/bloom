from fastapi import APIRouter, Depends, HTTPException, status
from backend.application.dto.client import ClientCreateRequest, ClientResponse
from backend.application.services.client_service import ClientService
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.dependencies import get_uow_factory
from backend.core.dependencies import get_current_attorney
from backend.core.logger import logger
from backend.application.commands.client import CreateClientCommand

router = APIRouter(prefix='/api/v0/clients', tags=['clients'])


@router.post(
    '',
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создать нового клиента',
)
async def create_client(
    request: ClientCreateRequest,
    current_attorney: dict = Depends(get_current_attorney),  # Получаем текущего юриста
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
) -> 'ClientResponse':
    '''Создание нового клиента'''
    try:
        # current_attorney_id - это ID текущего юриста, который авторизован
        current_attorney_id = int(current_attorney['sub'])

        cmd = CreateClientCommand(
            name=request.name,
            type=request.type,
            email=request.email,
            phone=request.phone,
            personal_info=request.personal_info,
            address=request.address,
            messenger=request.messenger,
            messenger_handle=request.messenger_handle,
            owner_attorney_id=current_attorney_id,
        )

        client_service = ClientService(uow_factory)
        return await client_service.create_client(cmd)

    except ValueError as e:
        logger.error(f'Ошибка валидации при создании клиента: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f'Критическая ошибка при создании клиента: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Не удалось создать клиента',
        )
