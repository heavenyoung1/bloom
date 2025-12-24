from typing import List
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.core.logger import logger
from backend.domain.entities.event import Event
from backend.infrastructure.mappers import EventMapper
from backend.infrastructure.models import EventORM
from backend.application.interfaces.repositories.event_repo import IEventRepository


class EventRepository(IEventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, event: Event) -> 'Event':
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_event = EventMapper.to_orm(event)

            # 2. Добавление в сессию
            self.session.add(orm_event)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            event.id = orm_event.id

            logger.info(f'СОБЫТИЕ сохранено. ID - {event.id}')
            return event

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении СОБЫТИЯ: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении СОБЫТИЯ: {str(e)}')

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении СОБЫТИЯ: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении СОБЫТИЯ: {str(e)}')

    async def get(self, id: int) -> 'Event':
        try:
            # 1. Получение записи из базы данных
            stmt = select(EventORM).where(EventORM.id == id)
            result = await self.session.execute(stmt)
            orm_event = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_event:
                return None

            # 3. Преобразование ORM объекта в доменную сущность
            event = EventMapper.to_domain(orm_event)

            logger.info(f'СОБЫТИЕ получено. ID - {event.id}')
            return event

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении СОБЫТИЯ. ID = {id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении СОБЫТИЯ: {str(e)}')

    async def get_for_case(self, case_id: int) -> List['Event']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(EventORM)
                .where(EventORM.case_id == case_id)  # Фильтрация по делу
                .order_by(EventORM.created_at.desc())  # Например, сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_events = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [EventMapper.to_domain(orm_event) for orm_event in orm_events]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении СОБЫТИЯ. ID = {case_id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении СОБЫТИЯ: {str(e)}')

    async def get_all_for_attorney(self, attorney_id: int) -> List['Event']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(EventORM)
                .where(EventORM.attorney_id == attorney_id)  # Фильтрация по адвокату
                .order_by(EventORM.created_at.desc())  # Например, сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_events = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [EventMapper.to_domain(orm_event) for orm_event in orm_events]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении СОБЫТИЯ. ID = {attorney_id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении СОБЫТИЯ: {str(e)}')

    async def get_nearest_for_attorney(
        self, attorney_id: int, count: int
    ) -> List['Event']:
        '''Получить ближайшие события по дате и ограниченные по количеству'''
        try:
            now = datetime.now(timezone.utc)
            # 1. Получение записей из базы данных
            stmt = (
                select(EventORM)
                .where(
                    EventORM.attorney_id == attorney_id,
                    EventORM.event_date >= now,
                )
                .order_by(EventORM.event_date.asc())
                .limit(count)
            )
            result = await self.session.execute(stmt)
            orm_events = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [EventMapper.to_domain(orm_event) for orm_event in orm_events]

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении ближайших СОБЫТИЙ. ID = {attorney_id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка при получении ближайших СОБЫТИЙ: {str(e)}'
            )

    async def update(self, updated_event: Event) -> 'Event':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(EventORM).where(EventORM.id == updated_event.id)
            result = await self.session.execute(stmt)
            orm_event = result.scalars().first()

            # 2. Проверка наличия записи в БД
            if not orm_event:
                logger.error(f'СОБЫТИЕ с ID {updated_event.id} не найдено.')
                raise EntityNotFoundException(
                    f'СОБЫТИЕ с ID {updated_event.id} не найдено.'
                )

            # 3. Обновление полей ORM-объекта из доменной сущности
            EventMapper.update_orm(orm_event, updated_event)

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'СОБЫТИЕ обновлено. ID= {updated_event.id}')
            return EventMapper.to_domain(orm_event)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении СОБЫТИЯ. ID={updated_event.id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при обновлении СОБЫТИЯ. ID={updated_event.id}: {e}'
            )

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(EventORM).where(EventORM.id == id)
            result = await self.session.execute(stmt)
            orm_event = result.scalars().first()

            if not orm_event:
                logger.warning(f'СОБЫТИЕ с ID {id} не найдено при удалении.')
                raise EntityNotFoundException(
                    f'СОБЫТИЕ с ID {id} не найдено при удалении.'
                )

            # 2. Удаление
            self.session.delete(orm_event)
            await self.session.flush()

            logger.info(f'СОБЫТИЕ с ID {id} успешно удалено.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении СОБЫТИЯ: {str(e)}')
