from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.client_payment import (
    GetPaymentsForAttorneyQuery,
)
from backend.domain.entities.payment import ClientPayment
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger

from backend.application.dto.client_payment import (
    PaymentResponse,
)

from typing import Optional, List



class GetlAllPaymentsUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetPaymentsForAttorneyQuery,
    ) -> List['PaymentResponse']:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить все дела для указанного юриста
                cases = await uow.payment_repo.get_all_for_attorney(cmd.attorney_id)

                # Проверка, что дела существуют
                if not cases:
                    logger.warning(f'Нет дел для юриста с ID {cmd.attorney_id}')
                    raise EntityNotFoundException(
                        f'Нет дел для юриста с ID {cmd.attorney_id}'
                    )

                logger.info(f'Получено {len(cases)} дел для юриста {cmd.attorney_id}')
                # 2. Возвращаем список дел в нужном формате (через модель CaseResponse)
                case_responses = [
                    CaseResponse(
                        id=case.id,
                        name=case.name,
                        client_id=case.client_id,  # Здесь должны быть данные клиента
                        attorney_id=case.attorney_id,  # Здесь должны быть данные адвоката
                        status=case.status,
                        description=case.description,
                        created_at=case.created_at,
                        updated_at=case.updated_at,
                    )
                    for case in cases
                ]

                logger.info(
                    f'Получено {len(cases)} дел для юриста с ID {cmd.attorney_id}'
                )
                return case_responses

            except Exception as e:
                logger.error(
                    f'Ошибка при получении дел для юриста с ID {cmd.attorney_id}: {e}'
                )
                raise e