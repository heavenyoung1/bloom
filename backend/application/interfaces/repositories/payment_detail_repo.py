from abc import abstractmethod
from typing import Optional

from backend.application.interfaces.repositories.base_repo import IBaseRepository
from backend.domain.entities.payment_detail import PaymentDetail


class IPaymentDetailRepository(IBaseRepository['PaymentDetail']):
    '''Специфичный интерфейс для PaymentDetail'''

    @abstractmethod
    async def get_for_attorney(self, attorney_id: int) -> Optional['PaymentDetail']: ...

