from backend.infrastructure.repositories.interfaces.base_repo import IBaseRepository
from backend.domain.entities.contact import Contact


class IContactRepository(IBaseRepository[Contact]):
    '''Специфичный интерфейс для Contact'''

    pass
