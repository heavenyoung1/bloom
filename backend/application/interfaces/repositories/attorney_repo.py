from abc import abstractmethod
from typing import Sequence, Optional

from backend.application.interfaces.repositories.base_repo import IBaseRepository
from backend.domain.entities.attorney import Attorney


class IAttorneyRepository(IBaseRepository[Attorney]):
    '''Специфичный интерфейс для Attorney'''

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional['Attorney']: ...

    @abstractmethod
    async def get_by_license_id(self, license_id: str) -> Optional['Attorney']: ...

    @abstractmethod
    async def get_by_phone(self, phone_number: str) -> Optional['Attorney']: ...
