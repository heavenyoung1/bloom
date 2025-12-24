from backend.application.dto.client_payment import PaymentClientResponse
from backend.domain.entities.client_payment import ClientPayment
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.client_payment import UpdateСlientPaymentCommand
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class UpdatePaymentUseCase:
    '''Сценарий: обновление платежа.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: UpdateСlientPaymentCommand,
    ) -> 'PaymentClientResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить платеж
                payment = await uow.payment_repo.get(cmd.payment_id)
                if not payment:
                    logger.warning(f'Платеж не найден: ID = {cmd.payment_id}')
                    raise EntityNotFoundException(
                        f'Платеж не найден: ID = {cmd.payment_id}'
                    )

                # 2. Применяем изменения через метод update доменной сущности
                # Преобразуем UpdateСlientPaymentCommand в UpdatePaymentCommand для доменной сущности
                from backend.application.commands.client_payment import (
                    UpdatePaymentCommand,
                )

                update_cmd = UpdatePaymentCommand(
                    name=cmd.name,
                    client_id=cmd.client_id,
                    attorney_id=cmd.attorney_id,
                    paid=cmd.paid,
                    paid_str=cmd.paid_str,
                    pade_date=cmd.pade_date,
                    paid_deadline=cmd.paid_deadline,  # Уже Optional[date]
                    taxable=cmd.taxable,
                    condition=cmd.condition,
                    status=cmd.status,
                )
                payment.update(update_cmd)

                # 3. Сохранение в базе
                updated_payment = await uow.payment_repo.update(payment)

                logger.info(
                    f'Платеж обновлен: ID = {updated_payment.id} '
                    f'Владелец = {updated_payment.attorney_id} '
                    f'Клиент = {updated_payment.client_id} '
                )

                # 4. Возврат Response
                return PaymentClientResponse.model_validate(updated_payment)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при обновлении платежа: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при обновлении платежа: {e}')
                raise Exception('Ошибка при обновлении платежа')
