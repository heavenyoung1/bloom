from fastapi import APIRouter, Depends, HTTPException, status
from backend.application.dto.client import ClientCreateRequest, ClientResponse
from backend.application.services.client_service import ClientService
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.dependencies import get_uow_factory
from backend.core.dependencies import get_current_attorney
from backend.core.logger import logger

router = APIRouter(prefix='/api/v1/clients', tags=['clients'])


@router.post(
    '',
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_client(
    request: ClientCreateRequest,
    uow_factory: UnitOfWorkFactory = Depends(get_uow_factory),
    current_attorney: dict = Depends(get_current_attorney),  # Получаем текущего юриста
    client_service: ClientService = Depends(),  # Внедряем сервис
) -> 'ClientResponse':
    '''Создание клиента'''
    try:
        # Передаем данные в сервис и получаем результат
        return await client_service.create_client(
            request, current_attorney['sub']
        )  # Извлекаем ID из токена
    except Exception as e:
        # Логируем и пробрасываем ошибку
        logger.error(f'Ошибка при создании клиента: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
