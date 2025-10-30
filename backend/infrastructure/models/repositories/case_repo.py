from sqlalchemy.orm import Session

from backend.core import logger
from ..repositories.interfaces import ICaseRepository

class CaseRepository(ICaseRepository):
    def __init__(self, session: Session):
        self.session = session