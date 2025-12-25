from typing import TYPE_CHECKING, List, Dict, Any

from sqlalchemy import select, text
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logger import logger
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.domain.entities.case import Case
from backend.infrastructure.mappers import CaseMapper
from backend.infrastructure.models import CaseORM
from backend.application.interfaces.repositories.case_repo import ICaseRepository

if TYPE_CHECKING:
    from backend.domain.entities.case import Case


class CaseRepository(ICaseRepository):
    '''
    Репозиторий для работы с сущностью «Дело» (Case) в базе данных.
    Реализует CRUD-операции через async SQLAlchemy.
    '''

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
            logger.error(f'Ошибка БД при получении дела ID = {id}: {e}')
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

    # ===============================================================================================
    async def get_all_for_attorney_with_relations(
        self, attorney_id: int
    ) -> List['CaseORM']:
        try:
            # 1. Создаем базовый запрос с фильтром по адвокату
            stmt = (
                select(CaseORM)
                .where(CaseORM.attorney_id == attorney_id)  # Выбор дел для юриста
                .order_by(CaseORM.created_at.desc())
            )
            # 2. Применяем eager loading для связанных объектов
            stmt = stmt.options(
                selectinload(CaseORM.client),
                selectinload(CaseORM.contacts),
            )
            # 3. Выполняем запрос
            result = await self.session.execute(stmt)
            orm_cases = result.scalars().all()

            logger.info(
                f'Получено {len(orm_cases)} дел для адвоката {attorney_id} '
                f'с загруженными связями (client, contacts)'
            )

            # 4. Возвращаем список ORM объектов (БЕЗ маппинга в доменную сущность)
            return list(orm_cases)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении дел с связями для адвоката {attorney_id}: {str(e)}'
            )
            raise DatabaseErrorException(
                f'Ошибка при получении дел с связанными данными: {str(e)}'
            )

    # ===============================================================================================

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

            # 3. Обновление полей ORM-объекта из доменной сущности
            CaseMapper.update_orm(orm_case, updated_case)

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'Дело обновлено. ID = {updated_case.id}')
            return CaseMapper.to_domain(orm_case)

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при обновлении дела ID = {updated_case.id}: {e}')
            raise DatabaseErrorException(f'Ошибка при обновлении данных ДЕЛА: {str(e)}')

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(CaseORM).where(CaseORM.id == id)
            result = await self.session.execute(stmt)
            orm_case = result.scalar_one_or_none()

            if not orm_case:
                logger.warning(f'Дело с ID {id} не найдено при удалении.')
                raise EntityNotFoundException(f'Дело с ID {id} не найдено')

            # 2. Удаление
            await self.session.delete(orm_case)
            await self.session.flush()

            # logger.info(f'Дело с ID {id} успешно удалено.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении ДЕЛА: {str(e)}')

    async def get_dashboard_data(self, attorney_id: int) -> List[Dict[str, Any]]:
        '''
        Получение данных для дашборда по указанному адвокату.
        Возвращает список словарей с данными о делах, клиентах, контактах, событиях и платежах.
        '''
        try:
            query = text("""
                SELECT 
                    c.name AS case_name,
                    cl.name AS client_name,
                    cl.phone AS client_phone,
                    co.name AS contact_name,
                    co.phone AS contact_phone,
                    e.name AS event_name,
                    COUNT(cp.id) AS pending_payments_count
                FROM cases c
                INNER JOIN clients cl ON c.client_id = cl.id
                INNER JOIN contacts co ON co.case_id = c.id
                INNER JOIN attorneys a ON c.attorney_id = a.id
                LEFT JOIN events e ON e.case_id = c.id 
                    AND e.id = (
                        SELECT id FROM events 
                        WHERE case_id = c.id 
                        ORDER BY event_date ASC 
                        LIMIT 1
                    )
                LEFT JOIN client_payments cp ON cp.client_id = cl.id 
                    AND cp.status = 'pending'
                WHERE c.attorney_id = :attorney_id
                GROUP BY c.id, cl.id, co.id, e.id
                LIMIT 1
            """)

            result = await self.session.execute(query, {'attorney_id': attorney_id})
            rows = result.fetchall()

            # Преобразуем результат в список словарей
            dashboard_data = []
            for row in rows:
                dashboard_data.append({
                    'case_name': row.case_name,
                    'client_name': row.client_name,
                    'client_phone': row.client_phone,
                    'contact_name': row.contact_name,
                    'contact_phone': row.contact_phone,
                    'event_name': row.event_name,
                    'pending_payments_count': row.pending_payments_count,
                })

            logger.info(
                f'Получено {len(dashboard_data)} записей для дашборда адвоката {attorney_id}'
            )
            return dashboard_data

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении данных дашборда для адвоката {attorney_id}: {str(e)}'
            )
            raise DatabaseErrorException(
                f'Ошибка при получении данных дашборда: {str(e)}'
            )
