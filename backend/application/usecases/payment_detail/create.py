from backend.application.dto.details_payment import PaymentDetailResponse
from backend.domain.entities.payment_detail import PaymentDetail
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.payment_detail import CreatePaymentDetailtCommand
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class CreatePaymentDetailUseCase:
    '''Сценарий: юрист создаёт платежные реквизиты.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: CreatePaymentDetailtCommand,
    ) -> 'PaymentDetailResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 2. Создание Entity
                payment_detail = PaymentDetail.create(
                    attorney_id=cmd.attorney_id,
                    inn=cmd.inn,
                    kpp=cmd.kpp,
                    index_address=cmd.index_address,
                    address=cmd.address,
                    bank_account=cmd.bank_account,
                    correspondent_account=cmd.correspondent_account,
                    bik=cmd.bik,
                    bank_recipient=cmd.bank_recipient,
                )

                # 3. Сохранение в базе
                saved_payment_detail = await uow.payment_detail_repo.save(payment_detail)

                logger.info(
                    f'Платежные реквизиты созданы: ID = {saved_payment_detail.id} '
                    f'Владелец = {saved_payment_detail.attorney_id} '
                )

                # 4. Возврат Response
                return PaymentDetailResponse.model_validate(saved_payment_detail)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании платежных реквизитов: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании платежных реквизитов: {e}')
                raise Exception('Ошибка при создании платежных реквизитов')