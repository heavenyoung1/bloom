from sqlmodel import select
from typing import Dict, List, TYPE_CHECKING
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
        
    async def get(self, id: int) -> 'Case':
        try:
            statement = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.exec(statement)
            orm_case = result.first()

            if not orm_case:
                return None
            
            case = CaseMapper.to_domain(orm_case)
            return case
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении ДЕЛА: {str(e)}')
        
    async def get_all(self) -> List['Case']:
        try:
            statement = select(CaseORM)
            result = await self.session.exec(statement)
            orm_cases = result.all()

            if not orm_cases:
                return None
            
            cases = [
                CaseMapper.to_domain(orm_case) for orm_case in orm_cases
            ]
            return cases
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении ДЕЛА: {str(e)}')
        
    async def update(self, updated_case: Case) -> Dict:
        try:
            id = updated_case.id
            statement = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.exec(statement)
            orm_case = result.first()

            if not orm_case:
                raise EntityNotFoundException('Дело не найдено')
            case = CaseMapper.to_domain(orm_case)

            # Обновляем поля дела
            case.name = updated_case.name
            case.client_id = updated_case.client_id
            case.status = updated_case.status
            case.description = updated_case.description
            
            # Преобразуем обновленное дело обратно в ORM модель
            updated_orm_case = CaseMapper.to_orm(case)
            #ТУТ МОЖЕТ БЫТЬ НУЖЕН FLASH

            # Важно: update здесь сохраняет изменения без явного merge и flush
            return {'success': True, 'case': case}
        except Exception as e:
            raise DatabaseErrorException(
                f'Ошибка при обновлении данных ДЕЛА: {str(e)}'
            )
        
    async def update(self, id: int) -> bool:
        try:
            statement = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.exec(statement)
            orm_case = result.first()
            if not orm_case:
                raise EntityNotFoundException('Дело не найдено')
            
            await self.session.delete(orm_case)
            await self.session.flush()  # Фиксируем изменения в транзакции
            return True 
        
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при удалении ДЕЛА: {str(e)}')
        
