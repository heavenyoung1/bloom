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

from backend.application.commands.payment_detail import CreatePaymentDetailtCommand

class CreatePaymentDetailUseCase:
    '''Сценарий: юрист создаёт новое дело.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: CreatePaymentDetailtCommand,
    ) -> 'PaymentDetailResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 2. Создание Entity
                case = Case.create(
                    name=cmd.name,
                    client_id=cmd.client_id,
                    attorney_id=cmd.attorney_id,
                    status=cmd.status,  # Статус будет передан из команды
                    description=cmd.description,
                )

                # 3. Сохранение в базе
                saved_case = await uow.case_repo.save(case)

                logger.info(
                    f'Дело создано: ID = {saved_case.id} '
                    f'Владелец = {saved_case.attorney_id} '
                    f'Связанный клиент = {saved_case.client_id} '
                )

                # 4. Возврат Response
                return CaseResponse.model_validate(saved_case)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании клиента: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании клиента: {e}')
                raise Exception('Ошибка при создании клиента')