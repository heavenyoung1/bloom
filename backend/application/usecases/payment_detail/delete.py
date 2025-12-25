from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.payment_detail import DeletePaymentDetailCommand
from backend.core.logger import logger


class DeletePaymentDetailUseCase:
    '''Сценарий: юрист удаляет платежные реквизиты.'''
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: DeletePaymentDetailCommand,
    ) -> bool:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Удалить платежные реквизиты
                await uow.payment_detail_repo.delete(cmd.payment_detail_id)

                logger.info(
                    f'Платежные реквизиты с ID {cmd.payment_detail_id} удалены.'
                )
                return True

            except Exception as e:
                logger.error(f'Ошибка при удалении платежных реквизитов: {e}')
                raise e
