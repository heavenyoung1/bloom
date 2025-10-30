from sqlalchemy.orm import Session

from backend.core import logger
from ..repositories.interfaces import IDocunentRepository


class DocumentRepository(IDocunentRepository):
    def __init__(self, session: Session):
        self.session = session
