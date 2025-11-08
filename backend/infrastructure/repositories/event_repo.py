from sqlalchemy.future import select

from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    DataError,
    NoResultFound,
    MultipleResultsFound,
    InvalidRequestError,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, TYPE_CHECKING

from backend.domain.entities.event import Event
from backend.infrastructure.mappers import EventMapper
from backend.infrastructure.models import EventORM
from backend.core.exceptions import (
    DatabaseErrorException,
    EntityNotFoundException,
    EntityAlreadyExistsError,
)

from backend.infrastructure.repositories.interfaces import IEventRepository
from backend.core.logger import logger


class EventRepository(IEventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
