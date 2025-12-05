from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException
from backend.core.logger import logger


class DeleteClientUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, client_id: int) -> bool:
        async with self.uow_factory as uow:
            try:
                client = await uow.client_repo.get(client_id)
                if not client:
                    raise EntityNotFoundException(f'Клиент с ID {client_id} не найден.')

                # Удаление клиента
                await uow.client_repo.delete(client_id)

                logger.info(f'Клиент с ID {client_id} удалён.')
                return True

            except Exception as e:
                logger.error(f'Ошибка при удалении клиента: {e}')
                raise e
