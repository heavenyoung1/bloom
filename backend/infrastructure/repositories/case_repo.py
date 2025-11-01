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
        try:
            statement = select(CaseORM).where(CaseORM.id == case.id)
            result = await self.session.exec(statement)
            case_found = result.first()

            if case_found is None:
                orm_case = CaseMapper.to_orm(domain=case)
                self.session.add(orm_case)
                await self.session.flush()
                return {'success': True, 'id': orm_case.id}
            else:
                return {'success': False, 'id': orm_case.id}
        except IntegrityError as e:
            # Ловим ошибку попытки сохранения неуникальных данных
            # ТУТ БУДЕТ ДРУГАЯ ОШИБКА
            if 'attorneys_attorney_id_key' in str(e):
                return {'success': False, 'id': None}
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при сохранении ДЕЛА: {str(e)}')
        
    # async def get(self, id: int) -> 'Case':
    #     try:
    #         statement = select(CaseORM).where(CaseORM.id == id)
    #         result = await self.session.exec(statement)
    #         caseorm = result.first()
