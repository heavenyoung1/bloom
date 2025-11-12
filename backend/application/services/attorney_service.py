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
