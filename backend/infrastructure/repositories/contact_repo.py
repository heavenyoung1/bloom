from typing import TYPE_CHECKING, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logger import logger
from backend.core.exceptions import DatabaseErrorException, EntityNotFoundException
from backend.domain.entities.contact import Contact
from backend.infrastructure.mappers import ContactMapper
from backend.infrastructure.models import ContactORM
from backend.application.interfaces.repositories.contact_repo import IContactRepository

if TYPE_CHECKING:
    from backend.domain.entities.contact import Contact


class ContactRepository(IContactRepository):
    '''
    Репозиторий для работы с сущностью «Связанный контакт» (Contact) в базе данных.
    Хранит дополнительные контакты, связанные с делом, например доверитель.
    '''

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, contact: Contact) -> 'Contact':
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_contact = ContactMapper.to_orm(contact)

            # 2. Добавление в сессию
            self.session.add(orm_contact)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            contact.id = orm_contact.id

            logger.info(f'СВЯЗАННЫЙ КОНТАКТ сохранен. ID - {contact.id}')
            return contact

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении СВЯЗАННОГО КОНТАКТА: {str(e)}')
            raise DatabaseErrorException(
                f'Ошибка при сохранении СВЯЗАННОГО КОНТАКТА: {str(e)}'
            )

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении СВЯЗАННОГО КОНТАКТА: {str(e)}')
            raise DatabaseErrorException(
                f'Ошибка при сохранении СВЯЗАННОГО КОНТАКТА: {str(e)}'
            )

    async def get(self, id: int) -> 'Contact':
        try:
            # 1. Получение записи из базы данных
            stmt = select(ContactORM).where(ContactORM.id == id)
            result = await self.session.execute(stmt)
            orm_contact = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_contact:
                return None

            # 3. Преобразование ORM объекта в доменную сущность
            case = ContactMapper.to_domain(orm_contact)

            logger.info(f'СВЯЗАННЫЙ КОНТАКТ получен. ID - {case.id}')
            return case

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении СВЯЗАННОГО КОНТАКТА ID = {id}: {e}')
            raise DatabaseErrorException(
                f'Ошибка при получении СВЯЗАННОГО КОНТАКТА: {str(e)}'
            )

    async def get_all_for_attorney(self, attorney_id: int) -> List['Contact']:
        try:
            # 1. Получение записи из базы данных
            stmt = select(ContactORM).where(ContactORM.attorney_id == attorney_id)
            result = await self.session.execute(stmt)
            orm_contacts = result.scalars().all()

            # 2. Проверка существования записи в БД
            if not orm_contacts:
                None

            # 3. Преобразование ORM объекта в доменную сущность
            contacts = [
                ContactMapper.to_domain(orm_contact) for orm_contact in orm_contacts
            ]

            logger.info(f'СВЯЗАННЫЙ КОНТАКТ получен. ID - {case.id}')
            return contacts

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении СВЯЗАННОГО КОНТАКТА ID = {id}: {e}')
            raise DatabaseErrorException(
                f'Ошибка при получении СВЯЗАННОГО КОНТАКТА: {str(e)}'
            )

    async def get_all_for_case(self, id: int) -> List['Contact']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(ContactORM)
                .where(ContactORM.case_id == id)  # Фильтрация по делу
                .order_by(ContactORM.created_at.desc())  # Например, сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_contacts = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [
                ContactMapper.to_domain(orm_contact) for orm_contact in orm_contacts
            ]

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении СВЯЗАННОГО КОНТАКТА ID = {id}: {e}')
            raise DatabaseErrorException(
                f'Ошибка при получении СВЯЗАННОГО КОНТАКТА: {str(e)}'
            )

    async def update(self, updated_contact: Contact) -> 'Contact':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(ContactORM).where(ContactORM.id == updated_contact.id)
            result = await self.session.execute(stmt)
            orm_contact = result.scalars().first()

            # 2. Проверка наличия записи в БД
            if not orm_contact:
                logger.error(f'СВЯЗАННЫЙ КОНТАКТ с ID {updated_contact.id} не найден.')
                raise EntityNotFoundException(
                    f'СВЯЗАННЫЙ КОНТАКТ с ID {updated_contact.id} не найден.'
                )

            # 3. Прямое обновление полей ORM-объекта
            orm_contact.name = updated_contact.name
            orm_contact.personal_info = updated_contact.personal_info
            orm_contact.phone = updated_contact.phone
            orm_contact.email = updated_contact.email
            orm_contact.case_id = updated_contact.case_id

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'СВЯЗАННЫЙ КОНТАКТ обновлен. ID= {updated_contact.id}')
            return ContactMapper.to_domain(orm_contact)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении СВЯЗАННОГО КОНТАКТА. ID={updated_contact.id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при обновлении СВЯЗАННОГО КОНТАКТА. ID={updated_contact.id}: {e}'
            )

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(ContactORM).where(ContactORM.id == id)
            result = await self.session.execute(stmt)
            orm_contact = result.scalars().first()

            if not orm_contact:
                logger.warning(f'СВЯЗАННЫЙ КОНТАКТ с ID {id} не найден при удалении.')
                raise EntityNotFoundException(
                    f'СВЯЗАННЫЙ КОНТАКТ с ID {id} не найден при удалении.'
                )

            # 2. Удаление
            await self.session.delete(orm_contact)
            await self.session.flush()

            logger.info(f'СВЯЗАННЫЙ КОНТАКТ с ID {id} успешно удален.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(
                f'Ошибка при удалении СВЯЗАННОГО КОНТАКТА: {str(e)}'
            )
