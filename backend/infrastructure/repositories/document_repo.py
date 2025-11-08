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
from typing import Optional
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, TYPE_CHECKING
from datetime import datetime
from backend.domain.entities.document import Document
from backend.infrastructure.mappers import DocumentMapper
from backend.infrastructure.models import DocumentORM
from backend.core.exceptions import (
    DatabaseErrorException,
    EntityNotFoundException,
    EntityAlreadyExistsError,
    FileStorageException,
)

from backend.infrastructure.repositories.interfaces import IDocumentRepository
from backend.core.logger import logger

from pathlib import Path


class DocumentRepository(IDocumentRepository):
    def __init__(
        self, session: AsyncSession, storage_path: str = '/var/law_system/documents'
    ):
        '''
        :param session: Асинхронная сессия SQLAlchemy
        :param storage_path: Корневая директория для хранения файлов
        '''
        self.session = session
        self.storage_path = Path(storage_path)

        # Создаем директорию если её нет
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _generate_file_path(self, case_id: int, filename: str) -> Path:
        '''
        Генерирует путь для сохранения файла.
        Структура: /var/law_system/documents/{case_id}/{timestamp}_{filename}
        '''
        case_dir = self.storage_path / str(case_id)
        case_dir.mkdir(parents=True, exist_ok=True)

        # Добавляем timestamp для уникальности
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f'{timestamp}_{filename}'

        return case_dir / unique_filename

    async def save(self, document: Document, file_content: bytes) -> 'Document':
        '''Сохраняет документ: метаданные в БД, файл в файловую систему'''
        try:
            # 1. Генерируем путь для файла
            file_path = self._generate_file_path(document.case_id, document.filename)

            # 2. Сохраняем файл в файловую систему асинхронно
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)

            # 3. Обновляем путь в документе
            document.storage_path = str(file_path)
            document.file_size = len(file_content)

            # 4. Конвертируем в ORM и сохраняем метаданные в БД
            orm_document = DocumentMapper.to_orm(document)
            self.session.add(orm_document)
            await self.session.flush()

            # 5. Обновляем ID в доменном объекте
            document.id = orm_document.id

            logger.info(f'Документ сохранен. ID={document.id}, Path={file_path}')
            return document

        except OSError as e:
            logger.error(f'Ошибка при сохранении файла: {str(e)}')
            raise FileStorageException(f'Ошибка при сохранении файла: {str(e)}')

        except IntegrityError as e:
            # Если ошибка в БД, удаляем созданный файл
            if file_path.exists():
                file_path.unlink()
            logger.error(f'Ошибка целостности при сохранении документа: {str(e)}')
            raise DatabaseErrorException(f'Ошибка при сохранении документа: {str(e)}')

    async def get(self, id: int) -> Optional[Document]:
        '''
        Получает метаданные документа по ID
        '''
        try:
            stmt = select(DocumentORM).where(DocumentORM.id == id)
            result = await self.session.execute(stmt)
            orm_document = result.scalars().first()

            if not orm_document:
                return None

            document = DocumentMapper.to_domain(orm_document)
            logger.info(f'Документ получен. ID={document.id}')
            return document

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при получении документа ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка при получении документа: {str(e)}')

    async def get_file_content(self, id: int) -> bytes:
        '''
        Получает содержимое файла документа
        '''
        try:
            # 1. Получаем метаданные документа
            document = await self.get(id)

            if not document:
                raise EntityNotFoundException(f'Документ с ID {id} не найден')

            # 2. Проверяем существование файла
            file_path = Path(document.file_path)
            if not file_path.exists():
                logger.error(f'Файл не найден: {file_path}')
                raise FileStorageException(f'Файл документа не найден: {file_path}')

            # 3. Читаем файл асинхронно
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()

            logger.info(f'Содержимое документа получено. ID={id}')
            return content

        except OSError as e:
            logger.error(f'Ошибка при чтении файла: {str(e)}')
            raise FileStorageException(f'Ошибка при чтении файла: {str(e)}')

    async def get_all_for_case(self, case_id: int) -> List['Document']:
        '''Получает все документы для конкретного дела'''
        try:
            stmt = (
                select(DocumentORM)
                .where(DocumentORM.case_id == case_id)
                .order_by(DocumentORM.created_at.desc())
            )
            result = await self.session.execute(stmt)
            orm_documents = result.scalars().all()

            documents = [DocumentMapper.to_domain(orm_doc) for orm_doc in orm_documents]
            return documents

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при получении документов для дела ID={case_id}: {e}'
            )
            raise DatabaseErrorException(f'Ошибка при получении документов: {str(e)}')

    async def update(self, updated_document: Document) -> Document:
        '''
        Обновляет метаданные документа (НЕ сам файл!)
        '''
        try:
            stmt = select(DocumentORM).where(DocumentORM.id == updated_document.id)
            result = await self.session.execute(stmt)
            orm_document = result.scalars().first()

            if not orm_document:
                logger.error(f'Документ с ID {updated_document.id} не найден.')
                raise EntityNotFoundException(
                    f'Документ с ID {updated_document.id} не найден'
                )

            # Обновляем только метаданные
            orm_document.filename = updated_document.filename
            orm_document.description = updated_document.description
            orm_document.document_type = updated_document.document_type

            await self.session.flush()

            logger.info(f'Документ обновлен. ID={updated_document.id}')
            return DocumentMapper.to_domain(orm_document)

        except SQLAlchemyError as e:
            logger.error(
                f'Ошибка БД при обновлении документа ID={updated_document.id}: {e}'
            )
            raise DatabaseErrorException(f'Ошибка при обновлении документа: {str(e)}')

    async def delete(self, id: int) -> bool:
        '''
        Удаляет документ: и из БД, и из файловой системы
        '''
        try:
            # 1. Получаем документ
            stmt = select(DocumentORM).where(DocumentORM.id == id)
            result = await self.session.execute(stmt)
            orm_document = result.scalars().first()

            if not orm_document:
                logger.warning(f'Документ с ID {id} не найден при удалении.')
                raise EntityNotFoundException(f'Документ с ID {id} не найден')

            # 2. Удаляем файл из файловой системы
            file_path = Path(orm_document.file_path)
            if file_path.exists():
                file_path.unlink()
                logger.info(f'Файл удален: {file_path}')
            else:
                logger.warning(f'Файл уже отсутствует: {file_path}')

            # 3. Удаляем запись из БД
            await self.session.delete(orm_document)
            await self.session.flush()

            logger.info(f'Документ с ID {id} успешно удален.')
            return True

        except OSError as e:
            logger.error(f'Ошибка при удалении файла: {str(e)}')
            raise FileStorageException(f'Ошибка при удалении файла: {str(e)}')

        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД при удалении документа ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка при удалении документа: {str(e)}')

    async def exists(self, id: int) -> bool:
        '''
        Проверяет существование документа
        '''
        try:
            stmt = select(DocumentORM.id).where(DocumentORM.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none() is not None

        except SQLAlchemyError as e:
            logger.error(f'Ошибка при проверке существования документа ID={id}: {e}')
            raise DatabaseErrorException(f'Ошибка при проверке документа: {str(e)}')
