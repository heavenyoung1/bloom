from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.client_payment import (
    CreateClientPaymentCommand,
)
from backend.domain.entities.client_payment import ClientPayment
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger

from backend.application.dto.client_payment import (
    PaymentClientCreateRequest,
    PaymentClientResponse,
)

class CreatePaymentUseCase:
    '''Сценарий: юрист создаёт платежный документ.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: CreateClientPaymentCommand,
    ) -> 'PaymentClientResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 2. Создание Entity
                payment = ClientPayment.create(
                    name=cmd.name,
                    client_id=cmd.client_id,
                    attorney_id=cmd.attorney_id,
                    paid=cmd.paid,
                    paid_str=cmd.paid_str,
                    pade_date=cmd.pade_date,
                    paid_deadline=cmd.paid_deadline,
                    status=cmd.status,
                    taxable=cmd.taxable,
                    condition=cmd.condition,
                )
                # 3. Сохранение в базе
                saved_payment = await uow.payment_repo.save(payment)

                logger.info(
                    f'Платеж создан: ID = {saved_payment.id} '
                    f'Владелец = {saved_payment.attorney_id} '
                    f'Клиент = {saved_payment.client_id} '
                )

                # 4. Возврат Response
                return PaymentClientResponse.model_validate(saved_payment)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании платежа: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании платежа: {e}')
                raise Exception('Ошибка при создании платежа')