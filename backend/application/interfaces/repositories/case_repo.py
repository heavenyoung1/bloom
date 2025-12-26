from abc import abstractmethod
from typing import Sequence, List, Dict, Any

from backend.application.interfaces.repositories.base_repo import IBaseRepository
from backend.domain.entities.case import Case

# Seauence - упорядоченная коллекция элементов, к которым можно обращаться по индексу
# (list, tuple, str, range)


class ICaseRepository(IBaseRepository['Case']):
    '''Специфичный интерфейс для Case'''

    pass

    @abstractmethod
    async def get_all_for_attorney(self, attorney_id: int) -> Sequence['Case']: ...

    @abstractmethod
    async def get_dashboard_data(self, attorney_id: int) -> List[Dict[str, Any]]: ...
