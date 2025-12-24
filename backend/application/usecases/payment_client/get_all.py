from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.client_payment import (
    GetСlientPaymentForAttorneyQuery,
)
from backend.core.exceptions import EntityNotFoundException
from backend.core.logger import logger

from backend.application.dto.client_payment import (
    PaymentClientResponse,
)

from typing import List


class GetAllPaymentsUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetСlientPaymentForAttorneyQuery,
    ) -> List['PaymentClientResponse']:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить все платежи для указанного юриста
                payments = await uow.payment_repo.get_all_for_attorney(cmd.attorney_id)

                # Проверка, что платежи существуют
                if not payments:
                    logger.warning(f'Нет платежей для юриста с ID {cmd.attorney_id}')
                    return []

                logger.info(
                    f'Получено {len(payments)} платежей для юриста {cmd.attorney_id}'
                )

                # 2. Возвращаем список платежей в нужном формате
                payment_responses = [
                    PaymentClientResponse.model_validate(payment)
                    for payment in payments
                ]

                logger.info(
                    f'Получено {len(payments)} платежей для юриста с ID {cmd.attorney_id}'
                )
                return payment_responses

            except Exception as e:
                logger.error(
                    f'Ошибка при получении платежей для юриста с ID {cmd.attorney_id}: {e}'
                )
                raise e
