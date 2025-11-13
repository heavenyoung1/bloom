from abc import abstractmethod
from typing import Sequence

from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.event import Event

# Seauence - упорядоченная коллекция элементов, к которым можно обращаться по индексу
# (list, tuple, str, range)


class IEventRepository(IBaseRepository['Event']):
    '''Специфичный интерфейс для Event'''

    pass

    @abstractmethod
    async def get_for_case(self, case_id: int) -> Sequence['Event']: ...

    @abstractmethod
    async def get_all_for_attorney(self, attorney_id: int) -> Sequence['Event']: ...
