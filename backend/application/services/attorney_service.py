from backend.infrastructure.uow import AsyncUnitOfWork
from backend.application.dto.attorney import (
    CreateAttorneyDTO,
    UpdateAttorneyDTO,
    AttorneyResponseDTO,
    AttorneyListItemDTO,
)
from backend.domain.entities.attorney import Attorney
from backend.core.exceptions import EntityNotFoundException, ValidationException
from backend.core.logger import logger
import hashlib


class AttorneyService:
    '''Service для работы с юристами'''
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def create_attorney(self, data: CreateAttorneyDTO) -> 'AttorneyResponseDTO':
        '''Создать юриста'''
        