from typing import Optional, TYPE_CHECKING

from sqlalchemy import select, func
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
            # КАК БУДТО ВРЕМЯ ЗДЕСЬ НЕ БУДЕТ ПРИСВАИВАТЬСЯ!!!
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
            # 1. Получение записи из базы данных
            stmt = select(AttorneyORM).where(AttorneyORM.id == id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_attorney:
                return None

            # 3. Преобразование ORM объекта в доменную сущность
            attorney = AttorneyMapper.to_domain(orm_attorney)

            logger.info(f'ЮРИСТ успешно получен. ID - {attorney.id}')
            return attorney

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении ЮРИСТА ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка БД при получении ЮРИСТА: {str(e)}')

    async def get_by_email(self, email: str) -> Optional['Attorney']:
        try:
            # 1. Получение записи из базы данных
            stmt = select(AttorneyORM).where(AttorneyORM.email == email)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalars().first()

            # 2. Проверка существования записи в БД
            if orm_attorney:
                attorney = AttorneyMapper.to_domain(orm_attorney)
                logger.info(
                    f'ЮРИСТ успешно получен по email. ID - {attorney.id}. Email - {attorney.email}.'
                )
                return attorney
            else:
                return None
        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении ЮРИСТА по email={email}: {e}')
            raise DatabaseErrorException(
                f'Ошибка БД при получении ЮРИСТА по email: {str(e)}'
            )

    async def get_by_license_id(self, license_id: str) -> Optional['Attorney']:
        try:
            # 1. Получение записи из базы данных
            stmt = select(AttorneyORM).where(AttorneyORM.license_id == license_id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalars().first()

            # 2. Проверка существования записи в БД
            if orm_attorney:
                attorney = AttorneyMapper.to_domain(orm_attorney)
                logger.info(
                    f'ЮРИСТ успешно получен по license_id. ID - {attorney.id}. license_id - {attorney.license_id}.'
                )
                return attorney
            else:
                return None
        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении ЮРИСТА по license_id={license_id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при получении ЮРИСТА по license_id: {str(e)}'
            )

    async def get_by_phone(self, phone_number: str) -> Optional['Attorney']:
        try:
            # 1. Получение записи из базы данных
            stmt = select(AttorneyORM).where(AttorneyORM.phone == phone_number)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalars().first()

            # 2. Проверка существования записи в БД
            if orm_attorney:
                attorney = AttorneyMapper.to_domain(orm_attorney)
                logger.info(
                    f'ЮРИСТ успешно получен по номеру телефона. ID - {attorney.id}. phone_number - {attorney.phone}.'
                )
                return attorney
            else:
                return None
        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении ЮРИСТА по phone_number = {phone_number}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при получении ЮРИСТА по license_id: {str(e)}'
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

            # 3. Прямое обновление полей ORM-объекта
            # ПОХОЖЕ НА КУСОК ДЕРЬМА
            # ПРИДУМАТЬ КАК НЕ ПЕРЕДАВАТЬ ПО ОДНОМУ АРГУМЕНТУ
            orm_attorney.license_id = updated_attorney.license_id
            orm_attorney.first_name = updated_attorney.first_name
            orm_attorney.last_name = updated_attorney.last_name
            orm_attorney.patronymic = updated_attorney.patronymic
            orm_attorney.email = updated_attorney.email
            orm_attorney.telegram_username = updated_attorney.telegram_username
            orm_attorney.phone = updated_attorney.phone
            orm_attorney.hashed_password = updated_attorney.hashed_password

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
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(AttorneyORM).where(AttorneyORM.id == attorney_id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalar_one_or_none()

            # 2. Проверка наличия записи в БД
            if not orm_attorney:
                logger.error(f'Юрист с ID {attorney_id} не найден.')
                raise EntityNotFoundException(f'Юрист с ID {attorney_id} не найден.')

            # 3. Прямое обновление полей ORM-объекта
            orm_attorney.is_verified = is_verified

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'Юрист обновлен. ID = {orm_attorney.id}')
            return AttorneyMapper.to_domain(orm_attorney)

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при обновлении ЮРИСТА ID={orm_attorney.id}: {e}')
            raise DatabaseErrorException(
                f'Ошибка при обновлении данных ЮРИСТА: {str(e)}'
            )

    async def change_is_avtive(self, attorney_id: int, is_active: bool) -> 'Attorney':
        '''Изменить статус верификации Юриста по ID.'''
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(AttorneyORM).where(AttorneyORM.id == attorney_id)
            result = await self.session.execute(stmt)
            orm_attorney = result.scalar_one_or_none()

            # 2. Проверка наличия записи в БД
            if not orm_attorney:
                logger.error(f'Юрист с ID {attorney_id} не найден.')
                raise EntityNotFoundException(f'Юрист с ID {attorney_id} не найден.')

            # 3. Прямое обновление полей ORM-объекта
            orm_attorney.is_verified = is_active

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'Юрист обновлен. ID = {orm_attorney.id}')
            return AttorneyMapper.to_domain(orm_attorney)

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при обновлении ЮРИСТА ID={orm_attorney.id}: {e}')
            raise DatabaseErrorException(
                f'Ошибка при обновлении данных ЮРИСТА: {str(e)}'
            )
