from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.case import Case


class ICaseRepository(IBaseRepository[Case]):
    '''Специфичный интерфейс для Case'''

    pass
