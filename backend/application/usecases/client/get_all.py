from typing import List

from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientResponse
from backend.core.logger import logger


class GetClientsForAttorneyUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, attorney_id: int) -> List[ClientResponse]:
        async with self.uow_factory as uow:
            try:
                clients = await uow.client_repo.get_all_for_attorney(attorney_id)
                return [ClientResponse.model_validate(client) for client in clients]

            except Exception as e:
                logger.error(
                    f'Ошибка при получении клиентов для юриста с ID {attorney_id}: {e}'
                )
                raise e
