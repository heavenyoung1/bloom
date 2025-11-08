from sqlalchemy.future import select

from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    DataError,
    NoResultFound,
    MultipleResultsFound,
    InvalidRequestError,
)
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

    async def save(self, case: Case) -> 'Case':
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_case = CaseMapper.to_orm(case)

            # 2. Добавление в сессию
            self.session.add(orm_case)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            case.id = orm_case.id

            logger.info(f'ДЕЛО сохранено. ID - {case.id}')
            return case

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении ДЕЛА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении ДЕЛА: {str(e)}')

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении ДЕЛА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении ДЕЛА: {str(e)}')

    async def get(self, id: int) -> 'Case':
        try:
            # 1. Получение записи из базы данных
            stmt = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.execute(stmt)
            orm_case = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_case:
                return None
                # raise EntityNotFoundException(f'Дело с ID {id} не найдено')

            # 3. Преобразование ORM объекта в доменную сущность
            case = CaseMapper.to_domain(orm_case)

            logger.info(f'ДЕЛО получено. ID - {case.id}')
            return case

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении дела ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении ДЕЛА: {str(e)}')

    async def get_all_for_attorney(self, id: int) -> List['Case']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(CaseORM)
                .where(CaseORM.attorney_id == id)  # Фильтрация по адвокату
                .order_by(CaseORM.created_at.desc())  # Например, сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_cases = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [CaseMapper.to_domain(orm_case) for orm_case in orm_cases]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении всех ДЕЛ: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при получении ДЕЛА: {str(e)}')

    async def update(self, updated_case: Case) -> 'Case':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(CaseORM).where(CaseORM.id == updated_case.id)
            result = await self.session.execute(stmt)
            orm_case = result.scalars().first()

            # 2. Проверка наличия записи в БД
            if not orm_case:
                logger.error(f'Дело с ID {updated_case.id} не найдено.')
                raise EntityNotFoundException(f'Дело с ID {updated_case.id} не найдено')

            # 3. Прямое обновление полей ORM-объекта
            orm_case.name = updated_case.name
            orm_case.client_id = updated_case.client_id
            orm_case.status = updated_case.status
            orm_case.description = updated_case.description

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'Дело обновлено. ID= {updated_case.id}')
            return CaseMapper.to_domain(orm_case)

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при обновлении дела ID={updated_case.id}: {e}')
            raise DatabaseErrorException(f'Ошибка при обновлении данных ДЕЛА: {str(e)}')

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.execute(stmt)
            orm_case = result.scalars().first()

            if not orm_case:
                logger.warning(f'Дело с ID {id} не найдено при удалении.')
                raise EntityNotFoundException(f'Дело с ID {id} не найдено')

            # 2. Удаление
            await self.session.delete(orm_case)
            await self.session.flush()

            logger.info(f'Дело с ID {id} успешно удалено.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении ДЕЛА: {str(e)}')
