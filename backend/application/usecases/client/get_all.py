from typing import List

from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientResponse
from backend.core.logger import logger


class GetClientsForAttorneyUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        client_id: int,
        owner_attorney_id: int,  # Для проверки прав доступа
    ) -> List[ClientResponse]:
        async with self.uow_factory as uow:
            try:
                # 1. Получить всех клиентов этого адвоката
                clients = await uow.client_repo.get_all_for_attorney(owner_attorney_id)
                logger.info(
                    f'Получено {len(clients)} клиентов для юриста {owner_attorney_id}'
                )
                return [ClientResponse.model_validate(client) for client in clients]

            except Exception as e:
                logger.error(
                    f'Ошибка при получении клиентов для юриста с ID {owner_attorney_id}: {e}'
                )
                raise e
