from sqlalchemy.orm import Session

from backend.core import logger
from ..repositories.interfaces import IClientRepository


class ClientRepository(IClientRepository):
    def __init__(self, session: Session):
        self.session = session
