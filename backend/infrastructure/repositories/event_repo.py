from sqlalchemy.orm import Session

from backend.core import logger
from ..repositories.interfaces import IEventRepository


class EventRepository(IEventRepository):
    def __init__(self, session: Session):
        self.session = session
