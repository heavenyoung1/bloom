from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException
from backend.application.commands.client import DeleteClientCommand
from backend.core.logger import logger


class DeleteClientUseCase:
    '''Сценарий: юрист удаляет клиента.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: DeleteClientCommand,
    ) -> bool:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить клиента
                client = await uow.client_repo.get(cmd.client_id)

                if not client:
                    raise EntityNotFoundException(
                        f'Клиент с ID {cmd.client_id} не найден.'
                    )

                # 3. Удалить клиента
                await uow.client_repo.delete(cmd.client_id)

                logger.info(f'Клиент с ID {cmd.client_id} удалён.')
                return True

            except Exception as e:
                logger.error(f'Ошибка при удалении клиента: {e}')
                raise e
