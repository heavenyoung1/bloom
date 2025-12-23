from backend.application.interfaces.repositories.document_repo import (
    IDocumentMetadataRepository,
)
from backend.application.interfaces.repositories.local_storage import IFileStorage
from backend.infrastructure.tools.file_metadata import FileMetadataExtractor
from backend.core.logger import logger
import uuid
from pathlib import Path


class DocumentService:
    '''
    Сервис для работы с документами.
    Координирует: сохранение метаданных в БД + сохранение файла на диск/облако
    '''

    def __init__(
        self, document_repo: IDocumentMetadataRepository, file_storage: IFileStorage
    ):
        self.document_repo = document_repo
        self.file_storage = file_storage
        self.metadata_extractor = FileMetadataExtractor()

    async def upload_document(
        self,
        case_id: int,
        attorney_id: int,
        file_name: str,
        file_content: bytes,
        description: str = '',
    ) -> 'Document':
        '''
        Загружает документ в систему.

        Args:
            case_id: ID дела, к которому прикрепляется документ
            attorney_id: ID юриста, владельца документа
            file_name: Оригинальное имя файла
            file_content: Содержимое файла в байтах
            description: Описание документа

        Returns:
            Сохраненный объект Document
        '''
        try:
            # 1. Извлекаем метаданные файла
            metadata = self.metadata_extractor.extract_all_metadata(
                file_content, file_name
            )
            mime_type = metadata['mime_type']
            file_size = metadata['file_size']

            # 2. Генерируем уникальное имя файла для хранения
            # Это предотвращает коллизии имен и обеспечивает безопасность
            file_extension = Path(file_name).suffix
            unique_file_name = f'{uuid.uuid4()}{file_extension}'
            storage_path = f'cases/{case_id}/{unique_file_name}'

            # 3. Сохраняем файл в хранилище
            saved_path = await self.file_storage.save_file(
                file_path=storage_path, file_content=file_content
            )

            logger.info(
                f'Файл сохранен: {saved_path}, '
                f'MIME: {mime_type}, Размер: {file_size} байт'
            )

            # 4. Создаем доменную сущность документа
            from backend.domain.entities.document import Document

            document = Document.create(
                file_name=file_name,  # Оригинальное имя для пользователя
                storage_path=saved_path,
                file_size=file_size,
                case_id=case_id,
                attorney_id=attorney_id,
                description=description,
                mime_type=mime_type,
            )

            # 5. Сохраняем метаданные в БД
            saved_document = await self.document_repo.save(document)

            logger.info(f'Документ создан: ID={saved_document.id}, Файл={file_name}')
            return saved_document

        except Exception as e:
            logger.error(f'Ошибка при загрузке документа: {e}')
            # Если файл был сохранен, но ошибка при сохранении в БД,
            # можно добавить логику удаления файла
            raise

    async def get_document_file(self, document_id: int) -> tuple[bytes, str, str]:
        '''
        Получает содержимое файла документа.

        Args:
            document_id: ID документа

        Returns:
            Кортеж (file_content, file_name, mime_type)
        '''
        # 1. Получаем метаданные документа из БД
        document = await self.document_repo.get(document_id)
        if not document:
            from backend.core.exceptions import EntityNotFoundException

            raise EntityNotFoundException(f'Документ с ID {document_id} не найден')

        # 2. Получаем файл из хранилища
        file_content = await self.file_storage.get_file(document.storage_path)

        return (
            file_content,
            document.file_name,
            document.mime_type or 'application/octet-stream',
        )

    async def delete_document(self, document_id: int) -> bool:
        '''
        Удаляет документ (файл и метаданные).

        Args:
            document_id: ID документа

        Returns:
            True если удаление прошло успешно
        '''
        # 1. Получаем метаданные для получения пути к файлу
        document = await self.document_repo.get(document_id)
        if not document:
            from backend.core.exceptions import EntityNotFoundException

            raise EntityNotFoundException(f'Документ с ID {document_id} не найден')

        # 2. Удаляем файл из хранилища
        try:
            await self.file_storage.delete_file(document.storage_path)
        except Exception as e:
            logger.warning(
                f'Ошибка при удалении файла {document.storage_path}: {e}. '
                'Продолжаем удаление метаданных.'
            )

        # 3. Удаляем метаданные из БД
        await self.document_repo.delete(document_id)

        logger.info(f'Документ удален: ID={document_id}')
        return True
