from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.attorney import Attorney


class IAttorneyRepository(IBaseRepository[Attorney]):
    '''Специфичный интерфейс для Attorney'''

    pass
