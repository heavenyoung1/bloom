from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientResponse
from backend.core.exceptions import EntityNotFoundException
from backend.application.commands.client import GetClientByIdQuery
from backend.core.logger import logger


class GetClientByIdUseCase:
    '''Сценарий: юрист получает клиента по его ID.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetClientByIdQuery,
    ) -> ClientResponse:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить клиента
                client = await uow.client_repo.get(cmd.client_id)

                if not client:
                    logger.error(f'Клиент с ID {cmd.client_id} не найден.')
                    raise EntityNotFoundException(
                        f'Клиент с ID {cmd.client_id} не найден.'
                    )

                logger.info(f'Клиент получен: ID = {cmd.client_id}')
                return ClientResponse.model_validate(client)
            except Exception as e:
                logger.error(f'Ошибка при получении клиента с ID {cmd.client_id}: {e}')
                raise e
