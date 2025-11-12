from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.event import Event


class IEventRepository(IBaseRepository[Event]):
    '''Специфичный интерфейс для Event'''

    pass
