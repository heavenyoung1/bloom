from abc import abstractmethod
from typing import Sequence

from backend.application.interfaces.repositories.base_repo import IBaseRepository
from backend.domain.entities.document import Document


class IDocumentMetadataRepository(IBaseRepository['Document']):
    '''Специфичный интерфейс для Contact'''

    pass

    @abstractmethod
    async def get_all_for_case(self, id: int) -> Sequence['Document']: ...
