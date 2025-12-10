from typing import List

from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientResponse
from backend.application.commands.client import GetClientsForAttorneyQuery
from backend.core.logger import logger


class GetClientsForAttorneyUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetClientsForAttorneyQuery,
    ) -> List[ClientResponse]:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить всех клиентов этого адвоката
                clients = await uow.client_repo.get_all_for_attorney(
                    cmd.owner_attorney_id
                )
                logger.info(
                    f'Получено {len(clients)} клиентов для юриста {cmd.owner_attorney_id}'
                )
                return [ClientResponse.model_validate(client) for client in clients]

            except Exception as e:
                logger.error(
                    f'Ошибка при получении клиентов для юриста с ID {cmd.owner_attorney_id}: {e}'
                )
                raise e
