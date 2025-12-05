from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientResponse
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class GetClientByIdUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        '''Получение клиента по ID'''
        self.uow_factory = uow_factory

    async def execute(
        self,
        client_id: int,
        owner_attorney_id: int,  # Для проверки прав доступа
    ) -> ClientResponse:
        async with self.uow_factory as uow:
            try:
                # 1. Получить клиента
                client = await uow.client_repo.get(client_id)

                if not client:
                    logger.error(f'Клиент с ID {client_id} не найден.')
                    raise EntityNotFoundException(f'Клиент с ID {client_id} не найден.')

                logger.info(f'Клиент получен: ID = {client_id}')
                return ClientResponse.model_validate(client)
            except Exception as e:
                logger.error(f'Ошибка при получении клиента с ID {client_id}: {e}')
                raise e
