from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

from backend.application.usecases.payment_detail import (
    CreatePaymentDetailUseCase,
    GetPaymentDetailForAttorneyUseCase,
    GetPaymentDetailByIdUseCase,
    UpdatePaymentDetailUseCase,
    DeletePaymentDetailUseCase,
)

from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)

from backend.application.commands.payment_detail import (
    CreatePaymentDetailtCommand,
    UpdatePaymentDetailCommand,
    DeletePaymentDetailCommand,
    GetPaymentDelatilByIdQuery,
    GetPaymentDetailForAttorneyQuery,
)

from backend.application.dto.details_payment import (
    PaymentDetailCreateRequest,
    PaymentDetailUpdateRequest,
    PaymentDetailResponse,
)

from backend.core.dependencies import (
    get_uow_factory,
    get_current_attorney_id,
    get_current_access_token,
)

from backend.application.usecases.payment_client import (
    CreatePaymentUseCase,
    DeletePaymentUseCase,
    UpdatePaymentUseCase,
    GetPaymentByIdUseCase,
    GetAllPaymentsUseCase,
)

from backend.application.commands.client_payment import (
    CreateClientPaymentCommand,
    UpdateСlientPaymentCommand,
    DeleteСlientPaymentCommand,
    GetСlientPaymentByIdQuery,
    GetСlientPaymentForAttorneyQuery,
    GetСlientPaymentForClientQuery
)

from backend.core.exceptions import (
    ValidationException,
    EntityNotFoundException,
    AccessDeniedException,
)

from backend.application.dto.client_payment import  (
    PaymentClientCreateRequest,
    PaymentClientUpdateRequest,
    PaymentClientResponse
)


from backend.core.logger import logger




class PaymentService:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        # Инициализируем нужные UseCases
        self.uow_factory = uow_factory
        self.get_attorney_payment_data_use_case = GetPaymentDetailForAttorneyUseCase(uow_factory)
        self.create_client_payment_use_case = CreatePaymentUseCase(uow_factory)
        self.get_client_payment_use_case = GetPaymentByIdUseCase(uow_factory)
        self.get_all_payments_for_attorney_use_case = GetAllPaymentsUseCase(uow_factory)
        self.update_client_payment_use_case = UpdatePaymentUseCase(uow_factory)
        self.delete_payment_use_case = DeletePaymentUseCase(uow_factory)
        
    async def create_payment(
            self,
            attorney_id: int,
            request: PaymentClientCreateRequest,
    ):
        # Вызываем команду для получения платежных данных юриста
        get_attorney_payment_data_cmd = GetPaymentDetailForAttorneyQuery(
            attorney_id
        )
        # Вызываем UseCase для получения платежных данных юриста
        attorney_payment_data = await self.get_attorney_payment_data_use_case.execute(
            get_attorney_payment_data_cmd
        )
        # Вызываем команду для создания платежа на основании полученных данных
        create_client_payment_cmd = CreateClientPaymentCommand(
            name=request.name,
            client_id=request.client_id,
            attorney_id=attorney_id,
            paid=request.paid,
            paid_str=request.paid_str,
            pade_date=request.pade_date,
            paid_deadline=request.paid_deadline,
            status=request.status,
            taxable=request.taxable,
            condition=request.condition,
        )
        payment_data = await self.create_client_payment_use_case.execute(
            create_client_payment_cmd
        )
        full_payment_data = {
            'payment_id': payment_data.id,
            'payment_name': payment_data.name,
            'client_id': payment_data.client_id,
            'attorney_id': payment_data.attorney_id,
            'paid': payment_data.paid,
            'paid_str': payment_data.paid_str,
            'pade_date': payment_data.pade_date,
            'paid_deadline': payment_data.paid_deadline,
            'status': payment_data.status,
            'taxable': payment_data.taxable,
            'condition': payment_data.condition,
            'inn': attorney_payment_data.inn,
            'kpp': attorney_payment_data.kpp,
            'index_address': attorney_payment_data.index_address,
            'address': attorney_payment_data.address,
            'bank_account': attorney_payment_data.bank_account,
            'corr_account': attorney_payment_data.correspondent_account,
            'bik': attorney_payment_data.bik,
            'bank_recipient': attorney_payment_data.bank_recipient,
        }
        return full_payment_data

    async def get_client_payment(self, payment_id: int):
        get_payment_cmd = GetСlientPaymentByIdQuery(
            payment_id=payment_id
            )
        result = await self.get_client_payment_use_case.execute(
            get_payment_cmd
            )
        return result
    
    async def get_all_payments_for_attorney(self, attorney_id: int):
        get_all_payments_for_attorney_cmd = GetСlientPaymentForAttorneyQuery(
            attorney_id=attorney_id,
            )
        result = await self.get_all_payments_for_attorney_use_case.execute(
            get_all_payments_for_attorney_cmd,
            )
        return result
    


    async def update_client_payment(
            self,
            attorney_id: int,
            payment_id: int,
            request: PaymentClientUpdateRequest,
    ):
        update_payment_data_cmd = UpdateСlientPaymentCommand(
            payment_id=payment_id,
            name=request.name,
            client_id=request.client_id,
            attorney_id=attorney_id,
            paid=request.paid,
            paid_str=request.paid_str,
            pade_date=request.pade_date,
            paid_deadline=request.paid_deadline,
            status=request.status,
            taxable=request.taxable,
            condition=request.condition,
        )
        result = await self.update_client_payment_use_case.execute(update_payment_data_cmd)
        return result
    
    async def delete_payment(
        self,
        payment_id: int,
    ):
        delete_payment_cmd = DeleteСlientPaymentCommand(
            payment_id=payment_id,
        )
        result = await self.delete_payment_use_case.execute(
            delete_payment_cmd
        )
        return result

