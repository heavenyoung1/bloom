from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client_payment import PaymentClientResponse
from backend.core.exceptions import EntityNotFoundException
from backend.application.commands.client_payment import GetСlientPaymentByIdQuery
from backend.core.logger import logger


class GetPaymentByIdUseCase:
    '''Сценарий: юрист получает информацию о платеже по ID.'''
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetСlientPaymentByIdQuery,
    ) -> 'PaymentClientResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить платеж
                payment = await uow.payment_repo.get(cmd.payment_id)

                if not payment:
                    logger.error(f'Платеж с ID {cmd.payment_id} не найден.')
                    raise EntityNotFoundException(f'Платеж не найден.')

                logger.info(f'Платеж получен: ID = {cmd.payment_id}')
                return PaymentClientResponse.model_validate(payment)
            except Exception as e:
                logger.error(f'Ошибка при получении платежа: {e}')
                raise e
