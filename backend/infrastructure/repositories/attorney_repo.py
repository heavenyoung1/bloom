from typing import Optional, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logger import logger
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.domain.entities.attorney import Attorney
from backend.infrastructure.mappers import AttorneyMapper
from backend.infrastructure.models import AttorneyORM
from backend.application.interfaces.repositories.attorney_repo import (
    IAttorneyRepository,
)

if TYPE_CHECKING:
    from backend.domain.entities.attorney import Attorney


class AttorneyRepository(IAttorneyRepository):
    '''
    Репозиторий для работы с сущностью «Юрист» (Attorney) в базе данных.

    Реализует CRUD-операции через SQLAlchemy AsyncSession.
    Все методы асинхронны и выбрасывают кастомные исключения при ошибках.
    '''

    def __init__(self, session: AsyncSession):
        '''Инициализация репозитория с асинхронной сессией SQLAlchemy.'''
        self.session = session

    async def save(self, attorney: Attorney) -> 'Attorney':
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_attorney = AttorneyMapper.to_orm(attorney)

            # 2. Добавление в сессию
            self.session.add(orm_attorney)

            # 3. flush() — отправляем в БД, получаем ID и timestamps
            await self.session.flush()

            # 4. Обновляем ID и timestamps в доменном объекте
            # (после flush() ORM объект уже имеет установленные created_at и updated_at)
            attorney.id = orm_attorney.id
            attorney.created_at = orm_attorney.created_at
            attorney.updated_at = orm_attorney.updated_at

            logger.info(f'ЮРИСТ сохранен. ID - {attorney.id}')
            return attorney

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении ЮРИСТА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении ЮРИСТА: {str(e)}')

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении ЮРИСТА: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении ЮРИСТА: {str(e)}')

    async def get(self, id: int) -> Optional['Attorney']:
        try:
            stmt = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalar_one_or_none()

            if not orm_attorney:
                return None

            attorney = AttorneyMapper.to_domain(orm_attorney)
            logger.info(f'ЮРИСТ успешно получен. ID - {attorney.id}')
            return attorney

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении ЮРИСТА ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка БД при получении ЮРИСТА: {str(e)}')

    async def get_by_email(self, email: str) -> Optional['Attorney']:
        return await self._get_by_field(AttorneyORM.email == email, 'email', email)

    async def get_by_license_id(self, license_id: str) -> Optional['Attorney']:
        return await self._get_by_field(
            AttorneyORM.license_id == license_id, 'license_id', license_id
        )

    async def get_by_phone(self, phone_number: str) -> Optional['Attorney']:
        return await self._get_by_field(
            AttorneyORM.phone == phone_number, 'phone_number', phone_number
        )

    async def update(self, updated_attorney: Attorney) -> 'Attorney':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(AttorneyORM).where(AttorneyORM.id == updated_attorney.id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalar_one_or_none()

            # 2. Проверка наличия записи в БД
            if not orm_attorney:
                logger.error(f'Юрист с ID {updated_attorney.id} не найден.')
                raise EntityNotFoundException(
                    f'Юрист с ID {updated_attorney.id} не найден.'
                )

            # 3. Обновление полей ORM-объекта из доменной сущности
            AttorneyMapper.update_orm(orm_attorney, updated_attorney)

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'Юрист обновлен. ID = {updated_attorney.id}')
            return AttorneyMapper.to_domain(orm_attorney)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении ЮРИСТА ID={updated_attorney.id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка при обновлении данных ЮРИСТА: {str(e)}'
            )

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalars().first()

            if not orm_attorney:
                logger.warning(f'ЮРИСТ с ID {id} не найден при удалении.')
                raise EntityNotFoundException(
                    f'ЮРИСТ с ID {id} не найден при удалении.'
                )

            # 2. Удаление
            await self.session.delete(orm_attorney)
            await self.session.flush()

            logger.info(f'ЮРИСТ с ID {id} успешно удален.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(f'Ошибка при удалении ЮРИСТА: {str(e)}')

    async def change_verify(self, attorney_id: int, is_verified: bool) -> 'Attorney':
        '''Изменить статус верификации Юриста по ID.'''
        return await self._change_field(
            attorney_id, 'is_verified', is_verified, 'верификации'
        )

    async def change_is_active(self, attorney_id: int, is_active: bool) -> 'Attorney':
        '''Изменить статус активности Юриста по ID.'''
        return await self._change_field(
            attorney_id, 'is_active', is_active, 'активности'
        )

    async def _get_by_field(
        self, condition, field_name: str, field_value: str
    ) -> Optional['Attorney']:
        '''
        Вспомогательный метод для получения юриста по произвольному полю.

        Args:
            condition: SQLAlchemy условие для фильтрации
            field_name: Название поля для логирования
            field_value: Значение поля для логирования

        Returns:
            Optional[Attorney]: Найденный юрист или None
        '''
        try:
            stmt = select(AttorneyORM).where(condition)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalar_one_or_none()

            if not orm_attorney:
                return None

            attorney = AttorneyMapper.to_domain(orm_attorney)
            # Получаем значение из ORM объекта для логирования
            # Маппинг имен полей: phone_number -> phone
            orm_field_name = field_name.replace('_number', '')
            actual_value = getattr(orm_attorney, orm_field_name, field_value)
            logger.info(
                f'ЮРИСТ успешно получен по {field_name}. ID - {attorney.id}. {field_name} - {actual_value}.'
            )
            return attorney

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении ЮРИСТА по {field_name}={field_value}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при получении ЮРИСТА по {field_name}: {str(e)}'
            )

    async def _change_field(
        self, attorney_id: int, field_name: str, field_value: bool, field_label: str
    ) -> 'Attorney':
        '''
        Вспомогательный метод для изменения булевого поля юриста.

        Args:
            attorney_id: ID юриста
            field_name: Название поля для обновления
            field_value: Новое значение поля
            field_label: Название поля для логирования (например, 'верификации')

        Returns:
            Attorney: Обновленный юрист
        '''
        try:
            stmt = select(AttorneyORM).where(AttorneyORM.id == attorney_id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalar_one_or_none()

            if not orm_attorney:
                logger.error(f'Юрист с ID {attorney_id} не найден.')
                raise EntityNotFoundException(f'Юрист с ID {attorney_id} не найден.')

            setattr(orm_attorney, field_name, field_value)
            await self.session.flush()

            logger.info(f'Юрист обновлен. ID = {orm_attorney.id}')
            return AttorneyMapper.to_domain(orm_attorney)

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при обновлении ЮРИСТА ID={attorney_id}: {e}')
            raise DatabaseErrorException(
                f'Ошибка при обновлении {field_label} ЮРИСТА: {str(e)}'
            )
