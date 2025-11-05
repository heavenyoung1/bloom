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

    async def save(self, client: Client) -> Dict:
        try:
            statement = select(ClientORM).where(ClientORM.id == client.id)
            result = await self.session.exec(statement)
            client_found = result.first()

            if client_found is None:
                orm_client = ClientMapper.to_orm(domain=client)
                self.session.add(orm_client)
                await self.session.flush()
                return {'success': True, 'id': orm_client.id}
            else:
                return {'success': False, 'id': orm_client.id}

        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при сохранении КЛИЕНТА: {str(e)}')
        
    async def get(self, id: int) -> 'Client':
        try:
            statement = select(ClientORM).whee(ClientORM.id == id)
            result = await self.session.exec(statement)
            orm_client = result.first()

            if not orm_client:
                return None
            
            client = ClientMapper.to_domain(orm_client)
            return client
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении КЛИЕНТА: {str(e)}')