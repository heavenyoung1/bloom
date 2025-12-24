from backend.application.dto.details_payment import PaymentDetailResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.payment_detail import GetPaymentDetailForAttorneyQuery
from backend.core.exceptions import EntityNotFoundException
from backend.core.logger import logger


class GetPaymentDetailForAttorneyUseCase:
    '''Сценарий: получение платежных реквизитов для юриста.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetPaymentDetailForAttorneyQuery,
    ) -> 'PaymentDetailResponse':
        async with self.uow_factory.create() as uow:
            try:
                payment_detail = await uow.payment_detail_repo.get_for_attorney(
                    cmd.attorney_id
                )

                if not payment_detail:
                    logger.error(
                        f'Платежные реквизиты для юриста с ID {cmd.attorney_id} не найдены.'
                    )
                    raise EntityNotFoundException(f'Платежные реквизиты не найдены.')

                logger.info(
                    f'Платежные реквизиты получены для юриста: ID = {cmd.attorney_id}'
                )
                return PaymentDetailResponse.model_validate(payment_detail)
            except Exception as e:
                logger.error(f'Ошибка при получении платежных реквизитов: {e}')
                raise e
