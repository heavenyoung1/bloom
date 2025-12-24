from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.application.commands.client_payment import DeleteСlientPaymentCommand
from backend.core.logger import logger


class DeletePaymentUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: DeleteСlientPaymentCommand,
    ) -> bool:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидация (проверка уникальности, существования адвоката)
                # ПОТОМ!!!

                # 3. Удалить дело
                await uow.payment_repo.delete(cmd.payment_id)

                logger.info(f'Платеж с ID {cmd.payment_id} удален.')
                return True

            except Exception as e:
                logger.error(f'Ошибка при удалении: {e}')
                raise e
