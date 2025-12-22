from abc import abstractmethod
from typing import Sequence

from backend.application.interfaces.repositories.base_repo import IBaseRepository
from backend.domain.entities.payment import ClientPayment


class IPaymentRepository(IBaseRepository['ClientPayment']):
    '''Специфичный интерфейс для ClientPayment'''

    @abstractmethod
    async def get_all_for_attorney(self, attorney_id: int) -> Sequence['ClientPayment']: ...

