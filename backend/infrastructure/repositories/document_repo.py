from typing import TYPE_CHECKING, List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.logger import logger
from backend.core.exceptions import (
    DatabaseErrorException,
    EntityNotFoundException,
)
from backend.domain.entities.document import Document
from backend.infrastructure.mappers import DocumentMapper
from backend.infrastructure.models import DocumentORM
from backend.infrastructure.repositories.interfaces import IDocumentMetadataRepository

if TYPE_CHECKING:
    from backend.domain.entities.document import Document


class DocumentMetadataRepository(IDocumentMetadataRepository):
    '''
    Репозиторий для работы с информацией о документах в БД.
    НЕ работает с реальными файлами!
    '''

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, document: Document) -> 'Document':
        '''Сохраняет документ: метаданные в БД, файл в файловую систему'''
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_document = DocumentMapper.to_orm(document)

            # 2. Добавление в сессию
            self.session.add(orm_document)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            document.id = orm_document.id

            logger.info(f'МЕТАДАННЫЕ ДОКУМЕНТА сохранены. ID - {document.id}')
            return document

        except IntegrityError as e:
            logger.error(f'Ошибка при сохранении МЕТАДАННЫХ ДОКУМЕНТА: {str(e)}')
            raise DatabaseErrorException(
                f'Ошибка при сохранении МЕТАДАННЫХ ДОКУМЕНТА: {str(e)}'
            )

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при сохранении МЕТАДАННЫХ ДОКУМЕНТА: {str(e)}')
            raise DatabaseErrorException(
                f'Ошибка при сохранении МЕТАДАННЫХ ДОКУМЕНТА: {str(e)}'
            )

    async def get(self, id: int) -> 'Document':
        try:
            # 1. Получение записи из базы данных
            stmt = select(DocumentORM).where(DocumentORM.id == id)
            result = await self.session.execute(stmt)
            orm_document = result.scalars().first()

            # 2. Проверка существования записи в БД
            if not orm_document:
                return None

            # 3. Преобразование ORM объекта в доменную сущность
            case = DocumentMapper.to_domain(orm_document)

            logger.info(f'МЕТАДАННЫЕ ДОКУМЕНТА получены. ID - {case.id}')
            return case

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении МЕТАДАННЫХ ДОКУМЕНТА. ID = {id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка при получении МЕТАДАННЫХ ДОКУМЕНТА: {str(e)}'
            )

    async def get_all_for_case(self, id: int) -> List['Document']:
        try:
            # 1. Получение записей из базы данных
            stmt = (
                select(DocumentORM)
                .where(DocumentORM.case_id == id)  # Фильтрация по делу
                .order_by(DocumentORM.created_at.desc())  # Сортировка по дате
            )
            result = await self.session.execute(stmt)
            orm_documents = result.scalars().all()

            # 2. Списковый генератор для всех записей из базы данных
            return [
                DocumentMapper.to_domain(orm_contact) for orm_contact in orm_documents
            ]

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении МЕТАДАННЫХ ДОКУМЕНТА. ID = {id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка при получении МЕТАДАННЫХ ДОКУМЕНТА: {str(e)}'
            )

    async def update(self, updated_document: Document) -> 'Document':
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(DocumentORM).where(DocumentORM.id == DocumentORM.id)
            result = await self.session.execute(stmt)
            orm_document = result.scalars().first()

            # 2. Проверка наличия записи в БД
            if not orm_document:
                logger.error(
                    f'МЕТАДАННЫЕ ДОКУМЕНТА с ID {updated_document.id} не найдены.'
                )
                raise EntityNotFoundException(
                    f'МЕТАДАННЫЕ ДОКУМЕНТА с ID {updated_document.id} не найдены.'
                )

            # 3. Прямое обновление полей ORM-объекта
            orm_document.file_name = updated_document.file_name
            orm_document.storage_path = updated_document.storage_path
            orm_document.file_size = updated_document.file_size
            orm_document.description = updated_document.description

            # 4. Сохранение в БД
            await self.session.flush()  # или session.commit() если нужна транзакция

            # 5. Возврат доменного объекта
            logger.info(f'МЕТАДАННЫЕ ДОКУМЕНТА обновлены. ID= {updated_document.id}')
            return DocumentMapper.to_domain(orm_document)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении МЕТАДАННЫХ ДОКУМЕНТА. ID={updated_document.id}: {e}'
            )
            raise DatabaseErrorException(
                f'Ошибка БД при обновлении МЕТАДАННЫХ ДОКУМЕНТА. ID={updated_document.id}: {e}'
            )

    async def delete(self, id: int) -> bool:
        try:
            # 1. Выполнение запроса на извлечение данных из БД
            stmt = select(DocumentORM).where(DocumentORM.id == id)
            result = await self.session.execute(stmt)
            orm_document = result.scalars().first()

            if not orm_document:
                logger.warning(
                    f'МЕТАДАННЫЕ ДОКУМЕНТА с ID {id} не найдены при удалении.'
                )
                raise EntityNotFoundException(
                    f'МЕТАДАННЫЕ ДОКУМЕНТА с ID {id} не найдены при удалении.'
                )

            # 2. Удаление
            await self.session.delete(orm_document)
            await self.session.flush()

            logger.info(f'МЕТАДАННЫЕ ДОКУМЕНТА с ID {id} успешно удалены.')
            return True

        except SQLAlchemyError as e:
            raise DatabaseErrorException(
                f'Ошибка при удалении МЕТАДАННЫЕ ДОКУМЕНТА: {str(e)}'
            )
