from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.client import Client


class IClientRepository(IBaseRepository[Client]):
    '''Специфичный интерфейс для Client'''

    pass
