from abc import abstractmethod
from typing import Sequence

from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.client import Client

# Seauence - упорядоченная коллекция элементов, к которым можно обращаться по индексу
# (list, tuple, str, range)

class IClientRepository(IBaseRepository['Client']):
    '''Специфичный интерфейс для Client'''
    pass

    @abstractmethod
    async def get_all_for_attorney(self, attorney_id: int) -> Sequence['Client']:
        ...