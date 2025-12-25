from backend.application.dto.details_payment import PaymentDetailResponse
from backend.domain.entities.payment_detail import PaymentDetail
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.payment_detail import UpdatePaymentDetailCommand
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class UpdatePaymentDetailUseCase:
    '''Сценарий: обновление платежных реквизитов.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: UpdatePaymentDetailCommand,
    ) -> 'PaymentDetailResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить платежные реквизиты
                payment_detail = await uow.payment_detail_repo.get(
                    cmd.payment_detail_id
                )
                if not payment_detail:
                    logger.warning(
                        f'Платежные реквизиты не найдены: ID = {cmd.payment_detail_id}'
                    )
                    raise EntityNotFoundException(
                        f'Платежные реквизиты не найдены: ID = {cmd.payment_detail_id}'
                    )

                # 2. Применяем изменения через метод update доменной сущности
                payment_detail.update(cmd)

                # 3. Сохранение в базе
                updated_payment_detail = await uow.payment_detail_repo.update(
                    payment_detail
                )

                logger.info(
                    f'Платежные реквизиты обновлены: ID = {updated_payment_detail.id} '
                    f'Владелец = {updated_payment_detail.attorney_id} '
                )

                # 4. Возврат Response
                return PaymentDetailResponse.model_validate(updated_payment_detail)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при обновлении платежных реквизитов: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(
                    f'Неизвестная ошибка при обновлении платежных реквизитов: {e}'
                )
                raise Exception('Ошибка при обновлении платежных реквизитов')
