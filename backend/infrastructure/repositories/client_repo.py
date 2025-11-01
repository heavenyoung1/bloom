from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, List, TYPE_CHECKING

from backend.domain.entities.client import Client
from backend.infrastructure.mappers import ClientMapper
from backend.infrastructure.models import ClientORM
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.infrastructure.repositories.interfaces import IClientRepository


class ClientRepository(IClientRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, client: Client) -> dict:
        try:
            statement = select(ClientORM).where(ClientORM.id == client.id)
            result = await self.session.exec(statement)
            client_found = result.first

        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при сохранении КЛИЕНТА: {str(e)}')
