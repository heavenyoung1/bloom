from sqlalchemy.orm import Session

from backend.core import logger
from ..repositories.interfaces import IContactRepository


class ContactRepository(IContactRepository):
    def __init__(self, session: Session):
        self.session = session
