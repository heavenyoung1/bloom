from backend.application.dto.details_payment import (
    PaymentCreateRequest, 
    PaymentDetailResponse,
    )
from backend.application.dto.details_payment import PaymentDetailResponse
from backend.domain.entities.payment_detail import PaymentDetail
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.payment_detail import GetPaymentDelatilByIdQuery
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger

from backend.application.commands.payment_detail import GetPaymentDelatilByIdQuery

class CreatePaymentUseCase:
    '''Сценарий: юрист создаёт новое дело.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetPaymentDelatilByIdQuery
    ):
        try:
            async with self.uow_factory.create() as uow:
                payment_detail = await uow.payment_detail_repo.get(cmd.payment_detail_id)

                if not payment_detail:
                        logger.error(f'Дело с ID {cmd.case_id} не найдено.')
                        raise EntityNotFoundException(f'Дело не найдено.')

                logger.info(f'Дело получено: ID = {cmd.case_id}')
                return PaymentDetailResponse.model_validate(payment_detail)
        except Exception as e:
            logger.error(f'Ошибка при получении дела: {e}')
            raise e
