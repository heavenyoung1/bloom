from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client_payment import PaymentResponse
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.application.commands.case import GetCaseByIdQuery
from backend.core.logger import logger


class GetPaymentByIdUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        '''Получение платежа по ID'''
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetCaseByIdQuery,
    ) -> 'PaymentResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело
                payment = await uow.payment_repo.get(cmd.case_id)

                if not payment:
                    logger.error(f'Дело с ID {cmd.case_id} не найдено.')
                    raise EntityNotFoundException(f'Дело не найдено.')

                logger.info(f'Дело получено: ID = {cmd.case_id}')
                return PaymentResponse.model_validate(payment)
            except Exception as e:
                logger.error(f'Ошибка при получении дела: {e}')
                raise e