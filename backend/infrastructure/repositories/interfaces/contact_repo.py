from abc import abstractmethod
from typing import Sequence

from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.contact import Contact


class IContactRepository(IBaseRepository['Contact']):
    '''Специфичный интерфейс для Contact'''

    pass

    @abstractmethod
    async def get_all_for_case(self, id: int) -> Sequence['Contact']: ...
