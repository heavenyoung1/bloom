from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, TYPE_CHECKING

from backend.domain.entities.case import Case
from backend.infrastructure.mappers import CaseMapper
from backend.infrastructure.models import CaseORM
from backend.core.exceptions import (
    DatabaseErrorException, 
    EntityNotFoundException,
    EntityAlreadyExistsError,
)

from backend.infrastructure.repositories.interfaces import ICaseRepository
from backend.core.logger import logger

if TYPE_CHECKING:
    from backend.domain.entities.case import Case


class CaseRepository(ICaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, case: Case) -> dict:
        try:
            # 1. Проверка существования сущности в БД
            if await self._exists(case.id):
                logger.info(f'Попытка сохранения дубликата ДЕЛА ID - {case.id}')
                raise EntityAlreadyExistsError(f'ДЕЛО с ID {case.id} уже существует')

            # 2. Конвертация доменной сущности в ORM-объект
            orm_case = CaseMapper.to_orm(case)

            # 3. Добавление в сессию
            self.session.add(orm_case)

            # 4. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 5. Обновляем ID в доменном объекте
            case.id = orm_case.id
            logger.info(f'ДЕЛО сохранено с ID - {case.id}')

            return case

        except IntegrityError as e:
            raise DatabaseErrorException(f'Ошибка целостности БД: {str(e)}')
        
        except Exception as e:
            raise DatabaseErrorException(f'Неожиданная ошибка при сохранении: {str(e)}')

    async def get(self, id: int) -> 'Case':
        try:
            stmt = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.execute(stmt)
            orm_case = result.scalars().first()

            if not orm_case:
                return None

            case = CaseMapper.to_domain(orm_case)
            return case
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении ДЕЛА: {str(e)}')

    async def get_all(self) -> List['Case']:
        try:
            stmt = select(CaseORM)
            result = await self.session.execute(stmt)
            orm_cases = result.scalars().all()

            if not orm_cases:
                return None

            cases = [CaseMapper.to_domain(orm_case) for orm_case in orm_cases]
            return cases
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при получении ДЕЛА: {str(e)}')

    async def update(self, updated_case: Case) -> Dict:
        try:
            id = updated_case.id
            stmt = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.execute(stmt)
            orm_case = result.scalars().first()

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
            # ТУТ МОЖЕТ БЫТЬ НУЖЕН FLASH

            # Важно: update здесь сохраняет изменения без явного merge и flush
            return {'success': True, 'case': case}
        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при обновлении данных ДЕЛА: {str(e)}')

    async def delete(self, id: int) -> bool:
        try:
            stmt = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.execute(stmt)
            orm_case = result.scalars().first()
            if not orm_case:
                raise EntityNotFoundException('Дело не найдено')

            await self.session.delete(orm_case)
            await self.session.flush()  # Фиксируем изменения в транзакции
            return True

        except Exception as e:
            raise DatabaseErrorException(f'Ошибка при удалении ДЕЛА: {str(e)}')

    async def _exists(self, id: str) -> bool:
        '''Проверяет существование записи.'''
        stmt = select(CaseORM).where(CaseORM.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None