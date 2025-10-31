from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, TYPE_CHECKING
from backend.domain.entities.case import Case
from backend.infrastructure.mappers import CaseMapper
from backend.infrastructure.models import CaseORM
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException

from ..repositories.interfaces import ICaseRepository

if TYPE_CHECKING:
    from backend.domain.entities.case import Case


class CaseRepository(ICaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, case: Case) -> dict:
